import spider_config as cf
import glob
import csv
import re
import operator

from urllib.parse   import quote

def readFileIntoList(fileName):
    lines = []
    try:
        with open(fileName, 'r') as f:
            for line in f:
                lines.append(line.strip())
            f.close()
    except Exception as e:
        raise
    return lines

def writeListIntoFile(theList, fileName, mode):
    try:
        with open(fileName, mode) as f:
            for each in theList:
                f.write(each + '\n')
            f.close()
    except Exception as e:
        print(e)

def makeSearchURL(keyword, first):
    return cf.BING_SEARCH_URL.format(quote(keyword), first)

def makeFileName(url):
    try:
        fileName = url.split('//')[1]
        fileName = fileName.replace('/', '_')
        fileName = fileName.replace('.', '_')
        return 'content_' + fileName + '.txt'
    except Exception as e:
        print(e)
        return None

def listToDict(wordList):
    res = {}
    for word in wordList:
        if word in res:
            res[word] = res[word] + 1
        else:
            res[word] = 1
    return res

def most_common(D, max):
    sorted_x = sorted(D.items(), key=operator.itemgetter(1))[::-1]
    keys = []
    values = []
    for key, value in sorted_x[:max]:
        keys.append(key)
        values.append(value)
    return keys, values

def getFilesInDir(commonPath):
    files = []
    for file in glob.glob(commonPath):
        files.append(file)
    return files

def writeHeaderCSV(csvFile, fieldNames):
    with open(csvFile, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldNames)
        writer.writeheader()
        f.close()

def writeCSV(csvFile, row_dict, fieldNames):
    with open(csvFile, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldNames)
        writer.writerow(row_dict)

def readFileIntoDict(fileName):
    res = {}
    try:
        with open(fileName, 'r') as f:
            for line in f:
                lines.append(line.strip())
            f.close()
    except Exception as e:
        print(e)
    return res

def writeDictIntoFile(dict: {}, file_name: str, index: int):
    location = "output/content_{}.txt".format(index)
    output_file = open(location, "w")
    output_file.write(file_name)
    for pair in dict:
        try:
            line = "{} {}\n".format(pair, dict[pair])
            output_file.write(line)
        except:
            print("error")
    output_file.close()

distracted_words = ['tag', 'video', 'doisongphapluat', 'nghean', 'tinmoi']

def isValidLink(input_link: str) -> bool:
    if input_link[-1:] == '/':
        return False
    if len(input_link) < 80:
        return False
    if input_link[-5:].find(".") < 0:
        return False
    for word in distracted_words:
        if input_link.find(word) >= 0:
            return False
    return True

def isValidWord(word):
    regex = '^[^0-9`~,.!%<>;\':"/[\]|{}()=_+-]*$'
    prog = re.compile(regex)
    if not prog.match(word):
        return False

    parts = word.split()
    for part in parts:
        if len(part) > 7:
            return False

    if len(word) < 2:
        return False

    return True

if __name__ == '__main__':
    # keywords = readFileIntoList(cf.ACCIDENT_KEYWORDS_FILE)
    # writeListIntoFile(keywords, 'test.txt')
    # fileName = makeFileName('https://m.thanhnien.vn/thoi-su/bat-giu-tai-xe-gay-tai-nan-chet-nguoi-roi-bo-chay-994992.html')
    # print(fileName)

    # files = getFilesInDir(cf.ACCIDENT_DATA_FOLDER + 'content_*.txt')
    # print(files)

    # fieldNames = ['firstname', 'lastname']
    # writeHeaderCSV('test.csv', fieldNames)
    # d1 = {'lastname': 'truong', 'firstname': 'ngu'}
    # d2 = {'firstname': 'khanh', 'lastname': 'hoang'}
    
    # writeCSV('test.csv', d1, fieldNames)
    # writeCSV('test.csv', d2, fieldNames)

    url = makeSearchURL('xe', 1)
    print(url)