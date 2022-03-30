import requests
from bs4 import BeautifulSoup

def getNewsList(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    news_url_list = []
    for news_tag in soup.select('.entry-title'):
        news_url = news_tag.a.get('href')
        #print("news_url ==> ", news_url)
        news_url_list.append(news_url)
    return news_url_list


def getNewsContent(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    title_tag = soup.select_one('.entry-title')
    author_tag = soup.select('.body')[0]
    datetime_tag = soup.select('.body')[1]
    article_type_tag = soup.select('.body')[2]
    article_content_tag = soup.select_one('.indent')
    article = {
        'url': res.url,
        'title': title_tag.text.strip(),
        'author': author_tag.text.strip(),
        'datetime': datetime_tag.text.strip(),
        'article_type': article_type_tag.text.strip(),
        'article_content': article_content_tag.text.strip(),
    }
    return article