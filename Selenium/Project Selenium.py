from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd


# Init:
gecko = input('Please provide path for the geckodriver (you can copy path with "" signs). If you want use default path "/opt/homebrew/bin/geckodriver" please click enter:')
if gecko =='':
    gecko_path = 'C:/Users/justy/Desktop/Info/Inne/DSC/UW/Semestr II/Webscrapping/geckodriver-v0.30.0-win64/geckodriver'
else:
    gecko = gecko.replace('"', '')
    gecko_path = gecko
ser = Service(gecko_path)
options = webdriver.firefox.options.Options()
options.headless = False
driver = webdriver.Firefox(options = options, service=ser)


url = 'https://www.goratings.org/en/'

data = pd.DataFrame({'player_name':[],'gender':[], 'nationality':[], 'date+of_birth':[], 'elo':[], 'wins':[], 'losses':[], 'total':[]})

# Actual program:
driver.get(url)

time.sleep(2)
for i in range(2,102):

    ## get data from the main url (gender,nationality,elo) for every iteration

    gender = driver.find_element(By.XPATH,'/html/body/table[2]/tbody/tr['+str(i)+']/td[3]/span').text
    if gender == "♂":
        gen = "Male"
    else:
        gen = "Female"
    flag = driver.find_element(By.XPATH,'/html/body/table[2]/tbody/tr['+str(i)+']/td[4]/img')
    nationality = flag.get_attribute('alt')
    elo = driver.find_element(By.XPATH,'/html/body/table[2]/tbody/tr['+str(i)+']/td[5]').text

    ## get link to the personal page and click on the element

    player_link = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr['+str(i)+']/td[2]/a')
    player_link.click()
    #time.sleep(0.1)

    ## get data from personal page (name, wins, losses, total games, date of birth) for every iteration

    player_name = driver.find_element(By.XPATH,'/html/body/h1').text
    player_wins = driver.find_element(By.XPATH,'.//th[text()=\'Wins\']/following-sibling::td').text
    player_losses = driver.find_element(By.XPATH,'.//th[text()=\'Losses\']/following-sibling::td').text
    player_total = driver.find_element(By.XPATH,'.//th[text()=\'Total\']/following-sibling::td').text
    player_date_of_birth = driver.find_element(By.XPATH,'.//th[text()=\'Date of Birth\']/following-sibling::td').text

    ## Save data to dataFrame

    player = {'player_name':player_name,'gender':gen, 'nationality':nationality, 'date+of_birth':player_date_of_birth, 'elo':elo, 'wins':player_wins, 'losses':player_losses, 'total':player_total}

    data = data.append(player, ignore_index = True)

    print(data)
    ## go back to the main page to iterate

    url = 'https://www.goratings.org/en/'
    driver.get(url)


data.to_csv('C:/Users/justy/Desktop/Info/Inne/DSC/UW/Semestr II/Webscrapping/GO Players.csv')