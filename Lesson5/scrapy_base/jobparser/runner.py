from Lesson5.scrapy_base.jobparser.spiders.hhru import HhruSpider
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from Lesson5.scrapy_base.jobparser import settings

# from jobparser.spiders.hhru import SjruSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider, vacancy = 'Python')
    process.start()
