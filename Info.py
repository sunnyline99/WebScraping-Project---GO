import scrapy
class Info(scrapy.Item):
    player = scrapy.Field()
    wins = scrapy.Field()
    losses = scrapy.Field()
    date = scrapy.Field()

class ProjectSpider(scrapy.Spider):
    name = "basic_info"
    allowed_domains = ["www.goratings.org"]
    try:
        with open("link_lists.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:]
    except:
        start_urls = []

    def parse(self, response):
        p = Info()
        player_xpath = '//h1/text()'
        date_xpath = '//th[text()="Date of Birth"]/following-sibling::*/text()'
        wins_xpath = '//th[text()="Wins"]/following-sibling::*/text()'
        losses_xpath = '//th[text()="Losses"]/following-sibling::*/text()'

        p['player'] = response.xpath(player_xpath).getall()
        p['date'] = response.xpath(date_xpath).getall()
        p['wins'] = response.xpath(wins_xpath).getall()
        p['losses'] = response.xpath(losses_xpath).getall()

        yield p
#scrapy crawl basic_info -o Info.csv -t csv
