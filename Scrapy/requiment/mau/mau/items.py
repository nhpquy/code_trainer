# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MauItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    mo_ta = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    yeu_cau = scrapy.Field()
    url = scrapy.Field()

    pass
