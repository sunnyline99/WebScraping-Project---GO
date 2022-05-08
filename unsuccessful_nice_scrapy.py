import scrapy

class Link(scrapy.Item):
    link = scrapy.Field()
    Nationality = scrapy.Field()
    Gender = scrapy.Field()

class LinkListsSpider(scrapy.Spider):
    name = 'link_lists2'
    allowed_domains = ['www.goratings.org']
    start_urls = ['https://www.goratings.org']
    def parse(self, response):
        xpath = './/td[2]/a/@href'
        selection = response.xpath(xpath)
        xpath_nationality='.//td[4]/img/@alt'
        selection_nationality = response.xpath(xpath_nationality)
        xpath_gender = './/td[3]/span/text()'
        selection_gender = response.xpath(xpath_gender)
        for s in range(0, 99):
            l = Link()
            link2 = selection[s].get()
            link2 = link2.replace("..","")
            l['link'] = 'https://www.goratings.org' + link2
            d = Link()
            d['Nationality']= selection_nationality[s].get()
            q = Link()
            q['Gender'] = selection_gender[s].get()
            yield l, d, q
# TERMINAL: scrapy crawl link_lists -o Link_lists.csv -t csv
