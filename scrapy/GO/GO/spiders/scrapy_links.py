import scrapy

default_no_pages = True

if default_no_pages == True:
    no_pages = 100
else:
    no_pages_q = input('Please provide number of player pages to scrape from https://www.goratings.org/en/: ')
    no_pages = int(no_pages_q)

class Link(scrapy.Item):
    link = scrapy.Field()

class LinkListsSpider(scrapy.Spider):
    name = 'link_lists'
    allowed_domains = ['www.goratings.org']
    start_urls = ['https://www.goratings.org']
    def parse(self, response):
        for i in range(2, no_pages+2):
            xpath = './/tr['+ str(i)+']/td[2]/a/@href'
            selection = response.xpath(xpath)
            for s in selection:
                l = Link()
                link2 = s.get()
                link2 = link2.replace("..","")
                l['link'] = 'https://www.goratings.org' + link2
                yield l
# TERMINAL: scrapy crawl link_lists -o link_lists.csv -t csv