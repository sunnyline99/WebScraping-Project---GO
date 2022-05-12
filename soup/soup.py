# import the library used to scrape information from a website
from bs4 import BeautifulSoup as BS
import requests
import pandas as pd
import re
import time

## Measuring the time efficiency of the code

startTime = time.time()

## Default number of scraped pages

default_no_pages = True

if default_no_pages == True:
    no_pages=100
else:
    no_pages_q = input('Please provide number of player pages to scrape from https://www.goratings.org/en/: ')
    no_pages = int(no_pages_q)

# specify the main url
url = "https://www.goratings.org/en/"

# parse the html in the 'bs' variable, and store it in Beautiful Soup format using "lxml" parser
bs = BS(requests.get(url).text, "lxml")

# find and return all the links for players using regex string
tags = bs.find_all('a', {'href':re.compile('.*\/players\/.*')})

# create an empty list for storing the full links
links=[]

# add full links for the first 100 players pages to the list
for i in range(0,100):
    links.append("https://www.goratings.org/en/"+tags[i]['href'])

# create an empty list for storing scraped information
result=[]

# main loop for scrapping the data from the players pages
for i in links:
# specify each player page
    url1=i
# parse the each player page in the 'bs' variable, and store it in Beautiful Soup format using "lxml" parser
    bs = BS(requests.get(url1).text, "lxml")
# extract player's name from h1
    player_name = bs.find('h1').get_text()
# extract the 1st table with player's data including wins, losses, total games and date of birth
# and the second table with player's games statistics including last 10 games results
    table1 = bs.find_all('table')[0]
    table2 = bs.find_all('table')[1]
# transforming the 1st and the 2nd table to pandas dataframe
    df1 = pd.read_html(str(table1))[0]
    df2 = pd.read_html(str(table2))[0]
# extracting information from the dataframes
    wins = df1.iat[0,1]
    losses = df1.iat[1,1]
    total = df1.iat[2,1]
    date_of_birth = df1.iat[-1,1]
    elo = df2.iat[0,1]
# making mini-table for 10 last games to calculate results depending on the color
# making mini-table for 10 last games to calculate average rating
    df5 = df2.iloc[:10, [2,3]]
    df6 = df2.iloc[:10, [1,5]]
# setting default values for future indicators
    bw_perc = 0
    bl_perc = 0
    ww_perc = 0
    wl_perc = 0
    avg_diff = 0
# internal loop #1 for calculating results depending on the color for last 10 games
    for ind in df5.index:
        if df5['Color'][ind] == "Black" and df5['Result'][ind] == "Win":
            bw_perc+=1
        elif df5['Color'][ind] == "Black" and df5['Result'][ind] == "Loss":
            bl_perc+=1
        elif df5['Color'][ind] == "White" and df5['Result'][ind] == "Win":
            ww_perc += 1
        elif df5['Color'][ind] == "White" and df5['Result'][ind] == "Loss":
            wl_perc += 1
# internal loop #2 for calculating average rating difference for last 10 games
    for ind in df6.index:
        avg_diff = avg_diff + df6['Rating'][ind] - df6['Opponent.1'][ind]

# calculate final indicators
    bw_perc = bw_perc / len(df5.index)
    bl_perc = bl_perc / len(df5.index)
    ww_perc = ww_perc / len(df5.index)
    wl_perc = wl_perc / len(df5.index)
    avg_diff = avg_diff / len(df6.index)

# create a list with all scraped data
    result.append([player_name,date_of_birth,elo,wins,losses,total,ww_perc,wl_perc,bw_perc,bl_perc,avg_diff])

# transforme the list to a pandas dataframe and export to csv
bs_result = pd.DataFrame(result, columns=["player_name","date_of_birth","elo","wins","losses","total","ww_perc","wl_perc","bw_perc","bl_perc","avg_diff"])
bs_result.to_csv('bs_result.csv')

## Measure the execution time

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))
