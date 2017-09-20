# Example of parsing(crawling) [tripadvisor.co.uk](www.tripadvisor.co.uk) site

Installation:
  - Download the latest version of [Geckodriver](https://github.com/mozilla/geckodriver/releases)
  - Unzip and put chromedriver into project directory
  - Go to the [tripadvisor.co.uk](www.tripadvisor.co.uk) and enter your query in the search bar
  - Copy current url
  - Change domain (in main.py) to current url
  - Save main.py
  - type pip3 install -r requirements.txt
  - python3 main.py and wait :)

# Features!

  - Save extracted data into result.xls file in the project directory
  - Goes to companies sites and search their email!
  - Multiprocessing

# - result.xls format
| name_of_cafe | address | phone | cost | website | emails | orig_url |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| The Breakfast Club | 31 Camden Passage, London N1 8EA, England | +44 20 0000 0000 |££ - £££|http://peytonandbyrne.co.uk/ica-bar/index.html|eatpig@hashe8.com info@hashe8.com | https://www.tripadvisor.co.uk/Restaurant_Review-g186338-d4079623-Reviews-Costa_Coffee-London_England.html|
