from datetime import datetime, date, timedelta


def get_recent_sunday(date):
    if date.weekday() == 6:  # If the date is already Sunday (weekday() returns 0 for Monday to 6 for Sunday)
        recent_sunday = date
    else:
        days_since_sunday = date.weekday() + 1
        recent_sunday = date - timedelta(days=days_since_sunday)
    return recent_sunday


def get_weekday(date):
    date_format = "%d-%m-%y"
    date_obj = datetime.strptime(date, date_format)
    weekday = date_obj.strftime("%A")
    return weekday


def format_date(date):
    formatted_date = date.strftime("%d/%m/%y")
    return formatted_date


def calculate_time_passed(start_date, end_date):
    delta = start_date - end_date
    weeks_passed = delta.days // 7
    return weeks_passed


def string_to_date(date):
    formatted_search = datetime.strptime(date, "%d/%m/%y").date()
    return formatted_search


class DateBrain:
    def __init__(self):
        self.current_line = 0
        self.search_line = 0
        self.current_date = date.today()
        self.formatted_date = self.current_date.strftime("%d/%m/%y")
        self.recent_sunday = None
        self.search_sunday = None
        self.formatted_sunday = None
        self.get_most_recent_sunday(self.current_date)

    def set_line_number(self, new_line):
        self.current_line = new_line
        print(self.current_line)

    def get_most_recent_sunday(self, date):
        if date.weekday() == 6:
            self.recent_sunday = date
        else:
            days_since_sunday = date.weekday() + 1
            self.recent_sunday = date - timedelta(days=days_since_sunday)
        self.formatted_sunday = self.recent_sunday.strftime("%d/%m/%y")

    def get_search_sunday(self, date):
        if date.weekday() == 6:
            self.search_sunday = date
        else:
            days_since_sunday = date.weekday() + 1
            self.search_sunday = date - timedelta(days=days_since_sunday)

    def save_current_line_and_week_date(self):
        with open("catch/users_info.txt", "w") as file:
            file.write(f"Line: {self.current_line}\n")
            file.write(f"Week Date: {self.formatted_sunday}\n")
        print("Data saved")

    def load_current_line_and_week_date(self):
        with open("catch/users_info.txt", "r") as file:
            lines = file.readlines()
            self.current_line = int(lines[0].strip().split(": ")[1])
            week_date_str = lines[1].strip().split(": ")[1]
            loaded_recent_sunday = datetime.strptime(week_date_str, "%d/%m/%y").date()
        self.update_line(loaded_recent_sunday)
        loaded_formatted_date = self.recent_sunday.strftime("%d/%m/%y")
        print(f"Loaded Line: {self.current_line}")
        print(f"Loaded Week Date: {self.formatted_sunday}")

    def update_line(self, loaded_date):
        delta = self.recent_sunday - loaded_date
        weeks_passed = delta.days // 7
        self.current_line += weeks_passed

    def search_date(self, date):
        formatted_search = string_to_date(date)
        search_date = get_recent_sunday(formatted_search)
        current_sunday = self.recent_sunday
        delta = search_date - current_sunday
        weeks_passed = delta.days // 7
        search_line = self.current_line + weeks_passed
        return search_line
