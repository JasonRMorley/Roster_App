from tkinter import *

import date_brain
from date_brain import DateBrain
from ui import UserInterface
from roster import Roster


class AppController:
    def __init__(self):
        self.db = DateBrain()
        self.db.load_current_line_and_week_date()

        self.current_line = self.db.current_line
        self.current_date = self.db.formatted_date

        self.roster = Roster("catch/Stagecoach_roster_38.csv")
        self.ui = None

    def set_change_line(self, new_line):
        self.db.set_line_number(new_line)
        self.db.save_current_line_and_week_date()
        self.current_line = self.db.current_line
        self.ui.update_line(self.current_line)

    def search_for_date(self, date, name):
        day_of_week = date_brain.get_day_of_week(date)
        return self.db.search_date(date)

    def start_app(self):
        window = Tk()
        self.ui = UserInterface(
            window,
            self.current_line,
            self.current_date,
            self.set_change_line,
            self.search_for_date,
        )
        window.mainloop()


if __name__ == "__main__":
    app_controller = AppController()
    app_controller.start_app()
