# File: scraper.py
# Function: Intended to scrape congress.gov
# for text searches on every congressional record.
# Currently scrapes the html page of a given date,
# Displays the list of congressional records for that date.
# Last updated: 07.24.20, by Ali Yildirim

#####################################################################
# TODO: Separate the code into functions, clean the code
# TODO: Add inbuilt word list and multi-word search
# TODO: Optimize page crawling
# TODO: Save found pages to a file
#####################################################################

from bs4 import BeautifulSoup
import requests

# Whether or not a new search will be made
repeat = True

#####################################################################
# This section gets a date input from the user                      
# And requests the html page from congress.gov for that date.
# Also gets a word to be searched from the user       
#####################################################################
   
while(repeat):
    year = input("Enter start year: ")
    day = input("Enter start day (numeric value): ")
    month = input("Enter start month (numeric value): ")
    
    year2 = input("Enter end year: ")
    day2 = input("Enter end day (numeric value): ")
    month2 = input("Enter end month (numeric value): ")

    word = input("Enter a word to be searched: ")
#####################################################################
#Int conversion of the variables as python takes string inputs
#####################################################################

    day3 = int(day)
    month3 = int(month)
    year3 = int(year)
    day4 = int(day2)
    month4 = int(month2)
    year4 = int(year2)
#####################################################################
# Script is looped until target date reached.
# Found tells if records ofr a date were found or not
#####################################################################

    while(year3 < year4 or day3 <= day4 or month3 < month4):
        found = False

#####################################################################
# This section gets the item list table that contains records
# and attempts to get breadcrumbs, where "page not found" is held
# Exception handling for when there's no data avilable to be grabbed.
#####################################################################
        try:
            fullDate = "https://www.congress.gov/congressional-record/" + str(year3) + "/" + str(month3).zfill(2) + "/" + str(day3).zfill(2) + "/senate-section"
            source = requests.get(fullDate).text
            soup = BeautifulSoup(source, 'lxml')
            lines = soup.find('table', class_='item_table')
            links = lines.find_all('a', href = True)
            notFound = soup.find('div', class_="breadcrumbs")
        
#####################################################################
# if "Page Not Found" is encountered, found value set to true.
#####################################################################
        except AttributeError:
            print("No data found for " + str(year3) + "/" + str(day3) + "/" + str(month3), " skipping.\n")
            if(day3<31):
                day3 = day3 + 1
            else:
                month3 = month3 + 1
                day3 = 1
            if(month3 == 12):
                month3 = 1
                year = year + 1
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
            
            iterator = iterator - 1
            for x in range (iterator//2):
                # Entry number user has selected
                selection = links[(int(x)*3-3)]['href']
                # Testing purposes only
                # print(selection)

                #####################################################################
                # Selects a page to process
                #####################################################################
                # Page number of the record
                page = int(selection[-1])
                endOfPage = False
                
                #####################################################################
                # Opens found page assuming one is selected
                #####################################################################                
                while(endOfPage == False):
                    # Record link + page
                    record = "https://www.congress.gov" + selection[:-1] + str(page)
                    # print(record)
                    # Requests the webpage of the record page
                    source2 = requests.get(record).text
                    soup2 = BeautifulSoup(source2, 'lxml')
                    
                    # If page is not found, it means end of record is reached
                    if("Page Not Found" in source2):
                        endOfPage = True
                    # Else, prints page.
                    else:
                        lines2 = soup2.find('pre', class_='styled')
                        lines3 = str(lines2)
                        if(word in lines3):
                            print("Found in: " + record)
                        page = page + 1

#####################################################################
# Iterates through the date until end date is reached
#####################################################################
               
            if(day3<31):
                day3 = day3 + 1
            else:
                month3 = month3 + 1
                day3 = 1
            if(month3 == 12):
                month3 = 1
                year = year + 1


#####################################################################
# Asks user if they want to repeat the search from beginning.
# if not, ends program.
#####################################################################
    
    userChoice = input("\nWould you like to start over? (y/n): ")
    if(userChoice == 'y' or userChoice == 'Y'):
        repeat = True
    else:
        repeat = False
