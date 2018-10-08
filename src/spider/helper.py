import spider.spider_config as cf
import glob
import csv
import re
import operator
import os

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
    if mode == 'w':
        exists = os.path.isfile(fileName)
        if exists:
            os.rename(fileName, fileName + '.bk')

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
    exists = os.path.isfile(csvFile)
    if exists:
        os.rename(csvFile, csvFile + '.bk')
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
    pass