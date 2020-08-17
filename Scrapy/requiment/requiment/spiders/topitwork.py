# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
script = """
function main(splash)
    splash:init_cookies(splash.args.cookies)
    local url = splash.args.url
    assert(splash:go(url))
    assert(splash:wait(5))
    return {
        cookies = splash:get_cookies(),
        html = splash:html()
    }
end
"""
script2 = """
function main(splash)
    splash:init_cookies(splash.args.cookies)
    local url = splash.args.url
    assert(splash:go(url))
    assert(splash:wait(0.5))r
    return {
        cookies = splash:get_cookies(),
        html = splash:html()
    }
end
"""
class TopITWork(scrapy.Spider):
    name = 'topitwork'
    allowed_domains = ['topitworks.com']
    start_urls = ['https://www.topitworks.com/vi/viec-lam?']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint="excute", args={'lua_source': script})

    def parse(self, response):
        # Get URL in page and yield Request
        url_selector = response.xpath('//h4[@class="hit-name"]/a/@href')
        for url in url_selector.extract():
            yield SplashRequest(url, callback=self.parse_job, endpoint='execute', args={'lua_source': script2})

        next_page_url = response.xpath('//div[@id="pagination"]/ul/li/a/@href').extract_first()
        yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_job(self, response):
        title = response.xpath('normalize-space(//h3[@class="job-name"]/text())').extract_first()
        ten_ct = response.xpath('//h4[@class="company-name hidden-xs"]/text()').extract()
        mo_ta = response.xpath(
            '//div[@class="read-more-panel-ex"]/div[@class="read-more-content mt1"]/text()').extract()
        yeu_cau = response.xpath(
            '//div[@class="read-more-panel-ex mt2"]/div[@class="read-more-content mt1"]/text()').extract()
        yield {
            'Title': title,
            'ten_cong_ty': ten_ct,
            'mo_ta': mo_ta,
            'yeu_cau': yeu_cau,
        }
