import plotly.graph_objects as go
from flask_app.businessCrime_dash_app.crimedata import CrimeData


class CrimeChart:
    """ Creates the crime charts to be used in the dashboard"""

    def __init__(self, data):
        self.data = data
        self.colors = ['#ff9da7', '#9c755f', '#f28e2b', '#4e79a7', '#e15759', '#edc948', '#b07aa1',
                       '#59a14f', '#d0e6e4']

    def create_line_chart(self, borough, major, minor):
        y = []
        month = self.data.months
        y = self.data.line_chart_data
        chart = go.Scatter(x=month, y=y,
                           mode='lines',
                           line=dict(color='firebrick', width=4))
        # Create the layout
        layout = go.Layout(showlegend=False, plot_bgcolor="#ffffff")

        # Create the figure
        figure = go.Figure(layout=layout)

        # Update the figure and add the traces
        figure.add_trace(chart)

        # Update the layout of the axes to look a little closer to the original chart we are copyin
        figure.update_layout(title='Business crime London' + " - " + borough + " - " + major + " - " + minor)
        figure.update_layout(height=300)
        figure.update_yaxes(title_font=dict(size=14, color='#CDCDCD'),
                            tickfont=dict(color='#666666', size=20), ticksuffix="",
                            showgrid=True, gridwidth=1, gridcolor='#CDCDCD',
                            tick0=min(y), nticks=5)
        figure.update_xaxes(title='Year/Month', tickangle=45, tickfont=dict(color='#666666', size=10),
                            showline=True, linewidth=2, linecolor='#CDCDCD')

        return figure

    def create_borough_bar_chart(self, borough, major, minor):
        y = []
        if borough == "(All)":
            Boroughs = self.data.borough_list
            chart_data = self.data.borough_bar_chart_data
            for i in range(len(Boroughs)):
                y.append(chart_data.loc[Boroughs[i]].sum())
        else:
            Boroughs = [borough]
            chart_data = self.data.borough_bar_chart_data.loc[borough].sum()
            y = [chart_data]
        chart = go.Bar(x=Boroughs, y=y, marker_color='#5283b0')
        # Create the layout
        layout = go.Layout(showlegend=False, plot_bgcolor="#ffffff")
        # Create the figure
        figure = go.Figure(layout=layout)
        # Update the figure and add the traces
        figure.add_trace(chart)
        # Update the layout of the axes so that bar chart is in descending order, the column with greatest value is on the left
        figure.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'}, height=400)
        figure.update_yaxes(title_font=dict(size=14, color='#CDCDCD'),
                            tickfont=dict(color='#666666', size=20), ticksuffix="",
                            showgrid=True, gridwidth=1, gridcolor='#CDCDCD',
                            tick0=min(y), nticks=5)
        figure.update_xaxes(title='London Borough', tickangle=45, tickfont=dict(color='#666666', size=10),
                            showline=True, linewidth=2, linecolor='#CDCDCD')

        return figure

    def create_major_crime_bar_chart(self, borough, major, minor):
        y = []
        majors = self.data.major_bar_chart_list
        if major == "(All)":
            if minor == "(All)":
                chart_data = self.data.major_bar_chart_data
                for i in range(len(majors)):
                    y.append(chart_data.loc[majors[i]].sum())
            else:
                majors = [self.data.obtain_major_from_minor(minor)]
                chart_data = self.data.major_bar_chart_data
                y = [chart_data.sum()]
        else:
            chart_data = self.data.major_bar_chart_data
            y = [chart_data.sum()]
        # Create the layout
        layout = go.Layout(showlegend=False, plot_bgcolor="#ffffff")
        if len(y) > 1:
            chart = go.Bar(x=majors, y=y,
                           marker_color=self.colors, width=0.9)
        else:
            position = self.data.major_list.index(majors[0])
            color = self.colors[position]
            chart = go.Bar(x=majors, y=y,
                           marker_color=color, width=0.9)
        # Create the figure
        figure = go.Figure(layout=layout)

        # Update the figure and add the traces
        figure.add_trace(chart)

        figure.update_layout(title="Major Class Description", height=350)
        # Update the layout of the axes so that bar chart is in descending order, the column with greatest value is on the left
        figure.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
        figure.update_yaxes(title_font=dict(size=14, color='#CDCDCD'),
                            tickfont=dict(color='#666666', size=20), ticksuffix="",
                            showgrid=True, gridwidth=1, gridcolor='#CDCDCD',
                            tick0=min(y), nticks=5)
        figure.update_xaxes(tickangle=45, tickfont=dict(color='#666666', size=8),
                            showline=True, linewidth=2, linecolor='#CDCDCD')

        return figure

    def create_minor_crime_bar_chart(self, borough, major, minor):
        y = []
        x = []
        cases = []
        minors = self.data.minor_bar_chart_list
        if major == "(All)":
            majors = self.data.major_bar_chart_list
            if minor == "(All)":
                chart_data = self.data.minor_bar_chart_data
                for i in range(len(minors)):
                    y.append(chart_data.loc[minors[i]].sum())
            else:
                chart_data = self.data.minor_bar_chart_data
                y = [chart_data.sum()]
            # Create the layout
            layout = go.Layout(showlegend=False, plot_bgcolor="#ffffff")
            # Create the figure
            figure = go.Figure(layout=layout)
            for a in range(len(majors)):
                for b in range(len(minors)):
                    if self.data.obtain_major_from_minor(minors[b]) == majors[a]:
                        x.append(minors[b])
                        cases.append(y[b])
                position = self.data.major_list.index(majors[a])
                color = self.colors[position]
                chart = go.Bar(x=x, y=cases, marker_color=color)
                figure.add_trace(chart)
                x = []
                cases = []
        else:
            if minor == "(All)":
                chart_data = self.data.minor_bar_chart_data
                for i in range(len(minors)):
                    y.append(chart_data.loc[minors[i]].sum())
            else:
                chart_data = self.data.minor_bar_chart_data
                y = [chart_data.sum()]
            # Create the layout
            layout = go.Layout(showlegend=False, plot_bgcolor="#ffffff")
            # Create the figure
            figure = go.Figure(layout=layout)
            position = self.data.major_list.index(major)
            color = self.colors[position]
            chart = go.Bar(x=minors, y=y, marker_color=color)
            figure.add_trace(chart)
            figure.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})

        # colors = ['pinkyl','blues','oranges','reds','blues','pubu','oranges','pinkyl','lightslategray']
        figure.update_layout(title="Minor Class Description", height=350)
        # Update the layout of the axes so that bar chart is in descending order, the column with greatest value is on the left
        figure.update_yaxes(title_font=dict(size=14, color='#666666'),
                            tickfont=dict(color='#666666', size=20), ticksuffix="",
                            showgrid=True, gridwidth=1, gridcolor='#CDCDCD',
                            tick0=min(y), nticks=5)
        figure.update_xaxes(tickangle=45, tickfont=dict(color='#666666', size=8),
                            showline=True, linewidth=2, linecolor='#CDCDCD')

        return figure

    def create_borough_map(self, borough):
        y = []
        if borough == "(All)":
            borough_name = 'London'
            boroughs = self.data.borough_list
            geo_code = self.data.geo_code_list
            map_data = self.data.borough_bar_chart_data
            for i in range(len(boroughs)):
                y.append(map_data.loc[boroughs[i]].sum())
        else:
            borough_name = borough
            boroughs = [borough]
            position = self.data.borough_list.index(borough)
            geo_code = [self.data.geo_code_list[position]]
            chart_data = self.data.borough_bar_chart_data.loc[borough].sum()
            y = [chart_data]
        # self.map_df = pd.DataFrame(list(zip(geo_code,boroughs,y)),columns = ["GEO_CODE","Borough","value"])
        fig = go.Figure(go.Choroplethmapbox(geojson=self.data.la_geojson, locations=geo_code, z=y,
                                            featureidkey="properties.LAD19CD", hovertext=boroughs,
                                            colorscale="Viridis", marker_opacity=0.5, marker_line_width=0

                                            ))
        fig.update_layout(mapbox_style="carto-positron", title="number of crime happened in " + borough_name,
                          mapbox_zoom=8.5, mapbox_center={"lat": 51.5074, "lon": -0.1000})
        return fig


data = CrimeData()
data.get_data()
borough = '(All)'
major = '(All)'
minor = '(All)'
data.process_data_for_selection(borough, major, minor)
CrimeChart(data).create_borough_map(borough)
