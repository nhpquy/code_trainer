from scrapy import Spider
from scrapy.selector import Selector

from ..items import RequimentItem
import scrapy


class StackSpider(Spider):
    name = 'careerlink'
    allowed_domains = ['careerlink.vn']
    start_urls = [
        'https://www.careerlink.vn/viec-lam/cntt-phan-mem/19?page=30',
    ]
    base_url = 'https://www.careerlink.vn/'

    def parse(self, response):
        all_job = response.xpath('//h2[@class="list-group-item-heading"]')

        for job in all_job:
            job_url = job.xpath('.//a/@href').extract_first()

            job_url = self.base_url + job_url
            yield scrapy.Request(job_url, callback=self.parse_job)
        next_page_partial_url = response.xpath('//ul[@class="pagination"]/li/a/@href').extract_first()
        next_page_url = self.base_url + next_page_partial_url
        yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_job(self, response):
        title = response.xpath('//span[@itemprop="title"]/text()').extract()
        mo_ta = response.xpath('//div[@itemprop="description"]/p/text()').extract()
        yeu_cau = response.xpath('normalize-space(//div[@itemprop="skills"]/p/text())').extract_first()

        yield {
            'title': title,
            'yeucau': yeu_cau,
            'mo_ta': mo_ta
        }
