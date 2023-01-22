from tkinter import *
from pages import *
from utilities import *


class MainView(Frame):

    def __init__(self, *args, **kwargs):
        """Initialize main view frame"""
        Frame.__init__(self, *args, **kwargs)

        # Create main containers
        self.top_frame = Frame(self)    # Frame for homepage button
        self.page_frame = Frame(self)   # Frame for all pages

        self.top_frame.pack(side="top", fill="x", expand=False)
        self.page_frame.pack(side="top", fill="both", expand=True)

        # Create page frames
        self.page_titles = ["Find capital of states and vice versa",
                            "Table of states and cities grouped by categories",
                            "Find out about a city",
                            "Find distance between two cities",
                            "Map of India"]
        
        get_xlsx_data()

        self.pages = [Page1(self), Page2(self), Page3(self), Page4(self), Page5(self)]
        set_pages(self.pages)

        # Create welcome page frame
        self.welcome_page = WelcomePage(self)
        self.welcome_page.add_page_links(self.pages, self.page_titles)

        # Place pages in the page frame container
        self.welcome_page.place(in_=self.page_frame, x=0, y=0, relwidth=1, relheight=1)
        for page in self.pages:
            page.place(in_=self.page_frame, x=0, y=0, relwidth=1, relheight=1)

        # Create welcome page button and initialize welcome page on startup
        Button(self.top_frame, text="Project India", command=self.show_welcome_page).pack(side="top", fill="x", expand=True)

        self.welcome_page.lift()

    def show_welcome_page(self):
        """Method to display welcome page"""
        for page in self.pages:
            page.reset_page()

        self.welcome_page.lift()
        

if __name__ == '__main__':
    # Initialize root, main view object and start mainloop
    root = Tk()
    root.wm_geometry("670x750")
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()