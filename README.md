# PyScrape

PyScrape is a basic web scraper that I wrote for practice while learning Python. Currently, it's only functional the website that I wrote it for, which is the discount items page of Schiit Audio's sales website, which can be found here: 'https://www.schiit.com/b-stocks'

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

PyScrape is an attempt at creating a basic web scraper that can be utilized through a graphical user interface modeled in tkinter. The GUI gives the user the ability to enter their desired website url, item to search for, sender email and password, and receiver email. It includes a Submit button that will get all of the entries in the desired fields and pass them off as a dictionary to a json file. The name of the item the user entered is then compared to a section of text that was retreived and parsed using requests and Beautiful Soup 4, which can include a list of items.  

PyScrape is currently not functional for most websites, but can be tested on the website it was written for and tested on, which is the discount items page of Schiit Audio's sales website, found here: https://www.schiit.com/b-stocks

I plan on editing it later so that the desired HTML can be entered via the GUI for use when parsing in order to make it more functional for other websites.

## How It Works

1) PyScrape launches a GUI built in tkinter that contains input fields for desired website, name of item to search, sender email and password, and receiver email. 

2) When the user clicks the "Submit" button, these are then put into a dictionary, which is stored as a JSON file which is written into the currently active folder. Note that clicking the "Submit" button overwrites the JSON file with each press, so it will only ever contain a single dictionary.

3) After the GUI window is closed, the main portion of the code then creates a dictionary, which it sets equal to the dictionary read from the JSON file.

4) PyScrape then uses Beautiful Soup 4 to parse the website into a usable format, and compares the user-provided item name to the items listed in the section searched for. If the item is listed in that section, the corresponding function returns the item name and price.

5) Pandas is then used called to create a CSV file containing the item name, price, and date it was checked for price tracking purposes. This file will be created if not found, or appended to if it has already been created.

6) The title and price are then formatted into as an f-string with: f"{title} is {price} on {date.today()}".
    - ex. "Asgard 2 is $159 on 2020-01-05"

7) The formatted string is then printed to screen.

8) The formatted string is then sent vis smtplib to the receiver email provided in the GUI.

## Usage

### TO TEST

I will provide the website URL and some example items below for testing that will also be provided as commented out options in the code. These can be entered in the website and item GUI fields so that you can run the search easily without having to look at the website:
    - URL: 'https://www.schiit.com/b-stocks'
    - Item Name:
        - 'Asgard 2' - this item is currently listed as of January 2020
            - Will return price in formatted info
        - 'Yggdrasil' - this is an item that is in Schiit's normal catalog, but is not currently listed on the B-Stock page
            - Will return 'not listed' as price in formatted info

If you do not wish for any emails to be sent while testing, I will provide a "no email" version with the smtplib section commented out to be run so that the user can run it while only getting the console output and csv data file.

### Prerequisites

- Python 3.6+, if lower f-strings neeed to be reformatted
- pandas
- beautifulsoup4

## To Do
- Implement a way for HTML to be entered via the GUI, so it can be more easily adapted to other websites
- More thorough testing
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