from bs4 import BeautifulSoup
from datetime import datetime
from tkinter import messagebox as mb
import tkinter as tk
import pandas as pd
import requests
import smtplib
import os
import re

class PyScrapeGUI(tk.Frame):
    
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, **kwargs)
        self.init_window()
        self.totals_list = []

    def init_window(self):
        self.master.title("Ebay Scraper")

        # Headers for requests
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 12499.66.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.106 Safari/537.36'}

        # Create variables to be accessed
        self.url = ''
        self.max_price = ''
        self.add = ''
        self.pw = ''
        self.rec = ''

        # Flag to be used for errors
        self.error_flag = ''

        # Some page settings
        label_width = 20
        entry_width = 60
        button_width = label_width

        # Create Labels for entry fields
        l_url = tk.Label(self, width=label_width, text="Enter URL: ")
        l_max = tk.Label(self, width=label_width, text="Enter max price: ")
        l_add = tk.Label(self, width=label_width, text="Enter sender's email: ")
        l_pw = tk.Label(self, width=label_width, text="Enter email password: ")
        l_rec = tk.Label(self, width=label_width, text="Enter reciever's email: ")

        # Create entry fields
        self.e_url = tk.Entry(self, width=entry_width)
        self.e_max = tk.Entry(self, width=entry_width)
        self.e_add = tk.Entry(self, width=entry_width)
        self.e_pw = tk.Entry(self, width=entry_width)
        self.e_rec = tk.Entry(self, width=entry_width)

        # Create buttons
        b_sub = tk.Button(self, width=button_width, text="Submit", command=lambda: [run_pyscrape(), self.e_url.focus()])
        b_sub_no_email = tk.Button(self, width=button_width, text="Submit w/o email", command=lambda: [run_pyscrape_no_email(), self.e_url.focus()])
        b_clear_entries = tk.Button(self, width=button_width, text="Clear entries", command=lambda: clear_entries())
        b_close = tk.Button(self, width=button_width, text="Close", command=lambda: self.quit())
        b_sub.grid(row=10, column=0)
        b_sub_no_email.grid(row=10, column=1, sticky='w')
        b_clear_entries.grid(row=11, column=0)
        b_close.grid(row=12, column=0)

        # Set up layout of label fields
        l_url.grid(row=0, column=0, sticky='w')
        l_max.grid(row=1, column=0, sticky='w')
        l_add.grid(row=2, column=0, sticky='w')
        l_pw.grid(row=3, column=0, sticky='w')
        l_rec.grid(row=4, column=0, sticky='w')

        # Set up layout of entry fields
        self.e_url.grid(row=0, column=1)
        self.e_max.grid(row=1, column=1)
        self.e_add.grid(row=2, column=1)
        self.e_pw.grid(row=3, column=1)
        self.e_rec.grid(row=4, column=1)


        def get_entries():
            # This function gets entries from the fields and returns them
            # as a dictionary when the submit button is pressed
            self.url = self.e_url.get()
            self.max_price = self.e_max.get()
            self.add = self.e_add.get()
            self.pw = self.e_pw.get()
            self.rec = self.e_rec.get()


        def clear_entries():
            # Repeat of get_entries that does not clear entry fields
            self.e_url.delete(0, tk.END)
            self.e_max.delete(0, tk.END)
            self.e_add.delete(0, tk.END)
            self.e_pw.delete(0, tk.END)
            self.e_rec.delete(0, tk.END)

        def parse_page(url):
            try:
                page = requests.get(url, headers=self.headers)
                soup = BeautifulSoup(page.content, 'html.parser')
                return soup
            except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema):
                self.error_flag = 'InvalidURL'

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
                    title = product.find('h3', class_='lvtitle').text.strip('New listing').strip()
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
                    if total_price <= float(self.max_price):
                        formatted = {"title": title,
                                        "list_price": fl_price,
                                        "shipping": fl_shipping,
                                        "total": total_price}
                        self.totals_list.append(formatted)
                except AttributeError: # I cannot figure out what is causing this error
                    continue

        def send_email(msg):
            if self.add == '' or self.pw == '' or self.rec == '':
                self.error_flag = 'NoEmailInfo'
            else:    
                with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.ehlo()
                    smtp.login(self.add, self.pw)
                    smtp.sendmail(self.add, self.rec, msg)

        def format_totals_list():
            for item in self.totals_list:
                title = item["title"]
                total = item["total"]
                list_price = item["list_price"]
                shipping = item["shipping"]
                formed_cheese = f"{title}: ${total} (list: ${list_price}, ship: ${shipping})"
                print(formed_cheese)

        def run_pyscrape():
            # Email not currently functional
            get_entries()
            soup = parse_page(self.url)
            if self.error_flag == 'InvalidURL':
                mb.showinfo("Error", "Please enter a valid URL and item name.")
            elif self.error_flag == 'AttributeError':
                mb.showinfo("Error", "Please enter a valid item name.")
            elif self.error_flag == 'NoEmailInfo':
                mb.showinfo("Error", "Please enter valid email credentials.")
            else:
                get_price(soup)


        def run_pyscrape_no_email():
            get_entries()
            soup = parse_page(self.url)
            if self.error_flag == 'InvalidURL':
                mb.showinfo("Error", "Please enter a valid URL and item name.")
            elif self.error_flag == 'AttributeError':
                mb.showinfo("Error", "Please enter a valid item name.")
            else:
                get_price(soup)
                format_totals_list()

root = tk.Tk()

app = PyScrapeGUI(root)
app.pack(fill=tk.BOTH, expand=1)
root.mainloop()
