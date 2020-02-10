
# Compares items listed on a website to files currently present in a specified path.
# Method get_titles() needs to changed depending on website HTML.

from bs4 import BeautifulSoup
from datetime import datetime
from tkinter import messagebox as mb
import tkinter as tk
import requests
import os

class CompareItemsGUI(tk.Frame):

    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, **kwargs)
        self.init_window()

    def init_window(self):
        self.master.title("Compare Items")
        self.today = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # File for data to be saved in csv
        self.json_fp = 'game_scrape.json'

        # Headers for requests
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 12499.66.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.106 Safari/537.36'}

        # Create variables to be accessed
        self.url = ''
        self.item = ''

        # Flag to be used for errors
        self.error_flag = ''

        # Some page settings
        label_width = 20
        entry_width = 60
        button_width = label_width

        # Create Labels for entry fields
        l_url = tk.Label(self, width=label_width, text="Enter URL: ")
        l_item = tk.Label(self, width=label_width, text="Item Name: ")

        # Create entry fields
        self.e_url = tk.Entry(self, width=entry_width)
        self.e_item = tk.Entry(self, width=entry_width)

        # Create buttons
        b_sub = tk.Button(self, width=button_width, text="Submit", command=lambda: [run_pyscrape(), self.e_url.focus()])
        b_clear_entries = tk.Button(self, width=button_width, text="Clear entries", command=lambda: clear_entries())
        b_close = tk.Button(self, width=button_width, text="Close", command=lambda: self.quit())
        b_sub.grid(row=10, column=0)
        b_clear_entries.grid(row=11, column=0)
        b_close.grid(row=12, column=0)

        # Set up layout of label fields
        l_url.grid(row=0, column=0, sticky='w')
        l_item.grid(row=1, column=0, sticky='w')

        # Set up layout of entry fields
        self.e_url.grid(row=0, column=1)
        self.e_item.grid(row=1, column=1)

        def get_entries():
            # This function gets entries from the fields and returns them
            # as a dictionary when the submit button is pressed
            self.url = self.e_url.get()
            self.item = self.e_item.get()

        def clear_entries():
            # Repeat of get_entries that does not clear entry fields
            self.e_url.delete(0, tk.END)
            self.e_item.delete(0, tk.END)

        def parse_page(url):
            try:
                page = requests.get(url, headers=self.headers)
                soup = BeautifulSoup(page.content, 'html.parser')
                return soup
            except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema):
                self.error_flag = 'InvalidURL'

        def get_titles(soup):
            name_list = []
            sections = soup.find_all('td', class_='normal alg file-obj')
            for section in sections:
                names = section.text.strip("\n")
                name_list.append(names)
            return name_list

        def compare_files(list, path):
            # Takes in list and path.
            # Compares files in path to those in list.
            # Returns path files not present in list.
            files_1 = list
            files_2 = os.listdir(path)
            absent_files = []
            for file in files_1:
                if file not in files_2:
                    absent_files.append(file)
            return absent_files


        """ def compare_files_by_path(path_1, path_2):
        # Compares files in two folders and returns 
            files_1 = os.listdir(path_1)
            files_2 = os.listdir(path_2)
            file_list_1 = []
            file_list_2 = []
            file_dict = {}
            for file1 in files_1:
                if file1 not in files_2:
                    file_list_2.append(file1)
            for file2 in files_2:
                if file2 not in files_1:
                    file_list_2.append(file2)
            file_dict.update({path_1: file_list_1,
                            path_2: file_list_2})
            return file_dict """


        def run_pyscrape():
            get_entries()
            soup = parse_page(self.url)
            if self.error_flag == 'InvalidURL':
                mb.showinfo("Error", "Please enter a valid URL and item name.")
            elif self.error_flag == 'AttributeError':
                mb.showinfo("Error", "Please enter a valid item name.")
            elif self.error_flag == 'NoEmailInfo':
                mb.showinfo("Error", "Please enter valid email credentials.")
            else:
                names = get_titles(soup)
                need = compare_files(names, '') # ENTER PATH IN ''
                print(need)


root = tk.Tk()
app = CompareItemsGUI(root)
app.pack(fill=tk.BOTH, expand=1)
root.mainloop()

