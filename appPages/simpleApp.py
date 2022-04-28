# -*- coding: utf-8 -*-
from dash import dcc, html, callback
from dash.dependencies import Output, Input
import plotly.express as px
import wbgapi as wb

from appPages.appSupport import ind_dic, econ_dic, min_year, max_year
from appPages.appSupport import return_key, extract_data
from appPages.appSupport import first_var, country_var

layout = html.Div([
    html.Div([
        dcc.Link('Go to: Multi DashBoard',
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
            value=first_var,
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
    html.Br(),
    html.Div([
        dcc.RadioItems(
            id="y-axis-type-2",
            options=["Linear", "Log"],
            value="Linear",
            labelStyle={
               "display": "inline-block",
            },
        ),
    ], style={'width': '15%', 'float': 'right', 'display': 'inline-block'}),
    html.Div([
        dcc.RangeSlider(
            id="year-slider-2",
            min=min_year,
            max=max_year,
            step=1,
            tooltip={"placement": "right", "always_visible": True},
            marks=None,
            dots=False,
            # marks={year: str(year)[2:4] for year in years["value"]},
            # value=years["value"].max(),
            value=[min_year, max_year]),
    ],  style={
        'width': '80%',
        'display': 'inline-block',
        'padding': '5px 0px 0px 0px',
        'font-size': '50%'
    }
    ),
    html.Div([
        dcc.Graph(id='data-graph-2'),
    ]),
])


@ callback(
    Output('data-graph-2', 'figure'),
    Input('year-slider-2', 'value'),
    Input('d-economies-2', 'value'),
    Input('d-indicators-2', 'value'),
    Input('y-axis-type-2', 'value'),
)
def update_graph(year, d_economies, d_indicator, y_axis_type):
    data = extract_data(wb, year, d_economies, d_indicator)
    y_axis_title = return_key(ind_dic, d_indicator)
    fig = px.scatter(
        data,
        x="Year",
        y=d_economies,
    )
    fig.update_layout(transition_duration=500)
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(
        title=f'{y_axis_title} :: {d_indicator}',
        type='linear' if y_axis_type == 'Linear' else 'log')
    fig.update_layout(height=530,
                      margin={
                          'l': 20,
                          'r': 10,
                          'b': 10,
                          't': 10
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
