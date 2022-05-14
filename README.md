# WebScraping-Project---GO
WebScraping final project. Scraping data about "GO" game players.

In the folder "soup" there is a file containing Beautiful Soup scraping solution. You can run the code in the console navigating to the directory that contains soup.py file  by -> "cd (path)". Then use command "python soup.py". By default script will scrape first 100 players pages. If you set "default_no_pages" parameter to False, you will be asked to provide number of the pages that you want to scrape (use int as input and check if there are that many players pages on the website). At the end you will be asked to provide the path to save the csv output. If you don`t provide path by default it is current directory.

In the folder "scrapy" there is a file containing full scrapy project. Inside the project in the "spiders" file there are 2 scripts. Project_Scrapy_links.py obtains the list of links necessary for further scraping. If the no_pages is kept at the default 100, it will scrape the first 100 links. It is necessary to save the output using the following command in the terminal: scrapy crawl link_lists -o link_lists.csv -t csv. Project_Scrapy.py performs the scraping of these webpages and returns the final output. To run second spider please use "scrapy crawl scrapy_output -o Go_Players_Data_Scrapy.csv -t csv" command in the console.

Ine the folder "selenium" there is a file containing Selenium scraping solution. you can run the code from console navigating to the directory with .....py file. Then use command "python soup.py". By default script will scrape first 100 players pages. If you set "default_no_pages" parameter to False, you will be asked to provide number of the pages that you want to scrape (use int as input and check if there are that many players pages on the website). 
