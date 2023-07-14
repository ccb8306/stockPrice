import requests
import db_util
from bs4 import BeautifulSoup
import json
import config_util

host = config_util.getConfig('news_scraping', 'list_host')   # host
url = config_util.getConfig('news_scraping', 'list_url')     # 상세 url
parameters = '?callback=Search.SearchPreCallback&ctype=A&div_code=02%2003%2C04&page_size=10&channel=basic_kr'       # 파라미터

# 헤더
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}

news_insert_query = ("INSERT INTO news (news_category, news_title, news_contents, news_writer, news_write_date, regi_date, last_modi_date)"
                    "VALUES (%s, %s, %s, %s, %s, NOW(), NOW())")


def getNewsData(keyword, maxPage = 10) :
    # 헤더에 넣을 세션(쿠키) 생성
    #req = requests.Session()
        
    for page in range(maxPage) :
        current_page = page + 1

        # url 
        fullUrl = host + url + parameters + '&page_no=' + str(current_page) + '&query=' + keyword

        print('scraping.... : ' + fullUrl)
        
        response = requests.get(fullUrl, headers=headers)

        result = response.text
        json_str = result[result.find('{'):result.rfind('}')+1]
        parsed_data = json.loads(json_str)

        newsList = parsed_data['KR_ARTICLE']['result']

        for newsDt in newsList :  
            # 뉴스 상세
            newsId = newsDt['CONTENTS_ID']
            view_host = config_util.getConfig('news_scraping', 'view_host')
            view_url = config_util.getConfig('news_scraping', 'view_url')
            newsViewLink = view_host + view_url + '/' + newsId + '?section=search'

            print('newsViewLink.... : ' + newsViewLink)

            viewResponse = requests.get(newsViewLink, headers)
            viewResult = BeautifulSoup(viewResponse.text, 'html.parser')

            newsView = viewResult.select_one('#articleWrap')

            news_category = None
            news_title = None
            news_contents = None
            news_writer = None
            news_write_date = None

            # category
            select_target = 'div.news_ttl_wrap span.cate'
            if newsView.select_one(select_target) is not None : news_category = newsView.select_one(select_target).text 
            else: news_category = keyword

            # title
            select_target = '.title-article01 h1.tit'
            if newsView.select_one(select_target) is not None : news_title = newsView.select_one(select_target).text
            else: news_title = None

            print('news_title.... : ' + news_title)

            # contents
            select_target = 'div.content01 > div.scroller-wrap01 > div.scroller01 > .story-news'
            if newsView.select_one(select_target) is not None : news_contents = newsView.select_one(select_target).text
            else: news_contents = None

            # wirter
            select_target = 'div.news_write_info_group dl.author a'
            if newsView.select_one(select_target) is not None : news_writer = newsView.select_one(select_target).text
            else: news_writer = None

            # write date
            select_target = '#newsUpdateTime01'
            remove_target = newsView.select_one(select_target + ' > span.txt')
            if newsView.select_one(select_target) is not None : news_write_date = newsView.select_one(select_target).text.replace(remove_target.text, '').strip()
            else: news_write_date = None
            
            
            news_insert_param = (news_category, news_title, news_contents, news_writer, news_write_date)

            db_util.excuteQuery(news_insert_query, news_insert_param)

