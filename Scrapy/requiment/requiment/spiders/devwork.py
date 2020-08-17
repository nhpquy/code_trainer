from scrapy import Spider

from ..items import RequimentItem
import scrapy


class CareerbuilderSpider(Spider):
    name = 'devwork'
    allowed_domains = ['devwork.vn']
    start_urls = [
        'https://devwork.vn/job/search?name-seach=&category-jod=0&location-jod=1&wage-job-from=&wage-job-to'
        '=&workingfrom_job=1&_token=4sCfy1EVjFElJayDIuzSBA139ENtPuoHmozjr9eB&page=23',
    ]

    def parse(self, response):
        all_job = response.xpath('//div[@class="job-list-content"]')

        for job in all_job:
            job_url = job.xpath('./h4/a/@href').extract_first()

            yield scrapy.Request(job_url, callback=self.parse_job)

            next_page_url = response.xpath('//li[@class="page-item"]/a/@href').extract_first()
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_job(self, response):
        item = RequimentItem()
        item['title'] = response.xpath('normalize-space(/html/body/section[1]/div/div/div/div[2]/h1/text())').extract()
        item['mo_ta'] = response.xpath('//div[@class="jod-detail-content-request col-md-12"]/text()').extract()
        if item['mo_ta'] is None:
            item['mo_ta'] = response.xpath(
                '//div[@class="jod-detail-content-request col-md-12"]/p/span/text()').extract()
        item['yeu_cau'] = response.xpath('/html/body/section[2]/div/div/div[1]/div[4]/div/text()').extract()
        if item['yeu_cau'] is None:
            item['yeu_cau'] = response.xpath('/html/body/section[2]/div/div/div[1]/div[4]/div/p/span/text()').extract()

        yield item
