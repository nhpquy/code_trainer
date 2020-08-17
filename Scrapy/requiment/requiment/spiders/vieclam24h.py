import scrapy
from scrapy import Spider
from scrapy.selector import Selector

from ..items import RequimentItem


class StackSpider(scrapy.Spider):
    name = 'vieclam24h'
    allowed_domains = ['vieclam24h.vn']
    start_urls = [
        'https://vieclam24h.vn/mien-nam/viec-lam-chuyen-mon/it-phan-mem-c74.html',
    ]
    base_url = 'https://vieclam24h.vn'

    def parse(self, response):
        all_job = response.xpath('//div[@class="media-left"]/a')

        for job in all_job:
            job_url = job.xpath('./@href').extract()[0]
            job_url = self.base_url + job_url
            yield scrapy.Request(job_url, callback=self.parse_job)

    def parse_job(self, response):
        item = RequimentItem()
        item['title'] = response.xpath(
            '//div[@class="box_chi_tiet_cong_viec bg_white mt16 box_shadow"]//h1/text()').extract()
        item['ten_cong_ty'] = response.xpath('normalize-space(//div[@class="box_chi_tiet_cong_viec bg_white mt16 '
                                             'box_shadow"]//p/a/text())').extract()
        item['dia_chi'] = response.xpath('normalize-space(//div[@id="ttd_detail"]/div[2]/div[3]/p/text())').extract()
        item['mo_ta'] = response.xpath('//div[@id="ttd_detail"]//div[@class="pl_24 pr_24"]/div[1]/p/text()').extract()
        item['yeu_cau'] = response.xpath('//div[@id="ttd_detail"]//div[@class="pl_24 pr_24"]/div[3]/p/text()').extract()

        yield item
