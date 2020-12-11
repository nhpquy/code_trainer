# -*- coding: utf-8 -*-
import scrapy


class SpiderSpider(scrapy.Spider):
    name = 'nhanlucit'
    allowed_domains = ['nhanlucit.vn']
    start_urls = [
        'https://nhanlucit.vn/vieclam/page/45',
    ]

    def parse(self, response):
        all_job = response.xpath('//div[@class="jobs posts-loop "]//h2[@class="loop-item-title"]/a/@href').extract()
        for job in all_job:
            yield scrapy.Request(job, callback=self.parse_job)

        next_page_url = response.xpath('//div[@class="jobs posts-loop "]//a[@class="prev page-numbers"]/@href').extract_first()
        yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_job(self, response):
        title = response.xpath('normalize-space(//h1[@class="page-title"]/text())').extract_first()
        # ten_ct = response.xpath('//h3[@class="company-title"]/a/text()').extract()

        # dia_chi = response.xpath('//span[@class="job-location"]/a/em/text()').extract_first()
        kinh_nghiem = response.xpath('//div[@class="job-desc"]/ul[1]/li[3]/text()').extract()
        muc_luong = response.xpath('//div[@class="job-desc"]/ul[1]/li[4]/text()').extract()
        mo_ta = response.xpath('//div[@class="job-desc"]/ul[2]/li/text()').extract()
        yeu_cau = response.xpath('//div[@class="job-desc"]/ul[3]/li/text()').extract()

        yield {
            'Title': title,
            # 'ten_cong_ty': ten_ct,
            # 'dia_chi': dia_chi,
            'kinh_nghiem': kinh_nghiem,
            'muc_luong': muc_luong,
            'mo_ta': mo_ta,
            'yeu_cau': yeu_cau,
        }
