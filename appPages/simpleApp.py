# -*- coding: utf-8 -*-
from dash import dcc, html, callback, no_update
from dash.dependencies import Output, Input

import plotly.express as px
import wbgapi as wb

from appPages.appSupport import ind_dic, econ_dic, min_year, max_year
from appPages.appSupport import return_key, one_econ_data
from appPages.appSupport import y_var, country_var
from appPages.appSupport import app_footer

from appPages.appLayout import multi_app_button

layout = html.Div([
    # html.Div([
    # dcc.Link('Goto: multiApp',
                  # href='/multiApp'),
                  # ],
                  # style={
                  # 'width': '10%',
                  # 'float': 'right',
                  # 'padding': '5px 0px 0px 0px',
                  # "font-size": "80%"}
                  # ),
                  html.Div([
                      dcc.Dropdown(
                          id='y-indicator-2',
                          options=[{"label": key, "value": value}
                                   for key, value in ind_dic.items()],
                          value=y_var,
                          multi=False,
                          optionHeight=38
                      )
                  ],
                      style={
                      # "marginLeft": "5px",
                      'width': '100%',
                      'display': 'inline-block',
                      'font-size': '80%'
                  }
                  ),
                  html.Br(),
                  html.Div([
                      dcc.Dropdown(
                          id='economies-2',
                          options=[{"label": key, "value": value}
                                   for key, value in econ_dic.items()],
                          value=[country_var],
                          clearable=True,
                          multi=True)
                  ],
                      style={
                      'width': '100%',
                      'display': 'inline-block',
                      # 'padding': '2px 0px 0px 0px',
                      'font-size': '90%'
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
                              "marginLeft": "5px",
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
                          tooltip={"placement": "bottom",
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
                      "marginBottom": "5px",
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
                  html.Div([
                      multi_app_button,
                  ],
                      style={
                      "width": "40%",
                      "display": "inline-block",
                      "marginTop": "5px",
                      "marginBottom": "5px",
                  }
                  ),
                  app_footer,
                  ],
                  style={
    "marginLeft": "5px",
    "marginRight": "5px",
    # 'width': '89%',
    # 'display': 'inline-block',
    # 'font-size': '80%'
}
),


@ callback(
    Output('data-graph-2', 'figure'),
    Input('year-slider-2', 'value'),
    Input('economies-2', 'value'),
    Input('y-indicator-2', 'value'),
    Input('y-axis-type-2', 'value'),
    Input('plot-choice-2', 'value'),
)
def update_graph(year, economies, y_indicator, y_axis_type, plot_choice):

    econ_len = len(economies)

    if not y_indicator or not economies:
        return no_update

    data = one_econ_data(wb, year, y_indicator, economies)
    y_axis_title = return_key(ind_dic, y_indicator)

    fig = px.scatter(
        data,
        x="Year",
        y=economies,
        labels={"Year": "Year",
                y_indicator: y_axis_title,
                # economies: return_key(econ_dic, economies),
                },
        trendline=("ols" if plot_choice == "OLS" else None),
    )

    fig.update_traces(
        marker=dict(
            size=10,
            line=dict(
                # width=2,
                color='DarkSlateGrey'
            )
        ),
        # selector=dict(mode='markers')
    )

    fig.update_layout(transition_duration=500,
                      title=(f"{return_key(econ_dic, economies[0])}"
                             if econ_len == 1 else None)
                      )

    if plot_choice != "OLS":
        fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(
        title=f'{y_axis_title} :: {y_indicator}',
        type='linear' if y_axis_type == 'Linear' else 'log')

    fig.update_layout(height=450,
                      margin={
                          # 'l': 20,
                          'r': 10,
                          'b': 10,
                          # 't': 28
                      }
                      )

    fig.update_layout(
        legend=dict(
            title_text="",
            orientation="h",
            yanchor="bottom",
            y=1,
            # xanchor="right", x=0.50
        ))

    return fig
