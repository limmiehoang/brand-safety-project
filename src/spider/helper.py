import spider_config as cf

from urllib.parse   import quote

def readFileIntoList(fileName):
    lines = []
    try:
        with open(fileName, 'r') as f:
            for line in f:
                lines.append(line.strip())
            f.close()
    except Exception as e:
        print(e)
    return lines

def writeListIntoFile(theList, fileName):
    try:
        with open(fileName, 'a') as f:
            for each in theList:
                f.write(each + '\n')
            f.close()
    except Exception as e:
        print(e)

def makeSearchURL(keyword, first):
    return cf.BING_SEARCH_URL + quote(keyword) + '&first=' + str(first)

def makeFileName(url):
    try:
        fileName = url.split('//')[1]
        fileName = fileName.replace('/', '_')
        fileName = fileName.replace('.', '_')
        return 'content_' + fileName + '.txt'
    except Exception as e:
        print(e)
        return None

if __name__ == '__main__':
    # keywords = readFileIntoList(cf.ACCIDENT_KEYWORDS_FILE)
    # writeListIntoFile(keywords, 'test.txt')
    fileName = makeFileName('https://m.thanhnien.vn/thoi-su/bat-giu-tai-xe-gay-tai-nan-chet-nguoi-roi-bo-chay-994992.html')
    print(fileName)