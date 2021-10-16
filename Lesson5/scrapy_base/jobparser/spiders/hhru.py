# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from Lesson5.scrapy_base.jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://voronezh.hh.ru/search/vacancy?area=&st=searchVacancy&text=python']

    def parse(self, response: HtmlResponse, **kwargs):
        next_page = 'https://voronezh.hh.ru' \
                    + response.css('a[class="bloko-button"][data-qa="pager-next"]').attrib['href']

        print(next_page)

        response.follow(next_page, callback=self.parse)

        vacansy = response.css(
            'div.vacancy-serp '
            'div.vacancy-serp-item '
            'div.vacancy-serp-item__row_header '
            'a.bloko-link::attr(href)'
        ).extract()

        for link in vacansy:
            yield response.follow(link, callback=self.vacansy_parse)

        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.css('h1[data-qa="vacancy-title"]::text').getall()
        salary = [
            response.css(
                'span[itemprop="baseSalary"] meta[itemprop="minValue"] ::attr(content)'
            ).extract_first(),
            response.css(
                'span[itemprop="baseSalary"] meta[itemprop="maxValue"] ::attr(content)'
            ).extract_first(),

            response.css(
                'span[itemprop="baseSalary"] meta[itemprop="currency"] ::attr(content)'
            ).extract_first()
        ]

        link = response.url
        site_scraping = self.allowed_domains[0]

        print('\nНазвание вакансии: ', name[0])
        print('Зарплата: ', salary)

        yield JobparserItem(name=name,
                            salary=salary,
                            vacancy_link=link,
                            site_scraping=site_scraping
                            )
