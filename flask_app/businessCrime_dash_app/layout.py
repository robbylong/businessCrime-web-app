from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from flask_app.businessCrime_dash_app.crimechart import CrimeChart
from flask_app.businessCrime_dash_app.crimedata import CrimeData

# Prepare the data set
data = CrimeData()
data.get_data()
borough = '(All)'
major = '(All)'
minor = '(All)'
data.process_data_for_selection(borough, major, minor)

# Create the figures
cc = CrimeChart(data)
fig_lc = cc.create_line_chart(borough, major, minor)
fig_borough_bc = cc.create_borough_bar_chart(borough, major, minor)
fig_major_bc = cc.create_major_crime_bar_chart(borough, major, minor)
fig_minor_bc = cc.create_minor_crime_bar_chart(borough, major, minor)
fig_borough_map = cc.create_borough_map(borough)

external_stylesheets = [dbc.themes.BOOTSTRAP]

layout = dbc.Container(children=[
    html.H1(children='Business Crime Dashboard'),

    dbc.Row([
        dbc.Col(width=3, children=[
            dbc.Label('Borough'),
            dcc.Dropdown(id="borough-select",
                         options=[{"label": x, "value": x} for x in data.borough_dropdown_list],
                         value="(All)",
                         placeholder='(All)'),
        ]),

        dbc.Col(width=3, children=[
            dbc.Label('Major'),
            dcc.Dropdown(id="major-select",
                         options=[{"label": x, "value": x} for x in data.major_dropdown_list],
                         value="(All)",
                         placeholder='(All)'),
        ]),
        dbc.Col(width=3, children=[
            dbc.Label('Minor'),
            dcc.Dropdown(id="minor-select",
                         options=[{"label": x, "value": x} for x in data.minor_dropdown_list],
                         value="(All)",
                         placeholder='(All)'),
        ])
    ]
    ),

    dbc.Row(children=[
        dbc.Row([
            dbc.Col(width=7, children=[
                dbc.Row([
                    dcc.Graph(
                        id='line-chart',
                        figure=fig_lc,
                        style={"height": 300}
                    )
                ]
                ),

                dbc.Row([
                    dcc.Graph(
                        id='borough-bar-chart',
                        figure=fig_borough_bc,
                        style={"height": 350}
                    )

                ]
                )
            ]
                    ),
            dbc.Col(width=5, children=[
                dcc.Graph(
                    id='map-chart',
                    figure=fig_borough_map,
                    style={"height": 600}
                )

            ])
        ], style={"height": "90%"}
        )
    ]
    ),
    dbc.Row([
        dbc.Col(width=5, children=[
            dcc.Graph(
                id='major-bar-chart',
                figure=fig_major_bc
            )
        ]),
        dbc.Col(width=7, children=[
            dcc.Graph(
                id='minor-bar-chart',
                figure=fig_minor_bc
            )
        ])
    ], style={"height": "10%"}
    )

],
    fluid=True,
)
