# -*- coding: utf-8 -*-
import scrapy
from etsy.spiders.Helpers import Helpers
import re
from etsy.items import EtsyItem


class FindsellersSpider(scrapy.Spider):
    name = "findSellers"
    allowed_domains = ["etsy.com"]
    start_urls = [
        'https://www.etsy.com/search/shops'
    ]

    def parse(self, response):
        shops = response.css("#shop-search div.shop")
        for shop in shops:
            shop_link = shop.css('div.shop-info.v2 > div.shop-details > span > a::attr(href)').extract()[0]
            shop_items = shop.css('.count-number::text').extract()[0]
            yield scrapy.Request(
                shop_link,
                callback=self.parseShop,
                cb_kwargs=dict(shop_items=shop_items)
            )
            pass
        next = response.css("#pager-next::attr(href)").extract()
        if next:
            url = next[0]
            print (url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parseShop(self,response, shop_items):
        name_css = ["div.content .shop-name-and-title-container > h1::text"]
        location_css = ["div.content .shop-location::text"]
        from_date_css = ["div.content .etsy-since::text"]
        sales_css = [
            "div.content .shop-sales > a::text",
            "div.content .shop-sales::text"
        ]
        reviews_css = ["div.content .star-rating-group .total-rating-count::text"]
        avg_css = ["div.content .star-rating-group .stars-svg > input[name='rating']::attr(value)"]
        # latest_review_css = ["#reviews > div > div > div.col-lg-9.p-xs-0 > div:nth-child(2) > div:nth-child(1) > div > div > div.flag-body.pb-xs-0 > div.mt-xs-2.mb-xs-2 > p"]

        name = Helpers.parse(response,name_css, "-")
        location = Helpers.parse(response,location_css, "-")
        from_date = Helpers.parse(response,from_date_css, "-")
        sales = Helpers.parse(response, sales_css, "-")
        # favourites = Helpers.parse(response, favourites_css, "-")
        reviews = Helpers.parse(response, reviews_css, "-")
        avg_bunch = Helpers.parse(response, avg_css, "-")

        # pat = re.compile('[a-z]{3} [0-9]{1,2}, [0-9]{4}',re.IGNORECASE)
        # latest_review = Helpers.parse(response, latest_review_css, response.request.url + " > No Latest Review")
        # latest_review_regx = pat.search(latest_review)
        # if latest_review_regx:
        #     latest_review_regx = latest_review_regx.group()
        # else:
        #     latest_review_regx = response.request.url + " > No Latest Review"

        etsy = EtsyItem()

        etsy['seller_name'] = name
        etsy['seller_location'] = location
        etsy['seller_join_date'] = from_date
        etsy['number_of_sales'] = sales
        # etsy['number_of_admirers'] = favourites
        etsy['number_of_reviews'] = reviews
        etsy['average_review_score'] = avg_bunch
        etsy['number_of_items'] = shop_items
        # etsy['date_of_last_review_left'] = latest_review_regx

        yield etsy