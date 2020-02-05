# PyScrape

PyScrape is a basic web scraper that I wrote for practice while learning Python. Initally, it was written to scrape the discount items page of Schiit Audio's sales website, which can be found here: 'https://www.schiit.com/b-stocks', but I have adapted the basic structure to eBay.ca (currently only functional for Canadian eBay) as well, and plan to expand it to other websites. Each website-specific scraper will be titled as such.

## Table of Contents
- About
- How It Works
- Usage
    - To Test
    - Prerequisites
- Getting Started
- To Do
- Author
- Acknowledgments

## About

Schiit Audio Scraper is an attempt at creating a basic web scraper that can be utilized through a graphical user interface modeled in tkinter. The GUI gives the user the ability to enter their desired website url, item to search for, sender email and password, and receiver email. It includes a Submit button that will get all of the entries in the desired fields, a "Submit without email" button if the user only wishes to perform the search, but does not wish to send out an email with the results, as well as a "Clear Entries" button to clear the entry fields, and a "Close" button to close the program. The name of the item the user entered is then compared to a section of text that was retreived and parsed using requests and Beautiful Soup 4, which can include a list of items. Schiit Audio Scraper is currently not functional for other websites, but can be tested on the discount items page of Schiit Audio's sales website, found here: https://www.schiit.com/b-stocks

Ebay Scraper works similarly to Schiit Audio Scraper, and will search through an eBay.ca results page to find items within a certain price range. The user passes in the URL from the eBay.ca search of an item they are looking for, as well as a maximum price that they wish to pay for the item. Currently, the email functionality for this program is disabled while I work on formatting the results so they can be displayed more clearly in an email sent via smtplib, but the entry fields for email info are still present. The program searches for the listed price as well as the shipping price, combines the two prices into a total price, and compares the user-entered maximum price against the total price of that item. If the total price of the item is less than or equal to the maximum price specified by the user, the item will be printed to screen.

I plan on adapting the basic framework it to other websites. Currently, I have version for:
- Schiit Audio B-Stocks
- eBay.ca

Currently, I'm working on "compare_files.py" which will be a separate program to compare files on one's own computer to those listed on a website. It can be used when a user is trying to download sequential files from a website, but may already have some of those files. It will write the names of the files listed on the website that are not currently in the provided directory to a json file.

## How It Works

1) Schiit Audio Scraper launches a GUI built in tkinter that contains input fields for desired website, name of item to search, sender email and password, and receiver email. 

2) When the user clicks the "Submit" button, these are then put into a dictionary, which is stored as a JSON file that is written into the current working directory. Note that clicking the "Submit" button overwrites the JSON file with each press, so it will not store multiple inputs.

3) After the GUI window is closed, the main portion of the code then creates a dictionary, which it sets equal to the dictionary read from the JSON file.

4) Beautiful Soup 4 is then used to parse the website into a usable format, and compares the user-provided item name to the items listed in the section searched for. If the item is listed in that section, the corresponding function returns the item name and price.

5) Pandas is then used called to create a CSV file containing the item name, price, and date it was checked for price tracking purposes. This file will be created if not found, or appended to if it has already been created.

6) The title and price are then formatted into as an f-string with: f"{title} is {price} on {date.today()}".
    - ex. "Asgard 2 is $159 on 2020-01-05"

7) The formatted string is then printed to screen.

8) The formatted string is then sent vis smtplib to the receiver email provided in the GUI.

## Usage

### TO TEST

If you do not wish for any emails to be sent while testing, I will provide a "Submit without email" button in the GUI so that it is not necessary to enter any email info to complete the search.

#### schiit_audio_scraper.py: 
I will provide the website URL and some example items below for testing that will also be provided as commented out options in the code. These can be entered in the website and item GUI fields so that you can run the search easily without having to look at the website:
- URL: 'https://www.schiit.com/b-stocks'
- Item Name:
    - 'Asgard 2' - this item is currently listed as of January 2020
        - Will return price in formatted info
    - 'Yggdrasil' - this is an item that is in Schiit's normal catalog, but is not currently listed on the B-Stock page
        - Will return 'not listed' as price in formatted info

#### ebay_scraper.py
This program can be tested using a URL from a search on ebay.ca. You must first search for an item, then copy/paste that URL into the "Enter URL: " field. Please enter the maximum price that you would like to pay for the item into the "Enter max" price field, and if desired, email info. I plan to add email functionality to this version once I'm able to format the large list of results properly in smtplib.

### Prerequisites

- Python 3.6+, if lower f-strings neeed to be reformatted
- pandas
- beautifulsoup4

## To Do
- Implement a way for HTML to be entered via the GUI, so it can be more easily adapted to other websites
- Store JSON and CSV files in user supplied filepath, if desired
- Add ability to search for multiple items at a time
- Improve GUI aesthetics and formatting
- Improve my code!

## Author

Chris Whitlock

This is the first project that I've ever created, so it may be a bit rough around the edges with regards to formatting and readability, but you can't learn if you don't try! Thanks for checking out my code!

## Acknowledgments

Harrsion Kinsley, founder of pythonprogramming.net, whose tkinter tutorial can be found here: https://pythonprogramming.net/python-3-tkinter-basics-tutorial/

John Elder and Codemy for the excellent tkinter tutorial videos on YouTube.

Kyle Lobo for tips on how to write this README, (https://github.com/kylelobo/The-Documentation-Compendium).

*Crash Course Python* by Eric Matthes

*Automate the Boring Stuff* by Al Sweigart