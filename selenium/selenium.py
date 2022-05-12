## Loading necessary libraries

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd

## Measuring the time efficiency of the code

startTime = time.time()

## Default number of scraped pages

default_no_pages = True

if default_no_pages == True:
    no_pages=100

## Setting up geckodriver

gecko = input('Please provide path for the geckodriver (you can copy path with "" signs)')
if gecko =='':
    gecko_path = 'C:/Users/justy/Desktop/Info/Inne/DSC/UW/Semestr II/Webscrapping/geckodriver-v0.30.0-win64/geckodriver'
else:
    gecko = gecko.replace('"', '')
    gecko_path = gecko

## Initiate driver

ser = Service(gecko_path)
options = webdriver.firefox.options.Options()
options.headless = False
driver = webdriver.Firefox(options = options, service=ser)

## Set starting url and dataframe structure

url = 'https://www.goratings.org/en/'
data = pd.DataFrame({'player_name':[], 'date_of_birth':[], 'elo':[], 'wins':[], 'losses':[], 'total':[], 'ww_perc':[],'wl_perc':[], 'bw_perc':[], 'bl_Perc':[], 'avg_diff':[]})

## Open firefox with starting url and wait for 2 seconds to make sure page will load

driver.get(url)
time.sleep(2)

## iterate through 100 pages -> we must set range from 2 to 102 as the first player link is in 2nd <tr> (row), and last one in 101th row

for i in range(2,no_pages+2):

    ## for every iteration set some values to 0 as at the end they will be taken to calculations (make sure they are calculated properly for every player)

    ww = 0
    wl = 0
    bw = 0
    bl = 0
    diff = 0
    av_diff = 0

    ## get link to the personal page and click on the element + wait for 0.05 seconds to make sure it loads propely

    player_link = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr['+str(i)+']/td[2]/a')
    player_link.click()
    time.sleep(0.05)

    ## get data from personal page (name, wins, losses, total games, date of birth) for every iteration from first table

    player_name = driver.find_element(By.XPATH,'/html/body/h1').text
    player_wins = driver.find_element(By.XPATH,'.//th[text()=\'Wins\']/following-sibling::td').text
    player_losses = driver.find_element(By.XPATH,'.//th[text()=\'Losses\']/following-sibling::td').text
    player_total = driver.find_element(By.XPATH,'.//th[text()=\'Total\']/following-sibling::td').text
    player_date_of_birth = driver.find_element(By.XPATH,'.//th[text()=\'Date of Birth\']/following-sibling::td').text

    ## get player`s current elo - always frirst row in the games tabe (the most current rating)

    player_current_elo = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[2]/td[2]').text

    ## iterate through 10 first rows from the game table and get data about last 10 games (color of the pieces, result of the game, 
    ## player elo and opponent elo in the given game). Additionaly from last 10 games calculate on the fly percentage of wins/losses by pieces color
    ## and average difference of elo between player and opponent

    for j in range(2,12):

        ## get pieces color and result of the game for each iteration

        col = driver.find_element(By.XPATH,'/html/body/table[2]/tbody/tr['+str(j)+']/td[3]').text
        result = driver.find_element(By.XPATH,'/html/body/table[2]/tbody/tr['+str(j)+']/td[4]').text

        ## check if that was won/lost game and what piece color player has -> then add this statistics

        if(col == "White" and result == "Win"):
            ww=ww+1
        elif(col == "Black" and result == "Win"):
            bw=bw+1
        elif(col == "White" and result == "Loss"):
            wl=wl+1
        elif(col == "Black" and result == "Loss"):
            bl=bl+1

        ## calculate percentages of wins/losses for last 10 games (output in dataframe)

        ww_perc=ww/10
        bw_perc=bw/10
        wl_perc=wl/10
        bl_perc=bl/10

        ## Scrape player and opponent elo

        player_elo = col = driver.find_element(By.XPATH,'/html/body/table[2]/tbody/tr['+str(j)+']/td[2]').text
        opponet_elo = col = driver.find_element(By.XPATH,'/html/body/table[2]/tbody/tr['+str(j)+']/td[6]').text

        ## calculate difference for each game between player and opponent

        diff = diff + (int(player_elo)-int(opponet_elo))

    ## calculate average difference between player and opponents (dataframe output)

    av_diff = diff/10

    ## Save data to dataframe

    player = {'player_name':player_name,'date_of_birth':player_date_of_birth, 'elo':player_current_elo, 'wins':player_wins, 'losses':player_losses, 'total':player_total, 'ww_perc':ww_perc, 'wl_perc':wl_perc, 'bw_perc':bw_perc, 'bl_perc':bl_perc, 'avg_diff':av_diff}
    data = data.append(player, ignore_index = True)

    ## go back to the main page to grab another link for next player

    url = 'https://www.goratings.org/en/'
    driver.get(url)

## Measure the execution time

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))

## after all iterations save data to the dataframe

path = input('Please provide path for the csv file to be saved (name of the csv file is Go_Players_Data_Selenium.csv)')
file_path = path + '/Go_Players_Data_Selenium.csv'
data.to_csv(file_path)
