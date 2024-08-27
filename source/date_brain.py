from datetime import datetime, date, timedelta


def get_recent_sunday(date):
    """Sunday is the start of the week. all calculations should be done from sunday to sunday. This function will get
    the most recent sunday from the inputted date"""
    if date.weekday() == 6:  # If the date is already Sunday (weekday() returns 0 for Monday to 6 for Sunday)
        recent_sunday = date
    else:
        days_since_sunday = date.weekday() + 1
        recent_sunday = date - timedelta(days=days_since_sunday)
    return recent_sunday


def get_day_of_week(date_string):
    """Takes a date as a string then returns the day of the week"""
    # Parse the date string into a datetime object
    date_object = datetime.strptime(date_string, "%d/%m/%y")

    # Get the day of the week
    day_of_week = date_object.strftime("%A")

    return day_of_week


def format_date(original_date):
    """takes a date then formats it into the UK standard for better readability"""
    formatted_date = original_date.strftime("%d/%m/%y")
    return formatted_date


def calculate_time_passed(start_date, end_date):
    """Takes start and end date to calculate the number of weeks inbetween the two"""
    delta = start_date - end_date
    weeks_passed = delta.days // 7
    return weeks_passed


def string_to_date(date_string):
    """Converts a date from a string into a date object"""
    formatted_search = datetime.strptime(date_string, "%d/%m/%y").date()
    return formatted_search


class DateBrain:
    def __init__(self):
        self.current_line = 3801
        self.search_line = 0
        self.current_date = date.today()
        self.formatted_date = self.current_date.strftime("%d/%m/%y")
        self.recent_sunday = get_recent_sunday(self.current_date)
        self.search_sunday = None
        self.formatted_sunday = format_date(self.recent_sunday)

    def set_line_number(self, new_line):
        """sets users line number"""
        self.current_line = new_line

    def save_current_line_and_week_date(self):
        with open("../files/users_info.txt", "w") as file:
            file.write(f"Line: {self.current_line}\n")
            file.write(f"Week Date: {self.formatted_sunday}\n")
        print("Line saved")

    def load_current_line_and_week_date(self):
        try:
            with open("../files/users_info.txt", "r") as file:
                lines = file.readlines()
                self.current_line = int(lines[0].strip().split(": ")[1])
                week_date_str = lines[1].strip().split(": ")[1]
                loaded_recent_sunday = datetime.strptime(week_date_str, "%d/%m/%y").date()
            self.update_line(loaded_recent_sunday)
            loaded_formatted_date = self.recent_sunday.strftime("%d/%m/%y")
            print(f"Loaded Line: {self.current_line}")
            print(f"Loaded Week Date: {self.formatted_sunday}")
        except (FileNotFoundError, IndexError):
            print("no current line found\n default line assigned")
        finally:
            self.save_current_line_and_week_date()

    def update_line(self, loaded_date):
        """Updates the users line number"""
        delta = self.recent_sunday - loaded_date
        weeks_passed = delta.days // 7
        current_line = self.current_line + weeks_passed

        # keeps the line number within the roster's range
        if current_line > 3944:
            over = (3944 - current_line)*-1
            current_line = 3800 + over
        self.current_line = current_line

    def get_search_line(self, date_to_search):
        """
         Takes the date as a sting, formats it into a datetime date.
         gets the most recent sunday.
         finds out how many weeks has passed between current recent sunday and the recent sunday from the each day
         adds the difference to the current line and stores that into the search line
        """
        formatted_search = string_to_date(date_to_search)
        search_date = get_recent_sunday(formatted_search)
        current_sunday = self.recent_sunday
        delta = search_date - current_sunday
        weeks_passed = delta.days // 7
        search_line = self.current_line + weeks_passed
        return search_line
