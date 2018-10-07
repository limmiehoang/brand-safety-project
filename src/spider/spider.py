#!/usr/bin/env python
# -*- coding: utf-8 -*-

import helper as hp
import spider_config as cf
import xml.etree.ElementTree as et
import requests
import operator

from urllib.request import urlopen, Request
from bs4            import BeautifulSoup, NavigableString, Tag
from underthesea    import pos_tag

def getLinksFromKeyword(keyword):
    links = []
    counter = 0
    first = 1
    while counter < 12:
        try:
            search_url = hp.makeSearchURL(keyword, first)
            rss = et.parse(urlopen(search_url)).getroot()
            temp = []
            for link in rss.iter('link'):
                link = link.text
                if hp.isValidLink(link):
                    temp.append(link)
                    counter += 1
                if counter == 12:
                    break
            links = links + temp
            first = first + 10
        except Exception as e:
            print(e)
    return links

def get500Pages(isAccident):
    if isAccident:
        keywords_file = cf.ACCIDENT_KEYWORDS_FILE
        pages_file = cf.ACCIDENT_PAGES_FILE
    else:
        keywords_file = cf.ORDINARY_KEYWORDS_FILE
        pages_file = cf.ORDINARY_PAGES_FILE
    pages = set()
    keywords = hp.readFileIntoList(keywords_file)
    for keyword in keywords:
        print('Getting pages for keyword: ' + keyword)
        links = getLinksFromKeyword(keyword)
        for link in links:
            pages.add(link)
    hp.writeListIntoFile(pages, pages_file)
    print('Wrote pages into file: ' + pages_file)


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

# ignored_tags = ['em', 'input', 'button', 'area', 'base', 'basefont', 'datalist', 'head', 'link',
#                 'meta', 'noembed', 'noframes', 'param', 'rp', 'script',
#                 'source', 'style', 'template', 'track', 'title', 'noscript', 'header',
#                 'footer', 'a', 'select', 'video','videolist','videoitem', 'ul', 'nav']

# def getContent(html):
#     content = BeautifulSoup(html, "html.parser")
#     for tag in ignored_tags:
#         for html_part in content.find_all(tag):
#             html_part.decompose()

#     text = content.text
#     text = text.lower()
#     text.replace("\n", " ")
#     return " ".join(text.split())

def getContentFromURL(url):
    try:
        req = Request(url, headers={'User-Agent': "Magic Browser"})
        f = urlopen(req)
        html = f.read().decode("utf-8", errors='ignore')
        f.close()
        
        html = requests.get(url).text
        doc = getContent(html)
        return doc
    except Exception as e:
        print(e)

def scrape500Pages(isAccident):
    if isAccident:
        pages_file = cf.ACCIDENT_PAGES_FILE
        data_folder = cf.ACCIDENT_DATA_FOLDER
        all_nouns_file = cf.ALL_ACCIDENT_NOUNS_FILE
        reading_index_file = cf.ACCIDENT_READING_INDEX
        
    else:
        pages_file = cf.ORDINARY_PAGES_FILE
        data_folder = cf.ORDINARY_DATA_FOLDER
        all_nouns_file = cf.ALL_ORDINARY_NOUNS_FILE
        reading_index_file = cf.ORDINARY_READING_INDEX
    
    try:
        reading_index = hp.readFileIntoList(reading_index_file)
        reading_index = int(reading_index[0])
    except:
        reading_index = 0
    
    pages = hp.readFileIntoList(pages_file)
    for page in pages[reading_index:]:
        try:
            reading_index += 1
            hp.writeListIntoFile([str(reading_index)], reading_index_file, 'w')
            print('Getting content for page: ' + page)
            doc = getContentFromURL(page)
            print('Extracting nouns from the content...')
            if ((doc is not None) and len(doc.strip()) > 0):
                nouns = [word.lower() for word, tu_loai in pos_tag(doc) if tu_loai == 'N' and hp.isValidWord(word)]
                fileName = data_folder + hp.makeFileName(page)
                print('Writing nouns into file:' + fileName)
                hp.writeListIntoFile(nouns, fileName, 'a')
                print('Writing nouns into file:' + all_nouns_file)
                hp.writeListIntoFile(nouns, all_nouns_file, 'a')
        except Exception as e:
            print(e)
            pass

def extractMostCommonNouns(isAccident, max):
    if isAccident:
        all_nouns_file = cf.ALL_ACCIDENT_NOUNS_FILE
        most_common_3000_nouns_file = cf.MOST_COMMON_3000_ACCIDENT
        print('---Extracting most common accident nouns---')
    else:
        all_nouns_file = cf.ALL_ORDINARY_NOUNS_FILE
        most_common_3000_nouns_file = cf.MOST_COMMON_3000_ORDINARY
        print('---Extracting most common ordinary nouns---')
    print('Reading file of all nouns into list...')
    nouns = hp.readFileIntoList(all_nouns_file)
    print('Making dictionary of word frequency...')
    d = hp.listToDict(nouns)
    words, frequencies = hp.most_common(d, max)
    hp.writeListIntoFile(words, most_common_3000_nouns_file, 'a')
    return words

def makeData():
    accident_nouns = extractMostCommonNouns(isAccident = True, max = cf.MAX_NOUNS)
    ordinary_nouns = extractMostCommonNouns(isAccident = False, max = cf.MAX_NOUNS)
    features = accident_nouns + ordinary_nouns
    label = ['isAccident']
    fieldNames = features + label
    hp.writeHeaderCSV(cf.DATASET, fieldNames)
    
    accident_files = hp.getFilesInDir(cf.ACCIDENT_DATA_FOLDER + 'content_*.txt')
    ordinary_files = hp.getFilesInDir(cf.ORDINARY_DATA_FOLDER + 'content_*.txt')
    for f in accident_files:
        try:
            words = hp.readFileIntoList(f)
            words = hp.listToDict(words)
            row_dict = {}
            for feature in features:
                if feature in words:
                    row_dict[feature] = words[feature]
                else:
                    row_dict[feature] = 0
            row_dict['isAccident'] = 1
            hp.writeCSV(cf.DATASET, row_dict, fieldNames)
        except Exception as e:
            print(e)
            pass
    for f in ordinary_files:
        try:
            words = hp.readFileIntoList(f)
            words = hp.listToDict(words)
            row_dict = {}
            for feature in features:
                if feature in words:
                    row_dict[feature] = words[feature]
                else:
                    row_dict[feature] = 0
            row_dict['isAccident'] = 0
            hp.writeCSV(cf.DATASET, row_dict, fieldNames)
        except Exception as e:
            print(e)
            pass

if __name__ == '__main__':
    # get500Pages(False)
    # get500Pages(True)
    scrape500Pages(isAccident = True)
    scrape500Pages(isAccident = False)
    # doc = getContentFromURL('https://news.zing.vn/tai-nan-lien-hoan-tren-quoc-lo-1-phu-nu-tu-vong-post867967.html')
    # print(doc)
    # print(type(doc))
    # print('pos tag')
    # pos_tag(doc)
    # print('done')
    # doc = getContentFromURL('https://news.zing.vn/tam-giu-tai-xe-xe-tai-lan-lan-dam-ba-bau-tu-vong-post845164.html')
    # print(doc)
    # print(type(doc))
    

