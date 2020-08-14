# File: scraper2.py
# Function: Intended to go over the results from scraper.py
# It will be used to further refine search results.
# Currently it just prints the text from each output from scraper.py
# Last updated: 08.14.20, by Ali Yildirim

import os
from bs4 import BeautifulSoup
import requests
import csv

# Gets a list of all files in the directory
allfiles = os.listdir()

# Checks each file in the directory, grabs .csv files to be processed
for filename in allfiles:
    if(filename[-3:] == "csv"):
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            # Grabs links from each csv file and turns them into strings
            # Prints each page that was saved by the scraper.py script
            for row in csv_reader:
                try:
                    record = row[0]
                    source = requests.get(record).text
                    soup = BeautifulSoup(source, 'lxml')
                    lines = soup.find('pre', class_='styled')
                    lines2 = str(lines)
                    print(lines2)
                except:
                    print("Link invalid: " + row[0])