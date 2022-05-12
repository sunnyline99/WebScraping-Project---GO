import scrapy
class Info(scrapy.Item): #create scrapy fields
    player = scrapy.Field()
    wins = scrapy.Field()
    losses = scrapy.Field()
    total = scrapy.Field()
    date = scrapy.Field()
    white_win = scrapy.Field()
    white_lose = scrapy.Field()
    black_win = scrapy.Field()
    black_lose = scrapy.Field()
    rating = scrapy.Field()
    average_rating_differences = scrapy.Field()


class ProjectSpider(scrapy.Spider):
    name = "scrapy_output" #name the scrapy
    allowed_domains = ["www.goratings.org"] #allowed domain name
    try:
        with open("link_lists.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:]
    except:
        start_urls = []

    def parse(self, response):
        p = Info()
        player_xpath = '//h1/text()' #refer to xpaths
        date_xpath = '//th[text()="Date of Birth"]/following-sibling::*/text()'
        wins_xpath = '//th[text()="Wins"]/following-sibling::*/text()'
        losses_xpath = '//th[text()="Losses"]/following-sibling::*/text()'
        total_xpath= '//th[text()="Total"]/following-sibling::*/text()'
        rating_xpath ='//table[2]/tr[2]/td[2]/text()'

        colors_list = [] #create lists for the color the player plays with
        wins_losses_list=[] #list containing either loss or wim
        player_elo_list =[] #the rating of the player at the time of the game
        opponent_elo_list =[] #the rating of the opponent at the time of the game
        wl = 0 #Instances when player playing with white pieces lost
        ww = 0 #Instances when player playing with white pieces won
        bw = 0 #black pieces won
        bl = 0 #black pieces lost
        diff = 0 #difference between the player's and the opponent's ratings
        for j in range(2, 12): #extract only the last 10 games
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

        for i in range(0,10): #Iterate over the last 10 games
            if colors_list[i]== "White" and wins_losses_list[i]== "Win":
                ww = ww +1 #if the player with white pieces one, ww variable will imcrease by one
            elif colors_list[i]== "White" and wins_losses_list[i]== "Loss":
                wl = wl + 1
            elif colors_list[i]== "Black" and wins_losses_list[i]== "Win":
                bw = bw + 1
            elif colors_list[i]== "Black" and wins_losses_list[i]== "Loss":
                bl = bl + 1
        for i in range(0,10):
             diff = diff - int(opponent_elo_list[i])+int(player_elo_list[i]) #for the last 10 games, calculate the difference
#between the player's and the opponents ratings

        p['player'] = response.xpath(player_xpath).getall()
        p['date'] = response.xpath(date_xpath).getall()
        p['wins'] = response.xpath(wins_xpath).getall()
        p['losses'] = response.xpath(losses_xpath).getall()
        p['white_win'] = ww/10 #calculate the instances as a proportion of total games taken into accouy
        p['white_lose'] = wl/10
        p['black_win'] = bw/10
        p['black_lose'] = bl/10
        p['rating'] =response.xpath(rating_xpath).getall()
        p['total'] = response.xpath(total_xpath).getall()
        p['average_rating_differences'] = diff/10 #calculate the average difference between the ratings of the player and the opponent

        yield p
