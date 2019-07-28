# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EtsyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    seller_name = scrapy.Field()
    seller_location = scrapy.Field()
    seller_join_date = scrapy.Field()
    number_of_sales = scrapy.Field()
    number_of_admirers = scrapy.Field()
    number_of_reviews = scrapy.Field()
    average_review_score = scrapy.Field()
    date_of_last_review_left = scrapy.Field()
    number_of_items = scrapy.Field()
