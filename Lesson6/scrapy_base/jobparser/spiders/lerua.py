import scrapy
from scrapy.http import HtmlResponse
from Lesson6.scrapy_base.jobparser.items import LeruaparserItem


class LeruaSpider(scrapy.Spider):
    name = 'lerua'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, mark):
        self.start_urls = [f'https://voronezh.leroymerlin.ru/catalogue/dreli?06575={mark}']

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath('//div[@data-marker="item"]//a[@class="iva-item-sliderLink-bJ9Pv"]'
                                   '//@href').extract()
        for link in ads_links:
            yield response.follow('https://www.voronezh.leroymerlin.ru' + link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        name = response.xpath('//span[@class="title-info-title-text"]//text()').extract()
        photos = response.xpath('//div[contains(@class , "gallery-img-wrapper")]'
                                '//div[contains(@class, "gallery-img-frame")]/@data-url').extract()
        price = response.xpath('//span[@class="js-item-price"]//text()').getall()
        print(name[0])
        print(photos)

        yield LeruaparserItem(name=name, photos=photos, price=price)
