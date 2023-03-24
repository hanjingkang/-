# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QaItem(scrapy.Item):
    big_category = scrapy.Field()
    big_category_link = scrapy.Field()
    small_category = scrapy.Field()
    small_category_link = scrapy.Field()
    book_name = scrapy.Field()
    book_price = scrapy.Field()
    book_author = scrapy.Field()

    pass
