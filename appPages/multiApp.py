# -*- coding: utf-8 -*-
from dash import dcc, html, callback, no_update
from dash.dependencies import Output, Input
import plotly.express as px
import wbgapi as wb

from appPages.appSupport import ind_dic, econ_dic, min_year, max_year
from appPages.appSupport import return_key, extract_data
from appPages.appSupport import first_var, second_var, country_var

layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id="y-indicator-7",
            options=[
                {"label": key,
                 "value": value} for key, value in ind_dic.items()],
            value=first_var,
            multi=False),
        dcc.RadioItems(
            id="y-axis-type-7",
            options=["Linear", "Log"],
            value="Linear",
        ),
    ], style={'width': '50%',
              'float': 'right',
              'display': 'inline-block',
              'font-size': "70%"
              }),
    html.Div([
        dcc.Dropdown(
            id="x-indicator-7",
            options=[
                {"label": key,
                 "value": value} for key, value in ind_dic.items()
            ],
            value=second_var,
            multi=False),
        dcc.RadioItems(
            id="x-axis-type-7",
            options=["Linear", "Log"],
            value="Linear",
            labelStyle={
                "display": "inline-block",
                "marginTop": "0px",
            },
        ),
    ], style={'width': '49%',
              'float': 'left',
              'display': 'inline-block',
              'font-size': "70%"
              }),
    html.Div([
        dcc.Dropdown(
            id="d-economies-7",
            options=[
                {"label": key, "value": value}
                for key, value in econ_dic.items()],
            value=country_var,
            clearable=False,
            multi=True)
    ],
        style={
        "width": "90%",
        "display": "inline-block",
        "padding": "5px 0px 0px 0px",
        "font-size": "85%"}
    ),
    html.Div([
        dcc.Link('Go to: Simple DashBoard',
                 href='/simpleApp'),
    ],            style={
        'width': '8%',
        'float': 'right',
        "padding": "5px 0px 0px 0px",
        "display": "inline-block",
        "font-size": "70%"
    }
    ),
    html.Br(),
    html.Div([
        dcc.RadioItems(
            value="Scatter",
            id="plot-choice-7",
            options=['Scatter', 'Line'],
            # labelStyle={
            # "display": "inline-block",
            # "marginTop": "0px",
            # },
        ),
    ], style={
        'width': '17%',
        'float': 'right',
        'display': 'inline-block'
    }),
    html.Div([
        dcc.RangeSlider(
            id="year-slider-7",
            min=min_year,
            max=max_year,
            step=1,
            tooltip={"placement": "right", "always_visible": True},
            marks=None,
            dots=False,
            # marks={year: str(year)[2:4] for year in years["value"]},
            # value=years["value"].max(),
            value=[min_year, max_year])
    ],
        style={
        "width": "70%",
        'float': 'left',
        "display": "inline-block",
        # "padding": "2px 0px 0px 0px",
        "font-size": "50%"
    }
    ),
    html.Br(),
    html.Div([
        dcc.Graph(id="data-graph-7"),
    ]),
    html.H6(
        [
            html.Span("NOTE: ", style={"color": "red"}),
            html.Span('''It is possible to select 2 or more Economies or Indicators,
                          but not both options simultaneously.
                Due to a problem with Multi-index DataFrame(Pandas) and Plotly.
                In case of missing data, try changing the yearly input'''),
        ]
    ),
])


@ callback(
    Output("data-graph-7", "figure"),
    Input("year-slider-7", "value"),
    Input("d-economies-7", "value"),
    Input("y-indicator-7", "value"),
    Input("x-indicator-7", "value"),
    Input("plot-choice-7", "value"),
    Input('y-axis-type-7', 'value'),
    Input('x-axis-type-7', 'value'),
)
def update_data(year, d_economies, y_ind, x_ind, plot_choice,
                y_axis_type, x_axis_type):
    if not x_ind and y_ind:
        x_axis = "Year"
        x_axis_title = "Year"
        y_axis = d_economies
        y_axis_title = return_key(ind_dic, y_ind)
        data = extract_data(wb, year, d_economies, y_ind)
    elif y_ind and x_ind:
        x_axis = x_ind
        x_axis_title = return_key(ind_dic, x_ind)
        y_axis = y_ind
        y_axis_title = return_key(ind_dic, y_ind)
        indicators = [y_ind, x_ind]
        data = extract_data(wb, year, d_economies, indicators)
    elif x_ind and not y_ind:
        x_axis = "Year"
        y_axis = d_economies
        x_axis_title = "Year"
        y_axis_title = return_key(ind_dic, x_ind)
        data = extract_data(wb, year, d_economies, x_ind)
    elif not x_ind and not y_ind or not d_economies:
        return no_update

    fig = px.scatter(
        data,
        x=x_axis,
        y=y_axis
    )
    fig.update_layout(transition_duration=500)
    fig.update_traces(mode="markers" if plot_choice ==
                      "Scatter" else "lines+markers")
    fig.update_xaxes(
        title=("Year" if x_axis == "Year" else f'{x_axis_title} :: {x_ind}'),
        showgrid=False,
        type="linear" if x_axis_type == "Linear" else 'log')
    fig.update_yaxes(
        title=f"{y_axis_title} :: {y_ind}",
        type="linear" if y_axis_type == "Linear" else 'log')
    fig.update_layout(height=500, margin={
        "l": 20,
        "r": 10,
        "b": 10,
        "t": 10
    })
    fig.update_layout(
        legend=dict(
            title_text="", orientation="h",
            yanchor="top", y=1.02,
            xanchor="right", x=0.50
        )
    )
    return fig
