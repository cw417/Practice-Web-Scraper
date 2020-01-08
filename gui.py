import tkinter as tk
import json

class ScrapeGUI(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)                 
        self.master = master
        self.init_window()

    def init_window(self):
  
        self.master.title("Web Scrape GUI")

        
        self.pack(fill=tk.BOTH, expand=1)

        label_width = 20
        entry_width = 60
        button_width = label_width

        def get_entries():
            """This function gets entries from the fields and returns them
            as a dictionary when the submit button is pressed"""
            dict = {}

            url = e_url.get()
            dict.update({'url': url})
            item = e_item.get()
            dict.update({'wanted_item': item})
            add = e_add.get()
            dict.update({'email_address': add})
            pw = e_pw.get()
            dict.update({'email_pw': pw})
            rec = e_rec.get()
            dict.update({'email_receive': rec})

            dict_file = json.dump(dict, open("pyscrape_dict.json", 'w'))

        # Create Labels for entry fields
        l_url = tk.Label(self, width=label_width, text="Enter URL: ")
        l_item = tk.Label(self, width=label_width, text="Item Name: ")
        l_add = tk.Label(self, width=label_width, text="Sender Email: ")
        l_pw = tk.Label(self, width=label_width, text="Sender PW: ")
        l_rec = tk.Label(self, width=label_width, text="Receiver Email: ")

        # Create entry fields
        e_url = tk.Entry(self, width=entry_width)
        e_item = tk.Entry(self, width=entry_width)
        e_add = tk.Entry(self, width=entry_width)
        e_pw = tk.Entry(self, width=entry_width)
        e_rec = tk.Entry(self, width=entry_width)

        # Create buttons for edit headers and submit
        b_sub = tk.Button(self, width=button_width, text="Submit", command=get_entries)

        # Set up layout of label fields
        l_url.grid(row=0, column=0, sticky='w')
        l_item.grid(row=1, column=0, sticky='w')
        l_add.grid(row=2, column=0, sticky='w')
        l_pw.grid(row=3, column=0, sticky='w')
        l_rec.grid(row=4, column=0, sticky='w')

        # Set up layout of entry fields
        e_url.grid(row=0, column=1)
        e_item.grid(row=1, column=1)
        e_add.grid(row=2, column=1)
        e_pw.grid(row=3, column=1)
        e_rec.grid(row=4, column=1)

        # Set up layout of buttons
        # Starts at 10 to enable later addition of extra entry fields
        b_sub.grid(row=10, column=0)

root = tk.Tk()

root.geometry("600x127")

app = ScrapeGUI(root)
root.mainloop()

