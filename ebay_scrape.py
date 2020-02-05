# A web scraper built in Pyhton 3.8 that can scrape info from ebay search listings
# Set a max price for the item as max_price, and pass in the URL of the ebay page after searching for the desired item
# If the item is below the max
# TODO:
#   - Use selenium to allow python to complete the search instead of passing in the URL of the ebay search

from bs4 import BeautifulSoup
from datetime import datetime
from tkinter import messagebox as mb
import tkinter as tk
import pandas as pd
import requests
import smtplib
import os
import re

url = 'https://www.ebay.ca/sch/i.html?_from=R40&_trksid=p2386202.m570.l1313.TR12.TRC2.A0.H0.Xt460.TRS0&_nkw=t460&_sacat=0'

headers = {'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 12499.66.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.106 Safari/537.36'}

# Set name of item to search for
wanted_item = ''

# Set price of item
# Items with a price below this threshold will not be returned
max_price = '300'

def parse_page(url):
    # Parses page with Beautiful Soup.
    # Pass in URL to parse.
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def get_price(soup):
    # Looks through HTML code to find desired info.
    # Pass in BS4 parsed HTML to be searched.
    products = soup.find_all('li', class_='sresult lvresult clearfix li')
    for product in products:
        title = product.find('h3', class_='lvtitle').text
        price_elem = product.find('li', class_='lvprice prc')
        price = price_elem.find('span', class_='bold').text
        compare_price = int(re.search(r'\d+', price).group())
        if compare_price <= int(max_price):
            form = f"{title}: {price}"
            print(form)

# WORKFLOW
# Grab element containing elements with item name and price
# Parse to separate item name and price
# Compare price to desired price threshold
# Format and append to dictionary if meets criteria



soup = parse_page(url)
get_price(soup)
""" for price in prices:
    price = prices.pop()
    print(type(price))
    price = price.split()
    if price.isdigit():
    print(price) """

