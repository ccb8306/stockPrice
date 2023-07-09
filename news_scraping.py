import requests
import db_util
from bs4 import BeautifulSoup


host = 'https://www.mk.co.kr/news/stock/'   # host
url = '/search'                 # 상세 url
parameters = '?word=삼성'       # 파라미터

# 헤더
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def getNewsData() :
    
    # 요청
    #fullUrl = host + url + parameters
    fullUrl = host
    response = requests.get(fullUrl, headers)
    result = BeautifulSoup(response.text, 'html.parser')

    # 파싱
    newsBody = result.select_one('section.news_sec.latest_news_sec')
    newsList = newsBody.select('ul.news_list > li.news_node:not(.ad_wrap)')

    news_insert_query = ("INSERT INTO news (news_category, news_title, news_contents, news_writer, news_write_date, regi_date, last_modi_date)"
                        "VALUES (%s, %s, %s, %s, %s, NOW(), NOW())")
    
    for newsDt in newsList :  
        print(newsDt)
        # 뉴스 상세
        newsViewLink = newsDt.select_one('a.news_item')['href']
        viewResponse = requests.get(newsViewLink, headers)
        viewResult = BeautifulSoup(viewResponse.text, 'html.parser')

        newsView = viewResult.select_one('section.contents')

        news_category = newsView.select_one('div.news_ttl_wrap span.cate').text
        news_title = newsView.select_one('div.news_ttl_wrap  h2.news_ttl').text
        news_contents = newsView.select_one('div.news_detail_body_group div.news_cnt_detail_wrap').text
        news_writer = newsView.select_one('div.news_write_info_group dl.author a').text
        news_write_date = newsView.select_one('div.news_write_info_group div.time_area dd').text

        news_insert_param = (news_category, news_title, news_contents, news_writer, news_write_date)

        db_util.excuteQuery(news_insert_query, news_insert_param)



