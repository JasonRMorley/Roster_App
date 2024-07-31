import pandas as pd
import ast


class Roster:
    def __init__(self, csv_path):
        # Read CSV and create a dictionary
        self.data = pd.read_csv(csv_path)
        self.data_dict = {
            row.Line: [row.Sunday, row.Monday, row.Tuesday, row.Wednesday, row.Thursday, row.Friday, row.Saturday]
            for (index, row) in self.data.iterrows()}

        # Convert the dictionary to a DataFrame with headers
        self.roster_df = pd.DataFrame.from_dict(self.data_dict, orient='index',
                                                columns=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
                                                         'Friday',
                                                         'Saturday'])
        self.previous_searches = {}

    def get_current_week(self, line):
        # Append the row corresponding to the line number to previous searches
        previous_search = self.data_dict.get(str(line), 'Line not found')

        # Return a DataFrame with the single row or error message
        return pd.DataFrame([previous_search], columns=self.roster_df.columns,
                            index=[line]) if previous_search != 'Line not found' else previous_search

    def add_to_search_dict(self, line, date, name, day_of_week):

        search = [date, day_of_week] + self.data_dict.get(str(line), 'Line not found')

        # If the line exists, save the search
        if search != 'Line not found':
            self.previous_searches[f"{name}"] = search
            print(self.previous_searches)

    def save_dict(self):
        with open("previous_search.txt", "w") as file:
            file.write(str(self.previous_searches))
            print("previous searches saved")

    def load_dict(self):
        with open("previous_search.txt", "r") as file:
            lines = file.readlines()
            dict_load = {}
            for line in lines:
                line_dict = ast.literal_eval(line.strip())
                dict_load.update(line_dict)
            print(dict_load)
            self.previous_searches = dict_load
            print("previous searches loaded")
