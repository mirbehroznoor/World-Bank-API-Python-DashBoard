# -*- coding: utf-8 -*-
from dash import dcc, html, callback, no_update
from dash.dependencies import Output, Input
import plotly.express as px
import wbgapi as wb

from appPages.appSupport import ind_dic, econ_dic, min_year, max_year
from appPages.appSupport import return_key, extract_data
from appPages.appSupport import y_var, country_var

layout = html.Div([
    html.Div([
        dcc.Link('Goto: multiApp',
                  href='/multiApp'),
    ],
        style={
            'width': '10%',
            'float': 'right',
            'padding': '5px 0px 0px 0px',
            "font-size": "80%"}
    ),
    html.Div([
        dcc.Dropdown(
            id='d-indicators-2',
            options=[{"label": key, "value": value}
                     for key, value in ind_dic.items()],
            value=y_var,
            multi=False)
    ],
        style={
            'width': '89%',
            'display': 'inline-block',
            'font-size': '70%'}
    ),
    html.Div([
        dcc.Dropdown(
            id='d-economies-2',
            options=[{"label": key, "value": value}
                     for key, value in econ_dic.items()],
            value=country_var,
            clearable=False,
            multi=True)
    ],
        style={
            'width': '100%',
            'display': 'inline-block',
            'padding': '2px 0px 0px 0px',
            'font-size': '85%'
    }
    ),
    html.Div([
        dcc.RadioItems(
            id="plot-choice-2",
            options=["None", "OLS"],
            value="None",
            inline=True,
            labelStyle={
                "width": "15%",
                "marginTop": "0px",
                "display": "inline-block",
                "float": "right",
                "font-size": "80%",
            },
        ),
        dcc.RadioItems(
            id="y-axis-type-2",
            options=["Linear", "Log"],
            value="Linear",
            inline=True,
            labelStyle={
                "width": "15%",
                "marginTop": "0px",
                "float": "left",
                "display": "inline-block",
                "font-size": "80%",
            },
        ),
    ]),
    html.Div([
        dcc.RangeSlider(
            id="year-slider-2",
            min=min_year,
            max=max_year,
            step=1,
            tooltip={
                "placement": "right",
                "always_visible": True},
            marks=None,
            dots=False,
            # marks={year: str(year)[2:4] for year in years["value"]},
            # value=years["value"].max(),
            value=[min_year, max_year],
        ),
    ],
        style={
        "width": "90%",
        'float': 'left',
        "display": "inline-block",
        "marginTop": "8px",
        "font-size": "50%"
    }
    ),
    html.Div([
        dcc.Graph(id='data-graph-2'),
    ],
        style={
        "width": "99%",
        "display": "inline-block",
        "marginTop": "0px",
        "font-size": "50%"
    }
    ),
]),


@ callback(
    Output('data-graph-2', 'figure'),
    Input('year-slider-2', 'value'),
    Input('d-economies-2', 'value'),
    Input('d-indicators-2', 'value'),
    Input('y-axis-type-2', 'value'),
    Input('plot-choice-2', 'value'),
)
def update_graph(year, d_economies, d_indicator, y_axis_type, plot_choice):

    if not d_indicator or not d_economies:
        return no_update

    data = extract_data(wb, year, d_economies, d_indicator)
    y_axis_title = return_key(ind_dic, d_indicator)

    fig = px.scatter(
        data,
        x="Year",
        y=d_economies,
        labels={"Year": "Year",
                d_indicator: y_axis_title,
                # d_economies: return_key(econ_dic, d_economies),
                },
        trendline=("ols" if plot_choice == "OLS" else None),
    )

    fig.update_layout(transition_duration=500)

    if plot_choice != "OLS":
        fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(
        title=f'{y_axis_title} :: {d_indicator}',
        type='linear' if y_axis_type == 'Linear' else 'log')

    fig.update_layout(height=450,
                      margin={
                          'l': 28,
                          'r': 10,
                          'b': 10,
                          't': 28
                      }
                      )

    fig.update_layout(legend=dict(
        title_text="",
        orientation="h",
        yanchor="top",
        y=1.02,
        xanchor="right",
        x=0.50
    ))

    return fig
