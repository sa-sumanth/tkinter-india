from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
import tkintermapview

from utilities import *

from more_itertools import locate


# Definition of the pages in the application

pages = None

# Page: Welcome page
class WelcomePage(Frame):

    def __init__(self, *args, **kwargs):
        """Initialize welcome page frame"""
        Frame.__init__(self, *args, **kwargs)

    def add_page_links(self, pages, page_titles):
        """Create button links to all the pages from welcome page"""
        for ind, page in enumerate(pages):
            Button(self, text=page_titles[ind], width=40, anchor="w", command=page.lift).grid(row=ind+1, column=0)


# Page: Find capital of states and vice versa
class Page1(Frame):

    def __init__(self, *args, **kwargs):
        """Initialize page 1 frame"""
        Frame.__init__(self, *args, **kwargs)
        print("Page 1: Initializing!")

        # Initialize and place widgets
        self.capital_of_state, self.state_of_capital = get_state_capital_dct()
        self.capital_text = Text(self, height=1, width=20)
        self.state_text = Text(self, height=1, width=20)
        self.capital_label = Label(self, text="")
        self.state_label = Label(self, text="")

        # Capital of state
        Label(self, text="").grid(row=0, column=0)
        Label(self, text="Enter name of the state to find its capital:").grid(row=1, column=0)
        Label(self, text="").grid(row=2, column=0)

        Label(self, text="State name").grid(row=3, column=0, sticky="w")
        self.state_text.grid(row=3, column=1, sticky="w")
        Label(self, text="").grid(row=4, column=0)

        Button(self, text="Find Capital", command=lambda: self.get_state_capital("capital")).grid(row=5, column=0, sticky="e")
        Label(self, text="").grid(row=6, column=0)
        self.capital_label.grid(row=7, column=0, columnspan=5, sticky="w")
        Label(self, text="").grid(row=8, column=0)

        # State of capital
        Label(self, text="").grid(row=9, column=0)
        Label(self, text="Enter name of the capital to find its state:").grid(row=10, column=0)
        Label(self, text="").grid(row=11, column=0)

        Label(self, text="Capital name").grid(row=12, column=0, sticky="w")
        self.capital_text.grid(row=12, column=1, sticky="w")
        Label(self, text="").grid(row=13, column=0)

        Button(self, text="Find State", command=lambda: self.get_state_capital("state")).grid(row=14, column=0, sticky="e")
        Label(self, text="").grid(row=15, column=0)
        self.state_label.grid(row=16, column=0, columnspan=5, sticky="w")

        print("Page 1: Rendering Complete!")

    def get_state_capital(self, get_type="capital"):
        """Method to return the state of a capital or the capital of a state based on xlsx data"""
        txt = "An error occurred while getting the {0}. Please try again!".format(get_type)
        input = ""
        self.state_label.config(text="")
        self.capital_label.config(text="")
        try:
            if get_type == "capital":
                input = self.state_text.get(1.0, "end-1c").strip().title()
                if self.capital_of_state.__contains__(input):
                    txt = "The capital of {0} is {1}.".format(input, self.capital_of_state[input])
            elif get_type == "state":
                input = self.capital_text.get(1.0, "end-1c").strip().title()
                if self.state_of_capital.__contains__(input):
                    txt = "{0} is the capital of {1}.".format(input, self.state_of_capital[input])
        except Exception as e:
            pass

        if get_type == "capital":
            self.capital_label.config(text=txt)
        elif get_type == "state":
            self.state_label.config(text=txt)
        
        self.state_text.delete(1.0, "end-1c")
        self.capital_text.delete(1.0, "end-1c")

    def reset_page(self):
        """Method to reset page 1 widgets"""
        self.capital_text.delete(1.0, "end-1c")
        self.state_text.delete(1.0, "end-1c")
        self.capital_label.config(text="")
        self.state_label.config(text="")


# Page: Table of states and cities grouped by categories
class Page2(Frame):

    def __init__(self, *args, **kwargs):
        """Initialize page 2 frame"""
        Frame.__init__(self, *args, **kwargs)
        print("Page 2: Initializing!")

        # Configure frame options and style
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=7)
        s = ttk.Style()
        s.theme_use('winnative')
        # ('winnative', ', 'default', 'classic', 'vista', 'xpnative')

        # Initialize and place widgets
        self.input = Text(self, height=1, width=20)
        self.button = Button(self, text="Find", width=10, command=self.select_row)

        self.all_data = get_all_data()
        self.columns = ["State", "Capital", "NSEW Zone", "Tier", "Population",	
                        "Development Level", "Size (in KM)", "Climate", "Rainfall (in mm)"]

        # Create table
        self.tree = ttk.Treeview(self, columns=self.columns, show='headings', height=28)
        self.id = {} # Dictionary to map state to its corresponding object in tree

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=CENTER, stretch=True, minwidth=90, width=65)

        # Add table data
        for i in range(len(self.all_data["State"])):
            temp_l = []
            for col in self.columns:
                temp_l.append(self.all_data[col][i])

            self.id[self.all_data["State"][i]] = self.tree.insert('', END, values=temp_l)

        # Initialize and configure scrollbars
        scrollbarx = ttk.Scrollbar(self, orient=HORIZONTAL)
        scrollbary = ttk.Scrollbar(self, orient=VERTICAL)
        scrollbarx.configure(command=self.tree.xview)
        scrollbary.configure(command=self.tree.yview)
        self.tree.configure(xscrollcommand=scrollbarx.set, yscrollcommand=scrollbary.set)
        
        self.input.grid(row=1, column=0, pady=10)
        self.button.grid(row=1, column=2, pady=10, sticky="w")
        Label(self, text="").grid(row=2, column=0)

        self.tree.grid(row=3, column=0, sticky='nsew', columnspan=3)
        scrollbarx.grid(row=20, column=0, sticky='ew', columnspan=5)
        scrollbary.grid(row=3, column=3, sticky='ns')

        print("Page 2: Rendering Complete!")

    def select_row(self):
        """Method to make row selections"""
        for i in self.tree.selection():
            self.tree.selection_remove(i)
        data = self.input.get(1.0, "end-1c").strip().lower()

        index_list = []
        if data:
            for col in self.columns:
                ind = locate(self.all_data[col], lambda x: str(x).strip().lower() == data)
                index_list.extend(ind)

        if list(set(index_list)):
            for i in list(set(index_list)):
                self.tree.selection_add(self.id[self.all_data["State"][i]])

    def reset_page(self):
        """Method to reset page 2 widgets"""
        self.input.delete(1.0, "end-1c")
        for i in self.tree.selection():
            self.tree.selection_remove(i)


# Page: Find out about a city
class Page3(Frame):

    def __init__(self, *args, **kwargs):
        """Initialize page 3 frame"""
        Frame.__init__(self, *args, **kwargs)
        print("Page 3: Initializing!")

        # Initialize and place widgets
        self.input = Text(self, height=1, width=20)
        self.button = Button(self, text="Find city", width=10, command=self.get_city_info)
        self.result_text = Text(self, height=35, width=80, state=DISABLED, wrap=WORD)
        self.label = Label(self, text="An error occurred while getting info. Please try again!")
        self.city_data = get_city_data()

        Label(self, text="").grid(row=0, column=0)
        Label(self, text="Find information about a city:").grid(row=1, column=0, sticky="w")
        Label(self, text="").grid(row=2, column=0)

        self.button.grid(row=3, column=1, padx=10, sticky="w")
        self.input.grid(row=3, column=0, padx=10, sticky="w")
        Label(self, text="").grid(row=4, column=0, padx=10)
        Label(self, text="").grid(row=4, column=1)

        print("Page 3: Rendering Complete!")

    def get_city_info(self, city_name=None):
        """Method to display information about the input city
        Input city can be from the page itself or from page 5 map markers"""
        city = self.input.get(1.0, "end-1c").strip().title() if not city_name else city_name

        self.input.delete(1.0, "end-1c")
        self.result_text.grid_forget()
        self.label.grid_forget()
        self.result_text.config(state=NORMAL)
        self.result_text.delete(1.0, "end-1c")

        if self.city_data.__contains__(city):
            self.result_text.insert(END, "City: " + city + "\n\n")
            self.result_text.insert(END, "Languages Spoken: " + self.city_data[city]["Languages Spoken"] + "\n\n")
            self.result_text.insert(END, "Food: " + self.city_data[city]["Food"] + "\n\n")
            self.result_text.insert(END, "Tourist Places: " + self.city_data[city]["Tourist Places"])
            self.result_text.grid(row=5, column=0, columnspan=35, padx=10, sticky="w")
        else:
            self.label.grid(row=5, column=0, columnspan=20, sticky="w")

        self.result_text.config(state=DISABLED)


    def reset_page(self):
        """Method to reset page 3 widgets"""
        self.input.delete(1.0, "end-1c")
        self.result_text.grid_forget()
        self.label.grid_forget()


# Page: Find distance between two cities
class Page4(Frame):

    def __init__(self, *args, **kwargs):
        """Initialize page 4 frame"""
        Frame.__init__(self, *args, **kwargs)
        print("Page 4: Initializing!")

        # Initialize and place widgets
        self.input1 = Text(self, height=1, width=20)
        self.input2 = Text(self, height=1, width=20)
        self.label = Label(self, text="")

        Label(self, text="").grid(row=0, column=0)
        Label(self, text="Enter city names to find the distance between them:").grid(row=1, column=0)
        Label(self, text="").grid(row=2, column=0)

        Label(self, text="City 1").grid(row=3, column=0, sticky="w")
        self.input1.grid(row=3, column=1, sticky="w")
        Label(self, text="").grid(row=4, column=0)

        Label(self, text="City 2").grid(row=5, column=0, sticky="w")
        self.input2.grid(row=5, column=1, sticky="w")
        Label(self, text="").grid(row=6, column=0)

        Button(self, text="Calculate Distance", command=self.calculate_distance).grid(row=7, column=0, sticky="e")
        Label(self, text="").grid(row=8, column=0)

        self.label.grid(row=9, column=0, columnspan=5, sticky="w")

        print("Page 4: Rendering Complete!")

    def calculate_distance(self):
        """Method to calculate distance between two cities"""
        txt = "An error occurred while calculating distance. Please try again!"
        try:
            if self.input1.get(1.0, "end-1c") and self.input2.get(1.0, "end-1c"):
                res = get_distance_bw_cities(self.input1.get(1.0, "end-1c"), self.input2.get(1.0, "end-1c"))
                txt = "The distance between {0} and {1} is {2} km.".format(self.input1.get(1.0, "end-1c").strip().title(), 
                                                                           self.input2.get(1.0, "end-1c").strip().title(),
                                                                           res)
        except Exception as e:
            pass

        self.input1.delete(1.0, "end-1c")
        self.input2.delete(1.0, "end-1c")
        self.label.config(text=txt)

    def reset_page(self):
        """Method to reset page 4 widgets"""

        self.input1.delete(1.0, "end-1c")
        self.input2.delete(1.0, "end-1c")
        self.label.config(text="")


# Page: Map of India
class Page5(Frame):

    def __init__(self, *args, **kwargs):
        """Initialize page 5 frame"""

        Frame.__init__(self, *args, **kwargs)
        print("Page 5: Initializing!")

        # Initialize and place widgets
        self.cities_dict = {}
        self.cities = get_city_markers()
        
        # Create tkintermapview and center at India
        self.map_widget = tkintermapview.TkinterMapView(self, width=700, height=550, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)
        self.map_widget.set_zoom(5)
        self.map_widget.set_position(23.4, 82.5)

        self.set_map_markers()

        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=10)

        print("Page 5: Rendering Complete!")

    def set_map_markers(self):
        """Method to setup all city markers"""
        for city in self.cities:
            self.cities_dict[city] = geocoder.osm((city.strip().title() + ", India"))
            lat = self.cities_dict[city].lat
            lng = self.cities_dict[city].lng
            self.map_widget.set_marker(lat, lng, command=self.marker_click_event)
            self.cities_dict[lat_lng_to_str(lat, lng)] = city        

    def marker_click_event(self, marker):
        """Method to redirect to page 3: info about a city on marker click event"""
        global pages
        city = self.cities_dict[lat_lng_to_str(marker.position[0], marker.position[1])]
        pages[2].get_city_info(city)
        pages[2].lift()

    def reset_page(self):
        """Method to reset page 5 widgets"""
        pass

def set_pages(pages_list):
    """Initialize page list to global variable for use in this module"""
    global pages
    pages = pages_list