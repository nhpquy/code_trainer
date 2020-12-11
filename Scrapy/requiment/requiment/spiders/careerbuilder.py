from scrapy import Spider
from scrapy.selector import Selector

from ..items import RequimentItem
import scrapy


class StackSpider(Spider):
    name = 'career'
    allowed_domains = ['careerbuilder.vn']
    start_urls = [
        'https://careerbuilder.vn/viec-lam/cntt-phan-mem-c1-sortdv-r50-trang-1-vi.html',
    ]
    base_url = 'https://careerbuilder.vn/'

    def parse(self, response):
        all_job = response.xpath('//h3[@class="job"]')

        for job in all_job:
            job_url = job.xpath('//a/@href').extract_first()

            # job_url = self.base_url + job_url
            yield {
                'item': job_url
            }
            yield scrapy.Request(job_url, callback=self.parse_job)
        next_page_partial_url = response.xpath('//div[@class="clr"]/a/@href').extract_first()

    def parse(self, response):
        item = RequimentItem()
        item['title'] = response.xpath('/html/body/main/section[2]/div/div/div[1]/section/div[2]/div[1]/p/text()').extract()
        item['mo_ta'] = response.xpath('//h3[@class="detail-title"]/text()').extract()
        item['yeu_cau'] = response.xpath('/html/body/div[2]/div[3]/div[5]/div[2]/div/div[2]/text()').extract()

        yield item
