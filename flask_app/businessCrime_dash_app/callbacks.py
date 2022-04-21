from dash import Output, Input
from flask_app.businessCrime_dash_app.crimechart import CrimeChart
from flask_app.businessCrime_dash_app.crimedata import CrimeData

data = CrimeData()
data.get_data()
borough = '(All)'
major = '(All)'
minor = '(All)'
data.process_data_for_selection(borough, major, minor)


def register_callbacks(dash_app):
    # Create the callbacks
    @dash_app.callback(Output("line-chart", "figure"),
                       Output("borough-bar-chart", "figure"),
                       Output("major-bar-chart", "figure"),
                       Output("minor-bar-chart", "figure"),
                       Output("map-chart", "figure"),
                       Input("borough-select", "value"),
                       Input("major-select", "value"),
                       Input("minor-select", "value"))
    def update_chart(borough_select, major_select, minor_select):
        data.get_data()
        data.process_data_for_selection(borough_select, major_select, minor_select)
        linechart = CrimeChart(data).create_line_chart(borough_select, major_select, minor_select)
        borough_barchart = CrimeChart(data).create_borough_bar_chart(borough_select, major_select, minor_select)
        major_barchart = CrimeChart(data).create_major_crime_bar_chart(borough_select, major_select, minor_select)
        minor_barchart = CrimeChart(data).create_minor_crime_bar_chart(borough_select, major_select, minor_select)
        map = CrimeChart(data).create_borough_map(borough_select)
        return linechart, borough_barchart, major_barchart, minor_barchart, map

    @dash_app.callback(Output("minor-select", "options"),
                       Output("minor-select", "value"),
                       Input("borough-select", "value"),
                       Input("major-select", "value"))
    def update_minor_dropdown_list(borough_select, major_select):
        data.get_data()
        list = data.process_minor_dropdown_list(borough_select, major_select)
        options = [{"label": x, "value": x} for x in list]
        value = "(All)"
        return options, value
