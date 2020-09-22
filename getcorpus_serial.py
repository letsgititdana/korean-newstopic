import os, sys, requests, argparse, datetime, re, time
from collections import Counter, defaultdict
from bs4 import BeautifulSoup
from konlpy.tag import Mecab


"""
Python script to generate sparse 2-dimensional data of words by article
encoding : UTF-8
"""


parser = argparse.ArgumentParser(description='Script to generate sparse article * words data')
parser.add_argument('geturllist', 
                    choices=['y','n'],
                    help="Whether to scrape list of valid URLS prior to word extraction. Set as 'y' for the first execution")
parser.add_argument('-c', '--category', metavar='', 
                    choices=['politics', 'society', 'economic', 'culture', 'entertain', 'digital', 'editorial'],
                    help='Category of articles whose URLs are to be scraped')
parser.add_argument('-s', '--start-date',  metavar='', help='Initial date of publishment')
parser.add_argument('-e', '--end-date',  metavar='', help='Final date of publishment')
args = parser.parse_args()

paper_publishers = ['한국일보','문화일보','동아일보','서울신문','세계일보','경향신문','국민일보','중앙일보','한겨레','조선일보']


def pageurl_template(category, pagenum, date):
    """
    Function to return formatted URL given category, page number, date
    """
    assert len(str(date)) == 8, 'Invalid input date format'
    return f"https://news.daum.net/breakingnews/{category}?page={pagenum}&regDate={date}"


def date_formatting(date):
    """
    Convert datetime.date object into yyyymmdd format string
    """
    year = str(date.year)
    month = str(date.month).rjust(2, '0')
    day = str(date.day).rjust(2, '0')
    return year + month + day


def get_datelist(start, end):
    """
    Given start, end date in yyyymmdd format, obtain list of dates(yyyymmdd) in between
    """
    assert len(start) == 8, 'start date not in proper format: yyyymmdd'
    assert len(end) == 8, 'end date not in proper format: yyyymmdd'
    
    start_list = [start[:4], start[4:6], start[6:]]
    end_list = [end[:4], end[4:6], end[6:]]
    
    start_date = datetime.date(*list(map(int, start_list)))
    end_date = datetime.date(*list(map(int, end_list)))
    delta = (end_date - start_date).days
    assert delta >= 0, 'start date must precede end date'
    
    date_list = [start_date + datetime.timedelta(d) for d in range(delta+1)]
    return list(map(date_formatting, date_list))


def get_validurl(date):
    """
    Get list of valid URL of articles that corresponds to certain input date
    """
    pagenum = 1
    urllist = []

    while True:
        response = requests.get(pageurl_template(category, pagenum, date))
        parsed = BeautifulSoup(response.text, 'html.parser')
        body = parsed.find('div', attrs={'class':'box_etc'})

        if body.select('p.txt_none'):
            break
        else:
            articles = body.select('div.cont_thumb')
            for tag in articles:
                publisher = tag.find('span', attrs={'class':'info_news'}).get_text().split()[0]
                if publisher in paper_publishers:
                    urllist.append(tag.find('a', attrs={'class':'link_txt'})['href'])
            pagenum += 1
        
    return urllist


def extract_nouns(url):
    """
    Extract nouns from the body text of article that corresponds to input URL using konlpy.Mecab
    """
    response = requests.get(url)
    parsed = BeautifulSoup(response.text, 'html.parser')
    body = parsed.find('div', attrs={'class':'news_view'})
    text_tags = body.find_all('p', attrs={'dmcf-ptype':'general'})
    text = ' '.join([tag.get_text().strip() 
                    for tag in text_tags 
                    if '@' not in tag.get_text() and len(tag.get_text()) > 8])

    pattern = re.compile("[\[(].{1,20}[\])]")
    nouns = [word 
            for word in mecab.nouns(pattern.sub('', text)) 
            if len(word) > 1]

    return nouns


if __name__ == '__main__':

    DIR_HOME = './dirs'
    if not os.path.exists('./dirs'):
        os.mkdir(DIR_HOME)
    category = args.category
    start = args.start_date
    end = args.end_date
    DIR_NAME = os.path.join(DIR_HOME, f"{category}-{start}-{end}")
    time_started = time.time()


    if args.geturllist == 'y':
        
        if not os.path.exists(DIR_NAME):
            os.mkdir(DIR_NAME)
        datelist = get_datelist(start, end)
        assert category, 'Category of articles is not specified'
        print(f"Saving valid URLs into urllist: {category}, from {start[:4]}-{start[4:6]}-{start[6:]} to {end[:4]}-{end[4:6]}-{end[6:]}")

        urllist = []
        for date in datelist:
            urllist += get_validurl(date)
            
            sys.stdout.write('\r')
            sys.stdout.write(f'>>> Successfully scraped valid URLs of {date[:4]}-{date[4:6]}-{date[6:]}')
            sys.stdout.flush()

        print('\n')
        with open(os.path.join(DIR_NAME, 'urllist.txt'), 'w') as f:
            for url in urllist:
                f.write(url + '\n')


    print("Extracting words from articles in the urllist")

    with open(os.path.join(DIR_NAME, 'urllist.txt'), 'r') as f:
        urls = f.read()

    urllist = urls.split()
    article2idx = defaultdict(lambda: len(article2idx))
    word2idx = defaultdict(lambda: len(word2idx))
    mecab = Mecab()
    corpus = []
    n_url = len(urllist)

    for idx, url in enumerate(urllist, 1):
        corpus += extract_nouns(url)
        
        sys.stdout.write('\r')
        sys.stdout.write(f">>> progress : [{('='*(int(idx/n_url*100) // 5)).ljust(20)}]")
        sys.stdout.flush()
        
    print('\n')
    minutes, seconds = list(map(int, divmod(time.time() - time_started, 60)))
    print(f">>> Corpus of articles is saved as {DIR_NAME + '/corpus'}")
    print(f">>> Total elapsed time : {str(minutes).rjust(3)}m {str(seconds).rjust(2,'0')}s")