# -*- coding: utf-8 -*-
from dash import dcc, html, callback
from dash.dependencies import Output, Input
import pandas as pd
import wbgapi as wb
import plotly.express as px

indicators = pd.DataFrame(wb.series.info().items)
economies = pd.DataFrame(wb.economy.info().items)
years = pd.DataFrame(wb.time.info().items)
years["value"] = years["value"].astype("int")
econ_dic = dict(economies.set_index("value")['id'])
ind_dic = dict(indicators.set_index("value")["id"])


def return_key(dic, val):
    for key, value in dic.items():
        if value == val:
            return key
    return('Key Not Found')


def extract_data(year, d_economies, d_indicator):
    data = (
        wb.data.DataFrame(d_indicator, d_economies,
                          numericTimeKeys=True, labels=True)
        .iloc[:, 3:]
        .transpose()
    )
    data = data.rename_axis(None, axis=1)
    data = data.reset_index()
    data = data.rename(columns={"index": "Year"})
    data = data[(data["Year"] >= year[0]) & (data["Year"] <= year[1])]
    return data


layout = html.Div([
    html.Div([
        dcc.Link('Go to: Multi DashBoard',
                  href='/multiApp'),
    ],
        style={
        'width': '10%',
        'float': 'right',
            # "display": "inline-block",
            'padding': '5px 0px 0px 0px',
            "font-size": "80%"}
    ),
    html.Div([
        dcc.Dropdown(
            id='d-indicators-2',
            options=[{"label": key, "value": value}
                     for key, value in ind_dic.items()],
            value="NY.GDP.PCAP.CD",
            multi=False)
    ],
        style={
        'width': '89%',
            'display': 'inline-block',
            # 'padding': '10px 5px',
            'font-size': '70%'}
    ),
    html.Div([
        dcc.Dropdown(
            id='d-economies-2',
            options=[{"label": key, "value": value}
                     for key, value in econ_dic.items()],
            value="KOR",
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
        dcc.RangeSlider(
            id="year-slider-2",
            min=years["value"].min(),
            max=years["value"].max(),
            step=1,
            tooltip={"placement": "right", "always_visible": True},
            marks=None,
            dots=False,
            # marks={year: str(year)[2:4] for year in years["value"]},
            # value=years["value"].max(),
            value=[1960, 2023]),
    ],  style={
        'width': '100%',
        'display': 'inline-block',
        # 'padding': '5px 0px 0px 0px',
        'font-size': '50%'
    }
    ),
    # html.Br(),
    html.Div([dcc.Graph(id='data-graph-2'),
              ]),
])


@ callback(
    Output('data-graph-2', 'figure'),
    Input('year-slider-2', 'value'),
    Input('d-economies-2', 'value'),
    Input('d-indicators-2', 'value'),
)
def update_graph(year, d_economies, d_indicator):
    data = extract_data(year, d_economies, d_indicator)
    y_axis_title = return_key(ind_dic, d_indicator)
    fig = px.scatter(
        data,
        x="Year",
        y=d_economies,
        # log_y=True,
    )
    fig.update_layout(transition_duration=500)
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(
        title=f'{y_axis_title} ::\t{d_indicator}', type='linear')
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
