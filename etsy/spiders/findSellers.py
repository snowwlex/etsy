# -*- coding: utf-8 -*-
import scrapy
from Helpers import Helpers
import re
from items import EtsyItem

class FindsellersSpider(scrapy.Spider):
    name = "findSellers"
    allowed_domains = ["etsy.com"]
    start_urls = (
        'https://www.etsy.com/search/shops',
    )

    def parse(self, response):
        shops = response.css("#shop-search > div > div.shop-info.v2 > div.shop-details > span > a::attr(href)").extract()
        for shop in shops:
            #print shop
            yield scrapy.Request(shop,self.parseShop)
            pass
        url = response.css("#pager-next::attr(href)").extract()[0]
        print url
        yield scrapy.Request(url=url, callback=self.parse)

    def parseShop(self,response):
        name_css = ["#before-sticky-nav > div > div > div.show-lg.show-xl.show-tv.shop-info.col-lg-7.pl-lg-3 > div.shop-name-and-title-container.mb-xs-2 > h1::text"]
        location_css = ["#before-sticky-nav > div > div > div.show-lg.show-xl.show-tv.shop-info.col-lg-7.pl-lg-3 > p > span.shop-location.mr-xs-2.pr-xs-2.br-xs-1::text"]
        from_date_css = ["#before-sticky-nav > div > div > div.show-lg.show-xl.show-tv.shop-info.col-lg-7.pl-lg-3 > p > span.etsy-since.no-wrap::text"]
        sales_css = ["#before-sticky-nav > div > div > div.show-lg.show-xl.show-tv.shop-info.col-lg-7.pl-lg-3 > p > span > a::text",
                      "#before-sticky-nav > div > div > div.show-lg.show-xl.show-tv.shop-info.col-lg-7.pl-lg-3 > p > span.mr-xs-2.pr-xs-2.br-xs-1:not([class^='shop-location'])::text"]
        favourites_css = ["#items > div > div > div.col-lg-3.hide-xs.hide-sm.hide-md.pl-xs-0 > div.mt-lg-5.pt-lg-2.bt-xs-1 > div:nth-child(2) > a::text"]
        reviews_css = ["#before-sticky-nav > div > div > div.show-xs.show-sm.show-md.col-xs-12.mt-xs-1 > div.star-rating-group.text-center > div > a > span::text"]
        avg_css = ["#reviews > div > div > div.col-lg-9.p-xs-0 > div.reviews-total > div > div:nth-child(2) > div > input[type='hidden']:nth-child(2)::attr(value)"]
        latest_review_css = ["#reviews > div > div > div.col-lg-9.p-xs-0 > div:nth-child(2) > div:nth-child(1) > div > div > div.flag-body.pb-xs-0 > div.mt-xs-2.mb-xs-2 > p"]

        name = Helpers.parse(response,name_css, response.request.url + " > No Name")
        location = Helpers.parse(response,location_css, response.request.url + " > No Location")
        from_date = Helpers.parse(response,from_date_css, response.request.url + " > No From Date")
        sales = Helpers.parse(response, sales_css, response.request.url + " > No Sales Info")
        favourites = Helpers.parse(response, favourites_css, response.request.url + " > No Favourites Info")
        reviews = Helpers.parse(response, reviews_css, response.request.url + " > No Reviews")
        avg_bunch = Helpers.parse(response, avg_css, response.request.url + " > No Average Review")

        pat = re.compile('[a-z]{3} [0-9]{1,2}, [0-9]{4}',re.IGNORECASE)
        latest_review = Helpers.parse(response, latest_review_css, response.request.url + " > No Latest Review")
        latest_review_regx = pat.search(latest_review)
        if latest_review_regx:
            latest_review_regx = latest_review_regx.group()
        else:
            latest_review_regx = response.request.url + " > No Latest Review"

        etsy = EtsyItem()

        etsy['seller_name'] = name
        etsy['seller_location'] = location
        etsy['seller_join_date'] = from_date
        etsy['number_of_sales'] = sales
        etsy['number_of_admirers'] = favourites
        etsy['number_of_reviews'] = reviews
        etsy['average_review_score'] = avg_bunch
        etsy['date_of_last_review_left'] = latest_review_regx

        yield etsy