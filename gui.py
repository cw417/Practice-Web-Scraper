from tkinter import *
import json

class PyScrapeGUI(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master
        self.init_window()

    def init_window(self):
  
        self.master.title("PyScrape GUI")

        
        self.pack(fill=BOTH, expand=1)

        label_width = 20
        entry_width = 60
        button_width = label_width

        def get_entries():
            """This function gets entries from the fields and returns them
            as a dictionary in a JSON file when the submit button is pressed"""
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

            dict_file = json.dump(dict, open("piescrape_dict.json", 'w'), indent=4, sort_keys=True)

        # Create Labels for entry fields
        l_url = Label(self, width=label_width, text="Enter URL: ")
        l_item = Label(self, width=label_width, text="Item Name: ")
        l_add = Label(self, width=label_width, text="Sender Email: ")
        l_pw = Label(self, width=label_width, text="Sender PW: ")
        l_rec = Label(self, width=label_width, text="Receiver Email: ")

        # Create entry fields
        e_url = Entry(self, width=entry_width)
        e_item = Entry(self, width=entry_width)
        e_add = Entry(self, width=entry_width)
        e_pw = Entry(self, width=entry_width)
        e_rec = Entry(self, width=entry_width)

        # Create submit button
        b_sub = Button(self, width=button_width, text="Submit", command=get_entries)

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

        # Set up button layout
        # Starts at 10 to enable later addition of more entry fields
        b_sub.grid(row=10, column=0)

root = Tk()

root.geometry("600x127")

app = PyScrapeGUI(root)
root.mainloop()

