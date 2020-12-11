from Scrapy.requiment.requiment.spiders.careerbuilder import StackSpider as CareerBuilderSpider
from Scrapy.requiment.requiment.spiders.careerlink import StackSpider as CareerLinkSpider
from Scrapy.requiment.requiment.spiders.devwork import CareerbuilderSpider as DevWorkSpider
from Scrapy.requiment.requiment.spiders.itviec import ItviecSpider

# Cac loai spider tuong ung cho tung trang web: ITViec, CareerLink,...
# co the them vao tu thu muc 'Scrapy.requiment.requiment.spiders'
crawl_spiders = {
    'careerbuilder': CareerBuilderSpider(),
    'careerlink': CareerLinkSpider(),
    'devwork': DevWorkSpider(),
    'it': ItviecSpider()
}

# 'careerbuilder': StackSpider(),
#                     'careerlink':, 'devwork', 'indeed', 'itviec', 'jobstreet', 'mywork',
#                 'nhanlucit', 'timviec365', 'timviecnhanh', 'topcv', 'topitwork', 'tuyendungvieclam',
#                 'vieclam24h', 'vietnamwork'
