from scrapy import Spider
from scrapy.selector import Selector

from ..items import RequimentItem
import scrapy

class StackSpider(Spider):
    name = 'indeed'
    allowed_domains = ['indeed.com']
    start_urls = [
        'https://vn.indeed.com/jobs?q=IT',
    ]
    base_url = 'https://vn.indeed.com/'

    def parse(self, response):
        all_job = response.xpath('//h2[@class="list-group-item-heading"]')

        for job in all_job:
            job_url = job.xpath('.//a/@href').extract_first()

            job_url = self.base_url + job_url

            yield scrapy.Request(job_url, callback=self.parse_job)

    def parse(self, response):
        item = RequimentItem()
        item['title'] = response.xpath('/html/body/div[1]/div[2]/div[3]/div/div/div[1]/div[1]/div[1]/h3/text()').extract()
        item['mo_ta'] = response.xpath('/html/body/div[1]/div[2]/div[3]/div/div/div[1]/div[1]/div[3]/div/ul[1]/li[1]/text()').extract()
        item['yeu_cau'] = response.xpath('//div[@itemprop="skills"]/p/text()').extract()

        yield item