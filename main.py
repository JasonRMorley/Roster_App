from tkinter import *

from source import date_brain
from source.date_brain import DateBrain
from source.ui import UserInterface
from source.roster import Roster


class AppController:
    def __init__(self):
        # date_brain handles everything date and line related
        self.db = DateBrain()
        self.db.load_current_line_and_week_date()
        self.current_line = self.db.current_line
        self.current_date = self.db.formatted_date
        self.search_line = None

        # roster handles everything roster related
        self.roster = Roster("files/Stagecoach_roster_38.csv")
        self.roster.load_dict()

        self.ui = None

    def set_change_line(self, new_line):
        """when called from the ui, this method will change the users current_line"""
        self.db.set_line_number(new_line)
        self.db.save_current_line_and_week_date()
        self.current_line = self.db.current_line

    def search_for_date(self, date, name):
        """when called from the UI, this Method gets the date and name from the ui,
        gets the day of the week,
        gets the search line and passes it all into a dictionary inside the roster"""
        day_of_week = date_brain.get_day_of_week(date)
        self.search_line = self.db.get_search_line(date)
        self.roster.add_to_search_dict(self.search_line, date, name, day_of_week)
        self.roster.save_dict()

    def start_app(self):
        window = Tk()
        self.ui = UserInterface(
            window,
            self.current_line,
            self.current_date,
            self.set_change_line,
            self.search_for_date,
            self.roster,
        )
        window.mainloop()


if __name__ == "__main__":
    app_controller = AppController()
    app_controller.start_app()
