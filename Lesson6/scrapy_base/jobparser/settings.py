SPIDER_MODULES = ['Lesson6.scrapy_base.jobparser.spiders']
NEWSPIDER_MODULE = 'Lesson6.scrapy_base.jobparser.spiders'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/94.0.4606.71 Safari/537.36'
ROBOTSTXT_OBEY = False
LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'  #INFO ERROR
LOG_FILE = 'log.txt'
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 3
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 8
IMAGES_STORE = 'images'
ITEM_PIPELINES = {
   'Lesson6.scrapy_base.jobparser.pipeline.DataBasePipeline': 300,
   'Lesson6.scrapy_base.jobparser.pipeline.LeruaPhotosPipeline': 200,
}

