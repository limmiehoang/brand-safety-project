# path configuration
DATA_PATH = 'data/'
BING_SEARCH_URL = 'https://www.bing.com/search?q={}&format=rss&&first={}'
ACCIDENT_KEYWORDS_FILE = DATA_PATH + '50_accident_keywords.txt'
ORDINARY_KEYWORDS_FILE = DATA_PATH + '50_ordinary_keywords.txt'
ACCIDENT_PAGES_FILE = DATA_PATH + '500_accident_pages.txt'
ORDINARY_PAGES_FILE = DATA_PATH + '500_ordinary_pages.txt'
ACCIDENT_DATA_FOLDER = DATA_PATH + 'accident_data/'
ORDINARY_DATA_FOLDER = DATA_PATH + 'ordinary_data/'
ALL_ACCIDENT_NOUNS_FILE = ACCIDENT_DATA_FOLDER + 'all_accident_nouns.txt'
ALL_ORDINARY_NOUNS_FILE = ORDINARY_DATA_FOLDER + 'all_ordinary_nouns.txt'
MOST_COMMON_3000_ACCIDENT = ACCIDENT_DATA_FOLDER + '3000_most_common_accident_nouns.txt'
MOST_COMMON_3000_ORDINARY = ORDINARY_DATA_FOLDER + '3000_most_common_ordinary_nouns.txt'
ACCIDENT_READING_INDEX = ACCIDENT_DATA_FOLDER + 'reading_index.txt'
ORDINARY_READING_INDEX = ORDINARY_DATA_FOLDER + 'reading_index.txt'
DATASET = DATA_PATH + 'dataset.csv'

# constants
MAX_NOUNS = 3000