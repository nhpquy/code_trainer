from scrapy import Spider
from scrapy.selector import Selector

from ..items import SampleItem


class SampleSpider(Spider):
    name = "sample"
    allowed_domains = ["itviec.com/"]
    start_urls = [
        "https://itviec.com/it-jobs/full-stack-software-engineer-lhv-software-2143",
    ]

    def parse(self, response):
        item = SampleItem()

        item['content'] = response.xpath('//div[@id="container"]').extract_first()
        yield item

        # for question in questions:
        #     item['title'] = question.xpath(
        #         'normalize-space(p/text())').extract()
        #     # item['url'] = question.xpath(
        #     #     'a[@class="question-hyperlink"]/@href').extract()[0]
        #     # tmp_data = {item['title'], item['url']}
        #     yield item