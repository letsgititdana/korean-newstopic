import sys
import requests
import argparse
import datetime
from bs4 import BeautifulSoup as bs

"""
Python script to obtain list of valid Daum news URLs
encoding : UTF-8
"""

parser = argparse.ArgumentParser(description='Script to generate valid list of article URLs')
parser.add_argument('category', help='Category of articles whose URLs are to be scraped')
parser.add_argument('start', help='Initial date of publishment')
parser.add_argument('end', help='Final date of publishment')
args = parser.parse_args()

paper_publishers = ['한국일보','문화일보','동아일보','서울신문','세계일보','경향신문','국민일보','중앙일보','한겨레','조선일보']
valid_categories = ('politics', 'society', 'economic', 'culture', 'entertain', 'digital', 'editorial')


def make_pageurl(category, pagenum, date):
    """
    Function to return formatted URL given category, page number, date
    """
    if category not in valid_categories:
        raise ValueError("category has to be one of ('politics', 'society', 'economic', 'culture', 'entertain', 'digital', 'editorial')")
    assert len(str(date)) == 8, 'Invalid input date format'
    return f"https://news.daum.net/breakingnews/{category}?page={pagenum}&regDate={date}"


def date_formatting(date):
    """
    convert datetime.date object into yyyymmdd format string
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


if __name__ == '__main__':

    urllist = []
    category = args.category
    start = args.start
    end = args.end
    datelist = get_datelist(start, end)
    print(f'>>> Articles of category ({category}) ranges from {start[:4]}-{start[4:6]}-{start[6:]} to {end[:4]}-{end[4:6]}-{end[6:]} are being processed')

    for date in datelist:
        pagenum = 1
        
        while True:
            response = requests.get(make_pageurl(category, pagenum, date))
            parsed = bs(response.text, 'html.parser')
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
        
        sys.stdout.write('\r')
        sys.stdout.write(f'>>> Successfully scraped valid URLs of {date[:4]}-{date[4:6]}-{date[6:]}')
        sys.stdout.flush()

    print('\n')
    with open('./urllist.txt', 'w') as f:
        for url in urllist:
            f.write(url + '\n')