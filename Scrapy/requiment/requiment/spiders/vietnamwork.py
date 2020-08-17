import scrapy
from lxml import html
from scrapy_splash import SplashRequest

# script = """
# function main(splash)
#     splash:init_cookies(splash.args.cookies)
#     local url = splash.args.url
#     assert(splash:go(url))
#     assert(splash:wait(5))
#     return {
#         cookies = splash:get_cookies(),
#         html = splash:html()
#     }
# end
# """
#
# script2 = """
# function main(splash)
#     splash:init_cookies(splash.args.cookies)
#     local url = splash.args.url
#     assert(splash:go(url))
#     assert(splash:wait(0.5))
#     return {
#         cookies = splash:get_cookies(),
#         html = splash:html()
#     }
# end
# """


class VNSpider(scrapy.Spider):
    name = 'vnwork'
    allowed_domains = ['vietnamworks.com']
    start_urls = ['https://www.vietnamworks.com/viec-lam-it-phan-mem-i35-vn/']
    base_url = 'https://www.vietnamworks.com/'

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, endpoint="render.html", callback=self.parse)

    def parse(self, response):
        all_books = response.xpath('/html/body/div[1]/div/div[4]/div[1]/div[4]/div/div[1]/div[3]/div[1]/div[1]/div[1]/div/div/div[1]/div/div[1]/div/div/div[2]/div/h3/a')

        yield {
            'link': all_books.extract()
        }
        # for book in all_books:
        #     book_url = book.xpath('/@href').extract_first()
        #
        #     book_url = self.base_url + book_url
        #     yield {
        #         'mota': book_url
        #     }
        #     # yield scrapy.Request(book_url, callback=self.parse_book)
    #
    #     next_page_partial_url = response.xpath(
    #         '//li[@class="next"]/a/@href').extract_first()
    #
    #     # if next_page_partial_url:
    #     #     if 'catalogue/' not in next_page_partial_url:
    #     #         next_page_partial_url = "catalogue/" + next_page_partial_url
    #
    #     next_page_url = self.base_url + next_page_partial_url
    #     yield scrapy.Request(next_page_url, callback=self.parse)
    #
    # def parse_book(self, response):
    #     title = response.xpath('//div[@class="job-header-info"]/h1/text()').extract()
    #     yield {
    #         'title': title
    #     }

# class VNSpider(scrapy.Spider):
#     name = 'vietnamwork'
#     allowed_domains = ['vietnamworks.com']
#     start_urls = ['https://www.vietnamworks.com/viec-lam-it-phan-mem-i35-vn',
#                   ]
#     base_url = 'https://www.vietnamworks.com/'
#
#     def parse(self, response):
#         all_job = response.xpath('//div[@class="job-item"]')
#
#         for job in all_job:
#             job_url = job.xpath('.//h3/a/@href').extract_first()
#
#             job_url = self.base_url + job_url
#             yield {
#                 'title': job_url
#             }
#
#             # yield scrapy.Request(job_url, callback=self.parse_job)
#
#         # next_page_partial_url = response.xpath(
#         #     '//a[@class="ais-pagination--link"]/@href').extract_first()
#         #
#         # next_page_url = self.base_url + next_page_partial_url
#         # yield scrapy.Request(next_page_url, callback=self.parse)
#
#     # def parse_job(self, response):
#     #     title = response.xpath('//div[@class="job-header-info"]/h1/text()').extract_first()
#     #     # mo_ta = response.xpath('.//div[@class="description"]/text()').extract()
#     #     # yeu_cau = response.xpath('.//div[@class="requirements"]/text()').extract()
#     #     # ten_ct = response.xpath('//div[@class="job-header-info"]//div[@class="col-sm-12 company-name"]/a/text()').extract()
#     #     # dia_chi = response.xpath('//div[@class="job-header-info"]//div[@class="col-sm-12 company-name"]/span/a/text()').extract()
#     #
#     #     yield {
#     #         'Title': title,
#             # 'mo_ta': mo_ta,
#             # 'yeu_cau': yeu_cau,
#             # 'ten_cong_ty': ten_ct,
#             # 'dia_chi': dia_chi
#
#         # }
#
#
#
#     # def parse(self, response):
#     #     # The main method of the spider. It scrapes the URL(s) specified in the
#     #     # 'start_url' argument above. The content of the scraped URL is passed on
#     #     # as the 'response' object.
#     #
#     #     nextpageurl = response.xpath('//a[@class="ais-pagination--link"]/@href')
#     #
#     #
#     #     for item in self.scrape(response):
#     #         yield item
#     #
#     #     if nextpageurl:
#     #         path = nextpageurl.extract_first()
#     #         nextpage = response.urljoin(path)
#     #         print("Found url: {}".format(nextpage))
#     #         yield scrapy.Request(nextpage, callback=self.parse)
#
#     # def parse(self, response):
#     #     item = RequimentItem()
#     #     # for resource in response.xpath('//div[@class="job-item-info relative"]/h3/..'):
#     #     item['title'] = response.xpath('//*[@id="job-list"]//h3/a/@href').extract_first()
#         # item['title'] = resource.xpath('//div[@class="job-header-info"]/h1/text()').extract_first()
#             # item['ten_cong_ty'] = resource.xpath('normalize-space(//div[@class="col-sm-12 company-name"]/a/text())').extract_first()
#             # item['mo_ta'] = resource.xpath('.//div[@class="description"]/text()').extract_first()
#             # item['yeu_cau'] = resource.xpath('.//div[@class="requirements"]/text()').extract_first()
