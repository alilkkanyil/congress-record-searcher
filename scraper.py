# File: scraper.py
# Function: Intended to scrape congress.gov
# for text searches on every congressional record.
# Currently scrapes the html page of a given date,
# Displays the list of congressional records for that date.
# Last updated: 07.10.20, by Ali Yildirim

#####################################################################

# TODO: Ask for 2 dates, get list of all records inbetween
# TODO: Scrape record contents using the results of the search.
# TODO: String search to find every occuring instance in records

from bs4 import BeautifulSoup
import requests

# Whether or not a new search will be made
repeat = True

#####################################################################
# This section gets a date input from the user                      
# And requests the html page from congress.gov for that date.       
#####################################################################
   
while(repeat):
# Whether the scraper finds "Page not Found" or not, false by default  
    found = False

    year = input("Enter a year: ")
    day = input("Enter a day (numeric value): ")
    month = input("Enter a month (numeric value): ")
    fullDate = "https://www.congress.gov/congressional-record/" + year + "/" + str(month).zfill(2) + "/" + str(day).zfill(2) + "/senate-section"

#####################################################################
# This section gets the item list table that contains records
# and attempts to get breadcrumbs, where "page not found" is held
#####################################################################   
 
    source = requests.get(fullDate).text
    soup = BeautifulSoup(source, 'lxml')
    lines = soup.find('table', class_='item_table')
    links = lines.find_all('a', href = True)
    notFound = soup.find('div', class_="breadcrumbs")

#####################################################################
# if "Page Not Found" is encountered, found value set to true.
#####################################################################
    
    for header in notFound:
        if("Page Not Found" in header):
            found = True

#####################################################################
# if "Page not Found" text is not seen on the html page,
# prints the list of pages of congressional meetings that occured.
# This list will later be used to crawl through each page. For now,
# its there for testing purposes only.
# If found value is True, it'll print "No data available."
##################################################################### 
    
    if(found == False):   
        iterator = 1
        print("No.\tPage Number\n")
        for article in lines.find_all('td'):
            if(iterator % 2 != 0):
                print(article.text)
                print()
            iterator = iterator + 1

        # Entry number user has selected
        selection = input("\nEnter an article number: ")
        selection = links[(int(selection)*3-3)]['href']
        # Testing purposes only
        print(selection)
        print(selection[-1])

#####################################################################
# Opens found page assuming one is selected
#####################################################################
        
        # Page number of the record
        page = int(selection[-1])
        endOfPage = False

        while(endOfPage == False):
            # Record link + page
            record = "https://www.congress.gov" + selection[:-1] + str(page)
            print(record)
            # Requests the webpage of the record page
            source2 = requests.get(record).text
            soup2 = BeautifulSoup(source2, 'lxml')

            # If page is not found, it means end of record is reached
            if("Page Not Found" in source2):
                endOfPage = True
            # Else, prints page.
            else:
                lines2 = soup2.find('pre', class_='styled')
                print(lines2)
                page = page + 1
    else:
        print("No data available for given date.\n")


#####################################################################
# Asks user if they want to repeat the search from beginning.
# if not, ends program.
#####################################################################
    
    userChoice = input("\nWould you like to start over? (y/n): ")
    if(userChoice == 'y' or userChoice == 'Y'):
        repeat = True
    else:
        repeat = False
