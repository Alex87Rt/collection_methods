# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from Lesson5.scrapy_base.jobparser.items import JobparserItem


class SuperjobruSpider(scrapy.Spider):
    name = 'superjob_ru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://voronezh.superjob.ru/vacancy/search/?keywords=Python']

    def parse(self, response: HtmlResponse, **kwargs):
        next_page = response.css('a.f-test-link-dalshe::attr(href)') \
        .extract_first()

        print(next_page)

        response.follow(next_page, callback=self.parse)

        vacancy  = response.css(
            'div.f-test-vacancy-item \
            a[class*=f-test-link][href^="/vakansii"]::attr(href)'
        ).extract()

        for link in vacancy:
            yield response.follow(link, self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.css('h1 ::text').extract()

        salary = response.css(
            'div._3MVeX span[class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"] ::text'
        ).extract()

        link = response.url
        site_scraping = self.allowed_domains[0]

        yield JobparserItem(
            name=name,
            salary=salary,
            vacancy_link=link,
            site_scraping=site_scraping
        )
