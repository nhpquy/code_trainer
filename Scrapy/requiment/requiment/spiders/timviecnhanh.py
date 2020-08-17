from scrapy import Spider
from scrapy.selector import Selector
import scrapy
from ..items import RequimentItem


class StackSpider(Spider):
    name = 'timviecnhanh'
    allowed_domains = ['timviecnhanh.com']
    start_urls = [
        'https://www.timviecnhanh.com/vieclam/timkiem?nganh_nghe[]=17&page=15',
    ]

    def parse(self, response):
        all_job = response.xpath('//td[@class="block-item w55"]')
        for job in all_job:
            job_url = job.xpath('.//a[1]/@href').extract_first()

            yield scrapy.Request(job_url, callback=self.parse_job)

        next_page_url = response.xpath('//div[@class="page-navi ajax"]/a/@href').extract_first()
        yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_job(self, response):
        item = RequimentItem()
        item['title'] = response.xpath('normalize-space(//header[@class="block-title"]//span/text())').extract_first()
        item['ten_cong_ty'] = response.xpath('normalize-space(//article[@class="block-content"]//h3/a/text())').extract()
        item['dia_chi'] = response.xpath('//article[@class="block-content"]//div[@class="col-xs-6 p-r-10 '
                                         'offset10"]//span/text()').extract_first()
        item['mo_ta'] = response.xpath('//article[@class="block-content"]//table/tbody/tr[1]/td[2]/p/text()').extract()
        item['yeu_cau'] = response.xpath('//article[@class="block-content"]//table/tbody/tr[2]/td[2]/p/text()').extract()

        yield item
