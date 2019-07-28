# -*- coding: utf-8 -*-

# Scrapy settings for etsy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'etsy'

SPIDER_MODULES = ['etsy.spiders']
NEWSPIDER_MODULE = 'etsy.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'etsy (+http://www.yourdomain.com)'

FEED_FORMAT= 'csv'
FEED_URI= 'output.csv'
LOG_LEVEL = 'ERROR'

FEED_EXPORTERS = {
    'csv': 'etsy.feedexport.CSVkwItemExporter'
}

#DOWNLOADER_MIDDLEWARES = {
#'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
#'scrapetest.middlewares.ProxyMiddleware': 100
#}

# By specifying the fields to export, the CSV export honors the order
# rath'er than using a random order.
EXPORT_FIELDS = [
    'seller_name',
    'seller_location',
    'seller_join_date',
    'number_of_sales',
    'number_of_admirers',
    'number_of_reviews',
    'average_review_score',
    'date_of_last_review_left',
    'number_of_items'
]