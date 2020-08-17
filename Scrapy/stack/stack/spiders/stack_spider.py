import scrapy
from scrapy import Request


class StackSpider(scrapy.Spider):
    name = "stack"
    allowed_domains = ["https://itviec.com"]
    start_urls = [
        'https://itviec.com',
    ]

    def parse(self, response):
        xp = "//div[@class='page-header__tag-list hidden-xs']/a/@href"
        return (Request(url, callback=self.parse_manga_list_page) for url in response.xpath(xp).extract())

    def parse_manga_list_page(self, response):
        for tr_sel in response.css('div.first-group'):
            yield {
                "title": tr_sel.css('div.description hidden-xs::text').extract_first(),
                # "synopsis": tr_sel.css("div.pt4::text").extract_first(),
                # "type_": tr_sel.css('td:nth-child(3)::text').extract_first().strip(),
                # "episodes": tr_sel.css('td:nth-child(4)::text').extract_first().strip(),
                # "rating": tr_sel.css('td:nth-child(5)::text').extract_first().strip(),
            }
