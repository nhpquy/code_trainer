# -*- coding: utf-8 -*-
import scrapy


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['timviec365.vn']
    start_urls = ['https://timviec365.vn/viec-lam-it-phan-mem-c13v0',
                  'https://timviec365.vn/viec-lam-it-phan-mem-c13v0/page=2',
                  'https://timviec365.vn/viec-lam-it-phan-mem-c13v0/page=3',
                  'https://timviec365.vn/viec-lam-it-phan-mem-c13v0/page=4',
                  'https://timviec365.vn/viec-lam-it-phan-mem-c13v0/page=5',
                  'https://timviec365.vn/viec-lam-it-phan-mem-c13v0/page=6',
                  ]
    base_url = 'https://timviec365.vn/'

    def parse(self, response):
        all_job = response.xpath('//div[@class="item_cate"]')

        for job in all_job:
            job_url = job.xpath('.//a/@href').extract_first()

            job_url = self.base_url + job_url

            yield scrapy.Request(job_url, callback=self.parse_job)

        next_page_partial_url = response.xpath('//div[@class="clr"]/a/@href').extract_first()
        next_page_url = self.base_url + next_page_partial_url
        yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_job(self, response):
        title = response.xpath('normalize-space(//div[@class="right_tit"]/h1)').extract_first()
        mo_ta = response.xpath('//div[@class="box_mota"]/text()').extract()
        yeu_cau = response.xpath('//div[@class="box_yeucau"]/text()').extract()

        # stars = response.xpath(
        #     '//div/p[contains(@class, "star-rating")]/@class').extract_first().replace('star-rating ', '')
        # description = response.xpath(
        #     '//div[@id="product_description"]/following-sibling::p/text()').extract_first()
        # upc = response.xpath(
        #     '//table[@class="table table-striped"]/tr[1]/td/text()').extract_first()
        # price_excl_tax = response.xpath(
        #     '//table[@class="table table-striped"]/tr[3]/td/text()').extract_first()
        # price_inc_tax = response.xpath(
        #     '//table[@class="table table-striped"]/tr[4]/td/text()').extract_first()
        # tax = response.xpath(
        #     '//table[@class="table table-striped"]/tr[5]/td/text()').extract_first()
        # number_of_reviews = response.xpath(
        #     '//table[@class="table table-striped"]/tr[5]/td/text()').extract_first().replace('\u00a3', '')

        yield {
            'Title': title,
            'mo_ta': mo_ta,
            'yeu_cau': yeu_cau,
            # 'Image': final_image,
            # 'Price': price,
            # 'Stock': stock,
            # 'Stars': stars,
            # 'Description': description,
            # 'Upc': upc,
            # 'Price after tax': price_excl_tax,
            # 'Price incl tax': price_inc_tax,
            # 'Tax': tax,
            # 'Number of reviews': number_of_reviews,
        }