from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
import json
import re
import requests


class Job():

    def __init__(self, mongodb_uri, db_name, collection_name):
        self.headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                         ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
        }
        self.link_hh = 'https://voronezh.hh.ru/search/vacancy'
        self.mongodb = MongoClient(mongodb_uri)
        self.db = self.mongodb[db_name]
        self.collection = self.db[collection_name]

    def print_salary(self, salary):
        objects = self.collection.find({'salary_max': {'$gt': salary}})
        for obj in objects:
            print(obj)

    def search_job(self, vacancy):
        self.parser_hh(vacancy)

    def parser_hh(self, vacancy):
        params = {
            'text': vacancy,
            'search_field': 'name',
            'page': ''
        }

        html = self.get_html(self.link_hh, params)
        last_page = self.get_last_page_hh(html)
        for page in range(0, last_page):
            params['page'] = page
            html = self.get_html(self.link_hh, params)
            if html.ok:
                parsed_html = self.get_parsed_html(html)

                vacancy_items = parsed_html.find('div', {'data-qa': 'vacancy-serp__results'})\
                    .find_all('div', {'class': 'vacancy-serp-item'})
                for item in vacancy_items:
                    vacancy = self.parser_item_hh(item)

                    if self.is_exist('vacancy_link', vacancy['vacancy_link']):
                        self.collection.update_one({'vacancy_link': vacancy['vacancy_link']},
                                                   {'$set': vacancy})
                    else:
                        self.collection.insert_one(vacancy)


    def parser_item_hh(self, item):
        vacancy_data = {}

        vacancy_name = item.find('div', {'class': 'resume-search-item__name'}).getText().replace(u'\xa0', u' ')
        vacancy_data['vacancy_name'] = vacancy_name

        company_name = item.find('div', {'class': 'vacancy-serp-item__meta-info'}).getText().replace(u'\xa0', u' ')
        vacancy_data['company_name'] = company_name


        city = item.find('span', {'class': 'vacancy-serp-item__meta-info'}).getText().split(', ')[0]
        vacancy_data['city'] = city

        salary = item.find('div', {'class': 'vacancy-serp-item__compensation'})
        salary_min = None
        salary_max = None
        salary_currency = None

        if salary:
            salary = salary.getText().replace(u'\xa0', u'')
            salary = re.split(r'\s|-', salary)
            if salary[0] == 'до':
                salary_max = int(salary[1])
            elif salary[0] == 'от':
                salary_min = int(salary[1])
            else:
                salary_min = int(salary[0])
                salary_max = int(salary[1])

            salary_currency = salary[-1]
            salary_currency = self.get_name_currency(salary_currency)

        vacancy_data['salary_min'] = salary_min
        vacancy_data['salary_max'] = salary_max
        vacancy_data['salary_currency'] = salary_currency

        vacancy_json = json.loads(item.find('script',
                                            {'data-name': 'voronezh.hh.ru/search/'
                                                          'vacancy?text=&area=113&specialization=1.82&i'
                                                          'ndustry=7&search_field=description&search_field='
                                                          'company_name&search_field=name'})['data-params'])

        id = vacancy_json['vacancyId']

        vacancy_data['vacancy_link'] = f'https://voronezh.hh.ru/search/vacancy/{id}'
        vacancy_data['site'] = 'voronezh.hh.ru'
        return vacancy_data

    def get_last_page_hh(self, html):
        parsed_html = self.get_parsed_html(html)
        if parsed_html:
            page_block = parsed_html.find('div', {'data-qa': 'pager-block'})
            if not page_block:
                last_page = 1
            else:
                last_page = int(
                    page_block.find_all('a', {'class': 'HH-Pager-Control'})[-2].getText())

        return last_page


    def get_parsed_html(self, html):
        if html.ok:
            parsed_html = bs(html.text,'html.parser')
            return parsed_html

    def get_html(self, link, params=None):
        html = requests.get(link, params=params, headers=self.headers)
        return html

    def is_exist(self, name_tags, field):
        return bool(self.collection.find_one({name_tags: { "$in": [field]}}))

    def get_name_currency(self, currency_name):
        currency_dict  = {
            'EUR': {' €'},
            'RUB': {' ₽'},
            'USD': {' $'}
        }
        name = currency_name
        for item_name, items_list in currency_dict.items():
            if currency_name in items_list:
                name = item_name

        return name
