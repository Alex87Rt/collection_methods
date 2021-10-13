from lxml import html
import requests
from datetime import datetime


def news_mail():
    news = []

    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
    }

    keys = ('title', 'link', 'datetime')

    request = requests.get('https://news.mail.ru/', headers=headers)
    root = html.fromstring(request.text)

    news_links = root.xpath('''(.//div[@class =  "news-item o-media news-item_media news-item_main"]  |  
                                //div[@class =  "news-item__inner"])
                                /a[contains(@href, "news.mail.ru")]/@href''')

    news_text = root.xpath('''(//div[@class =  "news-item o-media news-item_media news-item_main"]//h3  |  
                               //div[@class =  "news-item__inner"]/a[contains(@href, "news.mail.ru")])
                               /text()''')

    for i in range(len(news_text)):
        news_text[i] = news_text[i].replace(u'\xa0', u' ')

    news_links_temp = []
    for item in news_links:
        item = item.split('/')
        news_links_temp.append('/'.join(item[0:6]))

    news_links = news_links_temp
    news_datetime = []

    for items in news_links:
        request = requests.get(items, headers=headers)
        root = html.fromstring(request.text)
        date = root.xpath('//span[@class="note__text breadcrumbs__text js-ago"]/@datetime')
        news_datetime.extend(date)

    for i in range(len(news_datetime)):
        news_datetime[i] = datetime.strptime(news_datetime[i], '%Y-%m-%dT%H:%M:%S%z')

    for items in list(zip(news_text, news_links, news_datetime)):
        mail_dict = {}
        for key, value in zip(keys, items):
            mail_dict[key] = value

        mail_dict['source'] = 'news.mail.ru'
        news.append(mail_dict)

    return news

news_mail()
