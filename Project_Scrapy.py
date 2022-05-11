import scrapy


class Info(scrapy.Item):
    player = scrapy.Field()
    wins = scrapy.Field()
    losses = scrapy.Field()
    total = scrapy.Field()
    date = scrapy.Field()
    white_win = scrapy.Field()
    white_lose = scrapy.Field()
    black_win = scrapy.Field()
    black_lose = scrapy.Field()
    latest_rating = scrapy.Field()
    average_rating_differences = scrapy.Field()
    wins_losses= scrapy.Field()


class Other(scrapy.Item):
    x = scrapy.Field()


class ProjectSpider(scrapy.Spider):
    name = "ultimate"
    allowed_domains = ["www.goratings.org"]
    urls =[]
    try:
        with open("link_lists.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:]
            print(start_urls)
    except:
        start_urls = []

    def parse(self, response):
        p = Info()
        urls.append(start_urls)
        player_xpath = '//h1/text()'
        date_xpath = '//th[text()="Date of Birth"]/following-sibling::*/text()'
        wins_xpath = '//th[text()="Wins"]/following-sibling::*/text()'
        losses_xpath = '//th[text()="Losses"]/following-sibling::*/text()'
        total_xpath= '//th[text()="Total"]/following-sibling::*/text()'

        colors_list = []
        wins_losses_list=[]
        player_elo_list =[]
        opponent_elo_list =[]
        wl = 0
        ww = 0
        bw = 0
        bl = 0
        diff = 0
        for j in range(2, 12):
            #ww, wl, bw, bl = 0
            color = response.xpath('//table[2]/tr[' + str(j) + ']/*[3]/text()')
            for i in color:
                colors_list.append(i.extract())

            wins_losses = response.xpath('//table[2]/tr[' + str(j) + ']/*[4]/text()')
            for i in wins_losses:
                wins_losses_list.append(i.extract())

            player_elo = response.xpath('//table[2]/tr[' + str(j) + ']/*[2]/text()')
            for i in player_elo:
                player_elo_list.append(i.extract())

            opponent_elo = response.xpath('//table[2]/tr[' + str(j) + ']/*[6]/text()')
            for i in opponent_elo:
                opponent_elo_list.append(i.extract())

                # print(row.xpath('td/text()').getall())
        for i in range(0,10):
            if colors_list[i]== "White" and wins_losses_list[i]== "Win":
                ww = ww +1
            elif colors_list[i]== "White" and wins_losses_list[i]== "Loss":
                wl = wl + 1
            elif colors_list[i]== "Black" and wins_losses_list[i]== "Win":
                bw = bw + 1
            elif colors_list[i]== "Black" and wins_losses_list[i]== "Loss":
                bl = bl + 1
        for i in range(0,10):
             diff = diff + int(opponent_elo_list[i])-int(player_elo_list[i])


        p['player'] = response.xpath(player_xpath).getall()
        p['date'] = response.xpath(date_xpath).getall()
        p['wins'] = response.xpath(wins_xpath).getall()
        p['losses'] = response.xpath(losses_xpath).getall()
        p['white_win'] = ww/10
        p['white_lose'] = wl/10
        p['black_win'] = bw/10
        p['black_lose'] = bl/10
        p['total'] = response.xpath(total_xpath).getall()
        p['wins_losses'] = urls
        p['average_rating_differences'] = diff/10

        yield p
# scrapy crawl basic_info -o Info.csv -t csv
