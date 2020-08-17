import scrapy
from scrapy import Spider
from scrapy.selector import Selector

from ..items import RequimentItem


class StackTopSpider(scrapy.Spider):
    name = 'topcv'
    allowed_domains = ['topcv.vn']
    start_urls = [
        'https://www.topcv.vn/viec-lam/it-phan-mem-c10026.html?salary=0&exp=0&page=35',
    ]
    base_url = 'https://www.topcv.vn/'

    def parse(self, response):
        all_job = response.xpath('//h4[@class="job-title"]')

        for job in all_job:
            job_url = job.xpath('./a/@href').extract()

            yield scrapy.Request(job_url, callback=self.parse_job)

        next_page_partial_url = response.xpath('//ul[@class="pagination"]/li/a/@href').extract_first()

        next_page_url = next_page_partial_url
        yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_job(self, response):
        item = RequimentItem()
        item['title'] = response.xpath('//div[@class="box box-white"]//h1/text()').extract()
        item['ten_cong_ty'] = response.xpath('normalize-space(//div[@class="company-title"]//a/text())').extract_first()
        item['dia_chi'] = response.xpath('//div[@class="box box-white"]/div/div[1]/div/div[2]/div[2]/text()').extract()
        item['mo_ta'] = response.xpath('//div[@id="col-job-left"]/div[1]/p/text()').extract()
        item['yeu_cau'] = response.xpath('//div[@id="col-job-left"]/div[2]/p/text()').extract()

        yield item
