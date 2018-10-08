from spider.spider import get6000MostCommonNouns, scrape
from spider.helper import listToDict

def test_make_observation():
    features = get6000MostCommonNouns()
    nouns = scrape('https://vnexpress.net/tin-tuc/thoi-su/tp-hcm-xay-nha-hat-1-500-ty-tai-thu-thiem-vi-can-cho-nguoi-dan-3820751.html')
    nouns = listToDict(nouns)
    res = []
    for feature in features:
        if feature in nouns:
            res.append(nouns[feature])
        else:
            res.append(0)

    print(res)
    assert True