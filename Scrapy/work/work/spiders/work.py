import string
import scrapy
from scrapy import Request
from scrapy.selector import Selector

from ..items import WorkItem


class MangaBaseSpider(scrapy.Spider):
    name = "work"
    allowed_domains = ["itviec.com"]
    start_urls = ['https://itviec.com/it-jobs/ho-chi-minh-hcm']
    BASE_URL = 'https://itviec.com/it-jobs/'

    def parse(self, response):
        links = response.xpath('//div[@class="first-group"]//h2/a/@href').extreact()
        yield links
    #     for link in links:
    #         absolute_url = self.BASE_URL + link
    #         yield scrapy.Request(absolute_url, callback=self.par)
    #
    # def par(self, response):
    #     item = WorkItem()
    #     item["link"] = response.url
    #     item["attr"] = "".join(response.xpath("//p[@class='experience']//text()").extract())
    #     return item
        # return (Request(url, callback=self.parse_manga_list_page) for url in response.xpath(xp).extract())

    # def parse_manga_list_page(self, response):
    #     for tr_sel in response.css('div.job-requirements mobile-box'):
    #         yield {
    #             "title": tr_sel.css('div.requirements::text').extract_first().strip(),
    #
    #         }
        # next_urls = response.xpath("//div[@class='spaceit']//a/@href").extract()
        # for next_url in next_urls:
        #     yield Request(response.urljoin(next_url), callback=self.parse_anime_list_page)
