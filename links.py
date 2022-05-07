import scrapy

class Link(scrapy.Item):
    link = scrapy.Field()

class LinkListsSpider(scrapy.Spider):
    name = 'link_lists'
    allowed_domains = ['www.goratings.org']
    start_urls = ['https://www.goratings.org']
    def parse(self, response):
        xpath = './/td[2]/a/@href'
        selection = response.xpath(xpath)
        for s in selection:
            l = Link()
            link2 = s.get()
            link2 = link2.replace("..","")
            l['link'] = 'https://www.goratings.org' + link2
            yield l
# TERMINAL: scrapy crawl link_lists -o Link_lists.csv -t csv
