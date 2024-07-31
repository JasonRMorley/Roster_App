from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from roster import Roster


class UserInterface:
    def __init__(self, window, line, current_date, set_change_line, search_for_date):
        self.window = window
        self.window.title("Check a date")
        self.window.config(padx=10, pady=10)

        self.search_date = search_for_date
        self.set_change_line = set_change_line
        self.current_line = line
        self.current_date = current_date

        container = Frame(self.window)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary to hold the pages
        self.frames = {}

        for F in (HomePage, ChangeLine):
            page_name = F.__name__
            frame = F(parent=container, controller=self, line=self.current_line, date=self.current_date,
                      search_date=self.search_date)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def update_line(self, new_line):
        self.current_line = new_line
        self.set_change_line(new_line)
        self.frames['HomePage'].update_line_label(new_line)


class HomePage(Frame):
    def __init__(self, parent, controller, line, date, search_date):
        super().__init__(parent)
        self.controller = controller
        self.current_line = line
        self.current_date = date
        self.search_date = search_date
        self.df = Roster("catch/Stagecoach_roster_38.csv")
        self.df_current_line = self.df.get_current_week(self.current_line)
        self.df_previous_searches = self.df.previous_searches
        self.df.load_dict()

        # Widget frames
        self.frame_top = Frame(self)
        self.frame_top.pack(side="top", fill="both", expand=False)
        self.frame_middle_top = Frame(self)
        self.frame_middle_top.pack(side="top", fill="both", expand=True, pady=10)
        self.frame_middle = Frame(self)
        self.frame_middle.pack(side="top", fill="both", expand=True, pady=10)
        self.frame_middle_bottom = Frame(self)
        self.frame_middle_bottom.pack(side="top", fill="both", expand=True, pady=10)
        self.frame_bottom = Frame(self)
        self.frame_bottom.pack(side="top", fill="both", expand=True)

        # Widgets top
        self.label_line_number = Label(self.frame_top, text=f"Line Number: {self.current_line}", font=("Helvetica", 10))
        self.label_line_number.pack(pady=10, padx=2, side="left")

        button_line_number = Button(self.frame_top, text="change", command=lambda: controller.show_frame("ChangeLine"))
        button_line_number.pack(side="left")

        label_date = Label(self.frame_top, text=f"Date: {self.current_date}", font=("Helvetica", 10))
        label_date.pack(side="left", pady=10, padx=50)

        # Widgets middle top
        tree_current = ttk.Treeview(self.frame_middle_top, height=1)
        tree_current["columns"] = list(self.df_current_line.columns)
        tree_current["show"] = "headings"

        # Set the column headings
        for column in self.df.get_current_week(self.current_line).columns:
            tree_current.heading(column, text=column)
            tree_current.column(column, width=70)

        # Insert the data into the Treeview
        for index, row in self.df.get_current_week(self.current_line).iterrows():
            tree_current.insert("", "end", values=list(row))

        tree_current.pack()

        # Widgets middle
        self.entry_name = Entry(self.frame_middle)
        self.entry_name.pack(side="left", fill="both", expand=True)

        label_search = Label(self.frame_middle, text="Enter a date to search: ")
        label_search.pack(side="left", fill="both", expand=False)

        self.entry_search = Entry(self.frame_middle)
        self.entry_search.insert(0, "dd/mm/yy")
        self.entry_search.pack(side="left", fill="both", expand=True)
        button_search = Button(self.frame_middle, text="Search", command=self.search_button_clicked)
        button_search.pack(side="left", fill="both", expand=True)

        # Widgets middle bottom

        # Widgets bottom
        self.tree_saved = None
        self.display_recent_searches()

    def display_recent_searches(self):
        # Check if the tree_saved already exists and destroy it if it does
        if self.tree_saved:
            self.tree_saved.destroy()

        self.tree_saved = ttk.Treeview(self.frame_middle_bottom)
        self.tree_saved["columns"] = ['Name', 'Date', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                                      'Saturday']
        self.tree_saved["show"] = "headings"

        for col in self.tree_saved["columns"]:
            self.tree_saved.heading(col, text=col)
            self.tree_saved.column(col, width=100)

        self.tree_saved.pack(expand=True, fill='both')

        for line, days in self.df.previous_searches.items():
            self.tree_saved.insert("", "end", values=[line] + days)

    def update_line_label(self, new_line):
        self.label_line_number.config(text=f"Line Number: {new_line}")

    def search_button_clicked(self):
        date = self.entry_search.get()
        name = self.entry_name.get()
        self.df.add_to_search_dict(self.search_date(date), date, name)
        self.df.save_dict()
        self.display_recent_searches()


class ChangeLine(Frame):
    def __init__(self, parent, controller, line, date, search_date):
        super().__init__(parent)
        self.controller = controller
        self.current_line = line
        self.current_date = date
        self.search_date = search_date

        # Widgets
        self.line_entry = Entry(self, width=10)
        self.line_entry.pack(side="left")
        self.line_entry.insert(0, self.current_line)

        button_change_line = Button(self, text="done", command=self.change_line)
        button_change_line.pack(side="left")

        button_back = Button(self, text="Back", command=lambda: controller.show_frame("HomePage"))
        button_back.pack(side="left")

    def change_line(self):
        result = messagebox.askokcancel("update line number", f" update line number to {self.line_entry.get()}")
        if result:
            new_line = self.line_entry.get()
            self.controller.update_line(new_line)
            messagebox.showinfo("information", f"Line number updated: {new_line}")
