import scrapy
from scrapy import Spider

from ..items import RequimentItem


class ItviecSpider(scrapy.Spider):
    name = 'it'
    allowed_domains = ['itviec.com']
    start_urls = [
        'https://itviec.com/it-jobs',
    ]
    base_url = 'https://itviec.com'

    def parse(self, response):
        all_job = response.xpath('//h2[@class="title"]/a')

        for job in all_job:
            job_url = job.xpath('./@href').extract_first()
            job_urls = self.base_url + job_url
            yield scrapy.Request(job_urls, callback=self.parse_job)
        next_page_url = response.xpath('//div[@id="show_more"]/a/@href').extract()
        yield scrapy.Request(next_page_url, callback=self.parse)


    def parse_job(self, response):
        item = RequimentItem()
        item['title'] = response.xpath('normalize-space(//h1[@class="job_title"]/text())').extract()
        # item['ten_cong_ty'] = response.xpath('//h3[@class="name"]/a/text()').extract()
        # item['dia_chi'] = response.xpath('//div[@class="address__full-address"]/span/text()').extract()
        item['mo_ta'] = response.xpath('//div[@class="description"]//li/text()').extract()
        item['yeu_cau'] = response.xpath('//div[@class="experience"]//li/text()').extract()

        yield item
