import scrapy

class LeruaparserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    photos = scrapy.Field()
    price = scrapy.Field()
    pass
