# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RequimentItem(scrapy.Item):
    mo_ta = scrapy.Field()
    yeu_cau = scrapy.Field()
    title = scrapy.Field()
    ten_cong_ty = scrapy.Field()
    pass
