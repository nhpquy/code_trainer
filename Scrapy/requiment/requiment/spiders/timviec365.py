# -*- coding: utf-8 -*-
import scrapy

from ..items import RequimentItem


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['timviec365.vn']
    start_urls = [
        'https://timviec365.vn/viec-lam-it-phan-mem-c13v0/page=6',
    ]
    base_url = 'https://timviec365.vn/'

    def parse(self, response):
        # extract the csrf token value
        token = response.css('input[name="csrf_token"]::attr(value)').extract_first()
        # create form value
        data = {
            'csrf_token': token,
            'username': 'admin',
            'password': 'admin',
        }
        # Submit Post request login
        yield scrapy.FormRequest(url=self.login_url, formdata=data, callback=self.parse)

        all_job = response.xpath('//div[@class="item_cate"]')
        for job in all_job:
            job_url = job.xpath('.//a/@href').extract_first()

            job_url = self.base_url + job_url

            yield scrapy.Request(job_url, callback=self.parse_job)

        next_page_partial_url = response.xpath(
            '//div[@class="clr"]/a/@href').extract_first()

        next_page_url = self.base_url + next_page_partial_url
        yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_job(self, response):
        title = response.xpath('normalize-space(//div[@class="right_tit"]/h1)').extract_first()
        mo_ta = response.xpath('//div[@class="box_mota"]/text()').extract()
        yeu_cau = response.xpath('//div[@class="box_yeucau"]/text()').extract()
        ten_ct = response.xpath('//div[@class="box-cp"]/strong/text()').extract()
        dia_chi = response.xpath('//div[@class="box-cp"]/p[1]/text()').extract()

        item = RequimentItem()
        item['Title']: title
        item['mo_ta']: mo_ta
        item['yeu_cau']: yeu_cau
        item['ten_cong_ty']: ten_ct
        item['dia_chi']: dia_chi

        yield item

