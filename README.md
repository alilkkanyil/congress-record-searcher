# Congressional Records Scraper
This is a python script meant to crawl through U.S. congress website's ("congress.gov") house of representatives and senate congressional records.
It takes keywords or sentences and a range of dates from the user and scrapes based on those parameters. The script is meant to allow the user to search when specific topics, laws, etc. have been discussed in the senate or house of representatives.

# Requirements
BeautifulSoup 4 (bs4)
urllib
requests library
python 3.x

# Instructions
When prompted, provide beginning and end date (YYYY/MM/DD) in integer values for the search.
Afterwards, provide the keyword to be searched. The program will display the records in which the keyword has appeared.
The program provides prompts when necessary.

Run with "python scrapper.py"
