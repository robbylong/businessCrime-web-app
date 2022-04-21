from pathlib import Path
import json
import pandas as pd


class CrimeData:
    """Class for retrieving and structuring the data.
    """

    def __init__(self):
        self.crime = pd.DataFrame()
        self.borough_list = []
        self.major_list = []
        self.minor_list = []
        self.borough_dropdown_list = []
        self.major_dropdown_list = []
        self.minor_dropdown_list = []
        self.minor_dropdown_list_common = []
        self.months = []
        self.line_chart_data = []
        self.borough_bar_chart_data = []
        self.major_bar_chart_data = []
        self.minor_bar_chart_data = []
        self.map_df = []

    def get_data(self):
        csvfile = Path(__file__).parent.joinpath('data', 'dataset_with_geo.csv')
        self.crime = pd.read_csv(csvfile)
        file_path = Path(__file__).parent.joinpath('data', 'england_lad_2011.geojson')
        with open(file_path) as json_file:
            self.la_geojson = json.load(json_file)
        self.borough_list = self.crime["Borough"].unique().tolist()
        self.geo_code_list = self.crime["GEO_CODE"].unique().tolist()
        self.borough_dropdown_list = self.crime["Borough"].unique().tolist()
        self.major_list = self.crime["Major Class Description"].unique().tolist()
        self.major_dropdown_list = self.crime["Major Class Description"].unique().tolist()
        self.minor_list = self.crime["Minor Class Description"].unique().tolist()
        # self.minor_dropdown_list = self.crime["Minor Class Description"].unique().tolist()
        self.borough_dropdown_list.insert(0, "(All)")
        self.major_dropdown_list.insert(0, "(All)")
        # Create a list of column names (lists of Months covered) in the crime data
        self.months = sorted(self.crime)
        # Remove unnecessary column names from the list
        self.months.remove('Borough')
        self.months.remove('Major Class Description')
        self.months.remove('Minor Class Description')

    def process_minor_dropdown_list(self, borough, major):
        """Method for dashboard minor dropdown list
            it is necessary because in dataset
            the minor class description for each London borough may be different
        """
        if borough == "(All)":
            if major == "(All)":
                self.minor_dropdown_list = self.minor_list
            else:
                self.crime_minor_list = self.crime.groupby(["Major Class Description", "Minor Class Description"]).sum()
                self.minor_dropdown_list = list(self.crime_minor_list.loc[major].index)
        else:
            if major == "(All)":
                self.crime_minor_list = self.crime.groupby(["Borough", "Minor Class Description"]).sum()
                self.minor_dropdown_list = list(self.crime_minor_list.loc[borough].index)

            else:
                self.crime_minor_list = self.crime.groupby(
                    ["Borough", "Major Class Description", "Minor Class Description"]).sum()
                self.minor_dropdown_list = list(self.crime_minor_list.loc[borough].loc[major].index)
        if self.minor_dropdown_list[0] != "(All)":
            self.minor_dropdown_list.insert(0, "(All)")
        return self.minor_dropdown_list

    def obtain_major_from_minor(self, minor):
        self.major_minor = self.crime.groupby(["Major Class Description", "Minor Class Description"]).sum()
        # print(len(self.create_dic.loc["Burglary"].index))
        for i in range(len(self.major_minor.index)):
            major = self.major_list[i]
            for j in range(len(self.major_minor.loc[major].index)):
                if minor == self.major_minor.loc[major].index[j]:
                    return major

    def process_data_for_selection(self, borough, major, minor):
        # Prepare dataframe for line charts
        self.crime = self.crime.groupby(["Borough", "Major Class Description", "Minor Class Description"]).sum()
        if borough == "(All)":
            if major == "(All)":
                if minor == "(All)":
                    self.line_chart_data = self.crime.sum()
                else:
                    self.line_chart_data = self.crime.groupby(["Minor Class Description"]).sum()
                    self.line_chart_data = self.line_chart_data.loc[minor]
            else:
                if minor == "(All)":
                    self.line_chart_data = self.crime.groupby(["Major Class Description"]).sum()
                    self.line_chart_data = self.line_chart_data.loc[major]
                else:
                    self.line_chart_data = self.crime.groupby(
                        ["Major Class Description", "Minor Class Description"]).sum()
                    self.line_chart_data = self.line_chart_data.loc[major].loc[minor]
        else:
            if major == "(All)":
                if minor == "(All)":
                    # Crime cases for a specific borough with all major minors
                    self.line_chart_data = self.crime.loc[borough].sum()
                else:
                    self.line_chart_data = self.crime.loc[borough].groupby(["Minor Class Description"]).sum()
                    self.line_chart_data = self.line_chart_data.loc[minor]
            else:
                if minor == "(All)":
                    self.line_chart_data = self.crime.loc[borough].loc[major].sum()
                else:
                    # Crime cases for a specific borough, major and minor
                    self.line_chart_data = self.crime.loc[borough].loc[major].loc[minor]

        # Prepare dataframe for borough bar charts
        if major == "(All)":
            if minor == "(All)":
                self.borough_bar_chart_data = self.crime.groupby(["Borough"]).sum()
            else:
                self.borough_bar_chart_data = self.crime.groupby(["Minor Class Description", "Borough"]).sum()
                self.borough_bar_chart_data = self.borough_bar_chart_data.loc[minor]
                self.borough_list = list(self.borough_bar_chart_data.index)
        else:
            if minor == "(All)":
                self.borough_bar_chart_data = self.crime.groupby(["Major Class Description", "Borough"]).sum()
                self.borough_bar_chart_data = self.borough_bar_chart_data.loc[major]
            else:
                self.borough_bar_chart_data = self.crime.groupby(
                    ["Major Class Description", "Minor Class Description", "Borough"]).sum()
                self.borough_bar_chart_data = self.borough_bar_chart_data.loc[major].loc[minor]
                self.borough_list = list(self.borough_bar_chart_data.index)

        # Prepare dataframe for major and minor bar chart
        if borough != "(All)":
            self.crime = self.crime.groupby(["Borough", "Major Class Description", "Minor Class Description"]).sum()
            self.crime = self.crime.loc[borough]
        if major == "(All)":
            if minor == "(All)":
                self.major_bar_chart_data = self.crime.groupby(["Major Class Description"]).sum()
                self.major_bar_chart_list = list(self.major_bar_chart_data.index)
                self.minor_bar_chart_data = self.crime.groupby(["Minor Class Description"]).sum()
                self.minor_bar_chart_list = list(self.minor_bar_chart_data.index)
            else:
                self.major_bar_chart_data = self.crime.groupby(["Minor Class Description"]).sum()
                self.major_bar_chart_data = self.major_bar_chart_data.loc[minor]
                self.minor_bar_chart_data = self.major_bar_chart_data
                self.minor_bar_chart_list = [minor]
        else:
            if minor == "(All)":
                self.major_bar_chart_data = self.crime.groupby(["Major Class Description"]).sum()
                self.major_bar_chart_data = self.major_bar_chart_data.loc[major]
                self.major_bar_chart_list = [major]
                self.minor_bar_chart_data = self.crime.groupby(
                    ["Major Class Description", "Minor Class Description"]).sum()
                self.minor_bar_chart_data = self.minor_bar_chart_data.loc[major]
                self.minor_bar_chart_list = list(self.minor_bar_chart_data.index)
            else:
                self.major_bar_chart_data = self.crime.groupby(
                    ["Major Class Description", "Minor Class Description"]).sum()
                self.major_bar_chart_data = self.major_bar_chart_data.loc[major].loc[minor]
                self.major_bar_chart_list = [major]
                self.minor_bar_chart_data = self.major_bar_chart_data
                self.minor_bar_chart_list = [minor]
