import helper as hp
import spider_config as cf
import xml.etree.ElementTree as et
import requests

from urllib.request import urlopen
from bs4            import BeautifulSoup, NavigableString, Tag
from underthesea    import pos_tag

def getLinkFromRSS(keyword, fileName):
    links = []
    counter = 0
    first = 1
    while counter < 10:
        try:
            search_url = hp.makeSearchURL(keyword, first)
            rss = et.parse(urlopen(search_url)).getroot()
            temp = []
            for link in rss.iter('link'):
                link = link.text
                if len(link) > 85 and "bing" not in link:
                    temp.append(link)
                    counter += 1
                if counter == 10:
                    break
            links = links + temp
            first = first + 10
        except Exception as e:
            print(e)
    hp.writeListIntoFile(links, fileName)

def get500AccidentPages():
    keywords = hp.readFileIntoList(cf.ACCIDENT_KEYWORDS_FILE)
    for keyword in keywords:
        print('Getting pages for keyword: ' + keyword)
        getLinkFromRSS(keyword, cf.ACCIDENT_PAGES_FILE)

def checkExistClass(class_checking, classes):
    if classes is None: 
        return False
    for class_name in classes:
        if class_checking in class_name.lower():
            return True
    return False

def getContent(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        # Ignore anything in head
        body, text = soup.body, []
        for element in body.descendants:
            if type(element) == NavigableString:
                parent_tags = (t for t in element.parents if type(t) == Tag)
                hidden = False
                for parent_tag in parent_tags:
                    classes_tag = parent_tag.get('class')
                    footer = checkExistClass('footer', classes_tag)
                    video = checkExistClass('video', classes_tag)
                    time = checkExistClass('time', classes_tag)
                    hide = checkExistClass('hide', classes_tag) 
                    idTag = parent_tag.get('id')
                    comment = checkExistClass('comment', idTag)
                    footer_id = checkExistClass('footer', idTag)
                    feedback = checkExistClass('feedback', idTag)                     
                    # Ignore any text inside a non-displayed tag
                    if (parent_tag.name in ('em', 'input', 'button', 'area', 'base', 'basefont', 'datalist', 'head', 'link',
                                            'meta', 'noembed', 'noframes', 'param', 'rp', 'script',
                                            'source', 'style', 'template', 'track', 'title', 'noscript', 'header',
                                            'footer', 'a', 'select', 'video','videolist','videoitem', 'ul', 'nav') or
                        parent_tag.has_attr('hidden') or
                        (footer or video or time or hide) or
                        (parent_tag.name == 'input' and parent_tag.get('type') == 'hidden') or
                        (comment or footer_id or feedback)):
                        hidden = True
                        break
                if hidden:
                    continue

                # remove any multiple and whitespace
                string = ' '.join(element.string.split())
                if string:
                    if element.parent.name == 'p':
                        # Add extra paragraph formatting newline
                        string = '\n' + string
                        #print(string)
                    text += [string]
        if soup.title.string is not None:
            doc = soup.title.string+' '.join(text)
        else:
            doc = ' '.join(text)
        #print(doc)
        return doc
    except Exception as e:
        print(e)
        return None

def getContentFromURL(url):
    try:
        html = requests.get(url).text
        doc = getContent(html)
        return doc
    except Exception as e:
        print(e)

def scrape500Pages(isAccident):
    if isAccident:
        pages_file = cf.ACCIDENT_PAGES_FILE
        data_folder = cf.ACCIDENT_DATA_FOLDER
    else:
        pages_file = cf.ORDINARY_PAGES_FILE
        data_folder = cf.ORDINARY_DATA_FOLDER
    
    pages = hp.readFileIntoList(pages_file)
    for page in pages:
        try:
            print('Getting content for page: ' + page)
            doc = getContentFromURL(page)
            print('Done getting content.')
            print('Extracting nouns from the content...')
            nouns = [word.lower() for word, tu_loai in pos_tag(doc) if tu_loai == 'N']
            
            fileName = data_folder + hp.makeFileName(page)
            print('Writing nouns into file:' + fileName)
            hp.writeListIntoFile(nouns, fileName)
            print('Writing nouns into file:' + cf.ALL_ACCIDENT_NOUNS_FILE)
            hp.writeListIntoFile(nouns, cf.ALL_ACCIDENT_NOUNS_FILE)
        except Exception as e:
            print(e)
            pass



if __name__ == '__main__':
    # get500AccidentPages()
    scrape500Pages(isAccident = True)
