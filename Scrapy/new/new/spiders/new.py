import scrapy
from ..items import NewItem  # We need this so that Python knows about the item object


class NewSpider(scrapy.Spider):
    name = 'new'  # The name of this spider

    # The allowed domain and the URLs where the spider should start crawling:
    allowed_domains = ['www.aph.gov.au']
    start_urls = [
        'http://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results?q=&mem=1&par=-1&gen=0&ps=0/']

    def parse(self, response):
        # The main method of the spider. It scrapes the URL(s) specified in the
        # 'start_url' argument above. The content of the scraped URL is passed on
        # as the 'response' object.

        nextpageurl = response.xpath("//a[@title='Next page']/@href")

        for item in self.scrape(response):
            yield item

        if nextpageurl:
            path = nextpageurl.extract_first()
            nextpage = response.urljoin(path)
            print("Found url: {}".format(nextpage))
            yield scrapy.Request(nextpage, callback=self.parse)

    def scrape(self, response):
        for resource in response.xpath("//h4[@class='title']/.."):
            # Loop over each item on the page.
            item = NewItem()  # Creating a new Item object

            item['name'] = resource.xpath("h4/a/text()").extract_first()
            item['link'] = resource.xpath("h4/a/@href").extract_first()
            item['district'] = resource.xpath("dl/dd/text()").extract_first()
            item['twitter'] = resource.xpath("dl/dd/a[contains(@class, 'twitter')]/@href").extract_first()
            item['party'] = resource.xpath("dl/dt[text()='Party']/following-sibling::dd/text()").extract_first()

            yield item
