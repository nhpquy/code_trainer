import scrapy
from scrapy import Spider
from scrapy.selector import Selector

from ..items import RequimentItem


class StackSpider(Spider):
    name = 'mywork'
    allowed_domains = ['mywork.com.vn']
    start_urls = [
        'https://mywork.com.vn/tuyen-dung/trang/5?categories=38',
    ]
    base_url = 'https://mywork.com.vn'

    def parse(self, response):
        all_job = response.xpath('//section[@class="item"]')

        for job in all_job:
            job_url = job.xpath('//a/@href').extract_first()
            job_urls = self.base_url + job_url
            yield {
                'link': job_urls
            }
    #     yield scrapy.Request(job_urls, callback=self.parse_job)
        next_page_url = response.xpath('//ul[@class="pagination"]/li/a/@href').extract_first()
        yield scrapy.Request(next_page_url, callback=self.parse)
    #
    # def parse_job(self, response):
    #     item = RequimentItem()
    #     item['title'] = response.xpath('//h1[@class="main-title"]/span/text()').extract()
    #     item['ten_cong_ty'] = response.xpath('//h2[@class="desc-for-title mb-15"]/span/text()').extract()
    #     item['dia_chi'] = response.xpath('normalize-space(//span[@class="el-tag location_tag el-tag--primary"]/a/text())').extract()
    #     item['mo_ta'] = response.xpath('//div[@class="box multiple"]/div[3]/text()').extract()
    #     item['yeu_cau'] = response.xpath('//div[@class="box multiple"]/div[5]/text()').extract()
    #
    #     yield item