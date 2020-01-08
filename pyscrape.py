import requests
import smtplib
import json
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date
import gui

# Set up dictionary to hold entries from GUI
json_fp = 'pyscrape_dict.json'

def get_dict(json_fp):
    with open(json_fp) as json_data:
        pyscrape_dict = json.load(json_data)
        json_data.close()
        return pyscrape_dict

entry_dict = get_dict(json_fp)

# URL of website
# Scrapey currently only works for the webtsite it was written for, listed below:
# TEST URL: 'https://www.schiit.com/b-stocks'
url = entry_dict["url"]

# Name of item to check for 
# TEST ITEMS: 
    # 'Asgard 2' - an item that is currently listed on the website
    # 'Yggdrasil' - an item that Schiit currently sells, but that is not yet listed on the website. Will return 'not listed'.
wanted_item = entry_dict["wanted_item"]

# Info for BeautifulSoup4 - change as needed
headers = {'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 12499.66.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.106 Safari/537.36'}

# Login & receiver info for smtp
email_address = entry_dict["email_address"]
email_pw = entry_dict["email_pw"]
email_receive = entry_dict["email_receive"]

# Save pandas csv in current working directory
new_file = open("pyscrape_info.csv", 'a')
csv_filepath = new_file

def parse_page(url):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def get_title_price(soup):
    products = soup.find_all('div', class_='product')
    for product in products:
        title = product.find('div', class_='title').get_text().strip()
        price = product.find('div', class_='price').get_text().strip()
        if wanted_item in title:
            return [title, price]
    else:
        return [wanted_item, 'not listed']

def format_info(title, price):
    info = f"{title} is {price} on {date.today()}"
    return info

def send_email(msg):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(email_address, email_pw)   

        subj = 'PyScrape Update'
        body = msg

        smtp.sendmail(email_address, email_receive, msg)

def make_pandas(title, price, csv_filepath):
    data = [[title, price, date.today()]]
    df = pd.DataFrame(data, columns = ['Item', 'Price', 'Date'])
    append_csv = df.to_csv(csv_filepath, mode='a', header=False)

if __name__ == '__main__':
    soup = parse_page(url)
    title_price = get_title_price(soup)
    make_pandas(title_price[0], title_price[1], csv_filepath)
    formatted_info = format_info(title_price[0], title_price[1])
    print(formatted_info)
    send_email(formatted_info)