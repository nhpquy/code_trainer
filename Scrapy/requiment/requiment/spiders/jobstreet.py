from scrapy import Spider
from scrapy.selector import Selector

from ..items import RequimentItem


class StackSpider(Spider):
    name = 'jobstreet'
    allowed_domains = ['jobstreet.vn']
    start_urls = [
        'https://www.jobstreet.vn/j?q=IT&l=&button=&sp=search',
    ]
    base_url = 'https://www.jobstreet.vn'

    def parse(self, response):
        all_job = response.xpath('//h2[@class="title"]/a')

        for job in all_job:
            job_url = job.xpath('./@href').extract_first()
            job_urls = self.base_url + job_url
            yield scrapy.Request(job_urls, callback=self.parse_job)
        next_page_url = response.xpath('//div[@id="show_more"]/a/@href').extract_first()
        yield scrapy.Request(next_page_url, callback=self.parse)

    def parse(self, response):
        item = RequimentItem()
        item['title'] = response.xpath('//div[@class="job-position-wrap"]/h1/text()').extract_first()
        item['mo_ta'] = response.xpath('//div[@id="job_description"]//li/text()').extract()
        item['yeu_cau'] = response.xpath('/html/body/section[3]/div/div[1]/div[1]/div/div/div/ul[2]/li/text()').extract()

        yield item