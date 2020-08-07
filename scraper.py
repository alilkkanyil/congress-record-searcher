# File: scraper.py
# Function: Intended to scrape congress.gov
# for text searches on every congressional record.
# Currently scrapes the html page of a given date,
# Displays the list of congressional records for that date.
# Last updated: 08.05.20, by Ali Yildirim

#####################################################################
# TODO: Add GUI
# TODO: Clean code
#####################################################################

from bs4 import BeautifulSoup
import requests

matchList = ["unanimous consent", "ask consent", "request consent", "ask unanimous consent", "request unanimous consent", "ask Unanimous Consent", "request Unanimous Consent", "without objection", "without objection", "it is so ordered", "without objection it is so ordered", "without objection so ordered"]

# Whether or not a new search will be made
repeat = True

# Iterator for switching to a second batch
batchIterator = 1

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
                batchIterator = batchIterator + 1
            else:
                month3 = month3 + 1
                day3 = 1
                batchIterator = batchIterator + 1
            if(month3 == 12):
                month3 = 1
                year = year + 1
            found = True
        
#####################################################################
# The program opens a new file for 7 day increments to write the results
# This is done to prevent data loss or need to restart the process if
# The program crashes on a long period
#####################################################################
        fileDate = str(day3) + "_" + str(month3) + "_" + str(year3) + ".csv"
        if(batchIterator > 7):
            batchIterator = 1
            batchFile.close() 
        
        if(batchIterator == 1): 
            batchFile = open(fileDate, "w+")
#####################################################################
# if "Page not Found" text is not seen on the html page,
# prints the list of pages of congressional meetings that occured.
# This list will later be used to crawl through each page. For now,
# its there for testing purposes only.
# If found value is True, it'll print "No data available."
##################################################################### 
    
        pageList = []
        if(found == False):   
            iterator = 1
            print("No.\tPage Number\n")
            for article in lines.find_all('td'):
                if(iterator % 2 != 1):
                    pageList.append(str(article.text))
                iterator = iterator + 1
            
            pageList = list(dict.fromkeys(pageList))
            print(pageList)

            iterator = iterator - 1
            for x in range (len(pageList)):
                #####################################################################
                # Selects a page to process
                #####################################################################
                # Page number of the record
                page = 1
                recordPage = pageList[x]
                endOfPage = False
                
                #####################################################################
                # Opens found page assuming one is selected
                #####################################################################                
                while(endOfPage == False):
                    # Record link + page
                    record = "https://www.congress.gov/congressional-record/" + str(year3) + "/" + str(month3) + "/" + str(day3) + "/senate-section/article/" + recordPage + "-" + str(page)
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
                        for word in matchList:
                            if(word in lines3):
                                print(record)
                                print(word)
                                batchFile.write(record + "," + word + "\n")
                        page = page + 1

#####################################################################
# Iterates through the date until end date is reached
#####################################################################
               
            if(day3<31):
                day3 = day3 + 1
                batchIterator = batchIterator + 1
            else:
                month3 = month3 + 1
                day3 = 1
                batchIterator = batchIterator + 1
            if(month3 == 13):
                month3 = 1
                year = year + 1


#####################################################################
# Asks user if they want to repeat the search from beginning.
# if not, ends program.
#####################################################################
    batchFile.close()

    userChoice = input("\nWould you like to start over? (y/n): ")
    if(userChoice == 'y' or userChoice == 'Y'):
        repeat = True
    else:
        repeat = False
