# This web scraper is built to scrape ebay listings.
# Run an ebay search for your desired item, 
# and paste the URL of that search into the url variable.
# Set the max_price variable equal to the max total (price + shipping)
# that you want to pay for the item
# Items equal to or below this price threshold will be printed to screen

from bs4 import BeautifulSoup
import requests
import os
import re

# Run ebay search for the item you want, and then coopy/paste URL here
# It is set to search for Thinkpad T440p's as default, but should work for any search
url = 'https://www.ebay.ca/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313.TR12.TRC2.A0.H0.Xt440p.TRS0&_nkw=t440p&_sacat=0'

# Headers for requests module
headers = {'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 12499.66.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.106 Safari/537.36'}

# Set price of item
# Items with a price below this threshold will not be returned
max_price = '400'

def parse_page(url):
    # Parses page with Beautiful Soup.
    # Pass in URL to parse.
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def get_price(soup):
    # Looks through HTML code to find desired info.
    # Pass in BS4 parsed HTML to be searched.
    # Will find title, price, and shipping
    # Price and shipping are combined 
    # The combined price is compared against the specificed max price
    # If combined_price <= max price, formatted item info is appeneded to list
    products = soup.find_all('li', class_='sresult lvresult clearfix li')
    for product in products:
        try:
            title = product.find('h3', class_='lvtitle').text
            price_elem = product.find('li', class_='lvprice prc')
            base_price = price_elem.find('span', class_='bold').text
            ship_elem = product.find('li', class_='lvshipping')
            shipping = ship_elem.find('span', class_='ship').text.strip()
            # Remove commas so 4+ digit numbers can be converted to float
            sub_price = re.sub(r"(\d),(\d+).(\d\d)", r"\1\2.\3", base_price)
            # Find numbers in string to use for price values
            fl_price = float(re.search(r'\d+.\d\d', sub_price).group())
            fl_shipping = float(re.search(r'\d+.\d\d', shipping).group())
            # Combine base and shipping price into total price
            total_price = fl_price + fl_shipping
            total_price = round(total_price, 2)
            if total_price <= float(max_price):
                form = f"{title}\nBase price: {fl_price}\nShipping: {fl_shipping}\nTotal price: {total_price}\n\n"
                print(form)
        except AttributeError: # I cannot figure out what is causing this error
            continue

if __name__ == '__main__':
    soup = parse_page(url)
    get_price(soup)

