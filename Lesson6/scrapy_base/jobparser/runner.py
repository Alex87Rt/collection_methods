from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from Lesson6.scrapy_base.jobparser.spiders.lerua import LeruaSpider
from Lesson6.scrapy_base.jobparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeruaSpider, mark='bosch')
    process.start()
