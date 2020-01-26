from bs4 import BeautifulSoup
from datetime import datetime
import tkinter as tk
import pandas as pd
import requests
import smtplib
import os

class PyScrapeGUI(tk.Frame):

    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, **kwargs)
        self.init_window()

    def init_window(self):
        self.master.title("PyScrape")
        self.today = str(datetime.now())

        # File for data to be saved in csv
        self.csv_fp = 'pyscrape.csv'

        # Headers for requests
        self.headers = headers = {'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 12499.66.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.106 Safari/537.36'}

        # Create variables to be accessed
        self.url = ''
        self.item = ''
        self.add = ''
        self.pw = ''
        self.rec = ''

        # Some page settings
        label_width = 20
        entry_width = 60
        button_width = label_width

        # Create Labels for entry fields
        l_url = tk.Label(self, width=label_width, text="Enter URL: ")
        l_item = tk.Label(self, width=label_width, text="Item Name: ")
        l_add = tk.Label(self, width=label_width, text="Sender Email: ")
        l_pw = tk.Label(self, width=label_width, text="Sender PW: ")
        l_rec = tk.Label(self, width=label_width, text="Receiver Email: ")

        # Create entry fields
        self.e_url = tk.Entry(self, width=entry_width)
        self.e_item = tk.Entry(self, width=entry_width)
        self.e_add = tk.Entry(self, width=entry_width)
        self.e_pw = tk.Entry(self, width=entry_width)
        self.e_rec = tk.Entry(self, width=entry_width)

        # Create buttons
        b_sub = tk.Button(self, width=button_width, text="Submit", command=lambda: [get_entries(), run_pyscrape()])
        b_close = tk.Button(self, width=button_width, text="Close", command=lambda: self.quit())
        b_sub.grid(row=10, column=0)
        b_close.grid(row=11, column=0)

        # Set up layout of label fields
        l_url.grid(row=0, column=0, sticky='w')
        l_item.grid(row=1, column=0, sticky='w')
        l_add.grid(row=2, column=0, sticky='w')
        l_pw.grid(row=3, column=0, sticky='w')
        l_rec.grid(row=4, column=0, sticky='w')

        # Set up layout of entry fields
        self.e_url.grid(row=0, column=1)
        self.e_item.grid(row=1, column=1)
        self.e_add.grid(row=2, column=1)
        self.e_pw.grid(row=3, column=1)
        self.e_rec.grid(row=4, column=1)


        def get_entries():
            """This function gets entries from the fields and returns them
            as a dictionary when the submit button is pressed"""
            self.url = self.e_url.get()
            self.item = self.e_item.get()
            self.add = self.e_add.get()
            self.pw = self.e_pw.get()
            self.rec = self.e_rec.get()
            self.e_url.delete(0, tk.END)
            self.e_item.delete(0, tk.END)
            self.e_add.delete(0, tk.END)
            self.e_pw.delete(0, tk.END)
            self.e_rec.delete(0, tk.END)

        def parse_page(url):
            page = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            return soup

        def get_price(soup):
            products = soup.find_all('div', class_='product')
            for product in products:
                title = product.find('div', class_='title').get_text().strip()
                price = product.find('div', class_='price').get_text().strip()
                if self.item in title:
                    return price
            else:
                return 'not listed'

        def send_email(msg):
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(self.add, self.pw)   

                subj = 'PyScrape Update'
                body = msg

                smtp.sendmail(self.add, self.rec, msg)

        def make_pandas(price):
            data_layout = [[self.item, price, self.today]]
            df = pd.DataFrame(data_layout, columns = ['Item', 'Price', 'Date'])
            make_file = df.to_csv(self.csv_fp, mode='a', header=True)

        def append_pandas(price):
            data_layout = [[self.item, price, self.today]]
            df = pd.DataFrame(data_layout)
            append_csv = df.to_csv(self.csv_fp, mode='a', header=False)

        def run_pyscrape():
            soup = parse_page(self.url)
            price = get_price(soup)
            formatted_info = f"{self.item} is {price} on {self.today}"
            print(formatted_info)
            if not os.path.isfile(self.csv_fp):
                make_pandas(price)
            else:    
                append_pandas(price)
            send_email("\n" + formatted_info)

root = tk.Tk()

app = PyScrapeGUI(root)
app.pack(fill=tk.BOTH, expand=1)
root.mainloop()

