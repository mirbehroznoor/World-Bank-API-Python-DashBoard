# -*- coding: utf-8 -*-
from dash import dcc, html, callback, no_update
from dash.dependencies import Output, Input
import plotly.express as px
import wbgapi as wb

from appPages.appSupport import ind_dic, econ_dic, min_year, max_year
from appPages.appSupport import return_key, one_econ_data, multi_econ_data
from appPages.appSupport import y_var, x_var, country_var

layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id="y-indicator-7",
            options=[
                {"label": key,
                 "value": value} for key, value in ind_dic.items()],
            value=y_var,
            multi=False),
        dcc.RadioItems(
            id="y-axis-type-7",
            options=["Linear", "Log"],
            value="Linear",
        ),
    ], style={'width': '50%',
              'float': 'left',
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
            value=x_var,
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
              'float': 'right',
              'display': 'inline-block',
              'font-size': "70%"
              }),
    html.Div([
        dcc.Dropdown(
            id="economies-7",
            options=[
                {"label": key, "value": value}
                for key, value in econ_dic.items()],
            value=[country_var],
            clearable=True,
            multi=True)
    ],
        style={
        "width": "89%",
        "display": "inline-block",
        "padding": "5px 0px 0px 0px",
        "font-size": "85%"}
    ),
    html.Div([
        dcc.Link('Goto: simpleApp',
                 href='/simpleApp'),
    ],            style={
        'width': '10%',
        'float': 'right',
        "padding": "5px 0px 0px 0px",
        "display": "inline-block",
        "font-size": "80%"
    }
    ),
    html.Div([
        dcc.RangeSlider(
            id="year-slider-7",
            min=min_year,
            max=max_year,
            step=1,
            tooltip={"placement": "bottom", "always_visible": True},
            marks=None,
            dots=False,
            # marks={year: str(year)[2:4] for year in years["value"]},
            # value=years["value"].max(),
            value=[min_year, max_year])
    ],
        style={
        "width": "58%",
        'float': 'left',
        "display": "inline-block",
        "marginTop": "8px",
        "font-size": "50%"
    }
    ),
    html.Div([
        dcc.RadioItems(
            value="OLS",
            id="plot-choice-7",
            options=['Scatter', 'Line', "OLS"],
            inline=True,
        ),
    ], style={
        'width': '30%',
        'float': 'right',
        "marginTop": "8px",
        'display': 'inline-block',
        "font-size": "80%"
    }),
    html.Div([
        dcc.Graph(id="data-graph-7"),
    ],
        style={
        "width": "99%",
        "display": "inline-block",
        "marginTop": "0px",
        "font-size": "50%"
    }
    ),
])


@ callback(
    Output("data-graph-7", "figure"),
    Input("year-slider-7", "value"),
    Input("economies-7", "value"),
    Input("y-indicator-7", "value"),
    Input("x-indicator-7", "value"),
    Input("plot-choice-7", "value"),
    Input('y-axis-type-7', 'value'),
    Input('x-axis-type-7', 'value'),
)
def update_data(year, economies, y_ind, x_ind, plot_choice,
                y_axis_type, x_axis_type):

    econ_len = len(economies)
    col_cond = "no"

    if not x_ind and not y_ind or not economies:
        return no_update
    elif x_ind and y_ind and econ_len < 1:
        return no_update
    elif not x_ind and y_ind:
        x_axis = "Year"
        x_axis_title = "Year"
        y_axis = economies
        y_axis_title = return_key(ind_dic, y_ind)
        data = one_econ_data(wb, year, y_ind, economies)
    elif x_ind and not y_ind:
        x_axis = "Year"
        y_axis = economies
        x_axis_title = "Year"
        y_ind = x_ind
        y_axis_title = return_key(ind_dic, y_ind)
        data = one_econ_data(wb, year, y_ind, economies)
    elif (y_ind and x_ind) and (econ_len >= 1):
        x_axis = x_ind
        x_axis_title = return_key(ind_dic, x_ind)
        y_axis = y_ind
        y_axis_title = return_key(ind_dic, y_ind)
        indicators = [y_ind, x_ind]
        if econ_len == 1:
            data = one_econ_data(wb, year, indicators, economies)
        else:
            data = multi_econ_data(wb, year, indicators, economies)
            col_cond = "yes"

    fig = px.scatter(
        data,
        x=x_axis,
        y=y_axis,
        color=("Country" if col_cond == "yes" else None),
        labels={x_ind: x_axis_title,
                y_ind: y_axis_title,
                # economies: return_key(econ_dic, economies),
                },
        trendline=("ols" if plot_choice == "OLS" else None),
        text=("Year" if x_ind and y_ind else None),
    )

    fig.update_layout(transition_duration=500,
                      # title=(f"{economies}")
                      title=(f"{return_key(econ_dic, economies[0])}"
                             if econ_len == 1 else None)
                      )

    if plot_choice != "OLS":
        fig.update_traces(mode="markers" if plot_choice ==
                          "Scatter" else "lines+markers")
    else:
        fig.update_traces(textposition='top center')

    fig.update_xaxes(
        title=("Year" if x_axis ==
               "Year" else f'{x_axis_title} :: {x_ind}'),
        showgrid=False,
        type="linear" if x_axis_type == "Linear" else 'log')

    fig.update_yaxes(
        title=f"{y_axis_title} :: {y_ind}",
        type="linear" if y_axis_type == "Linear" else 'log')

    fig.update_layout(height=500,
                      margin={
                          # "l": 20,
                          "r": 10,
                          "b": 10,
                          # "t": 28
                      }
                      )

    fig.update_layout(
        legend=dict(
            title_text="",
            orientation="h",
            yanchor="bottom",
            y=1,
            # xanchor="right", x=0.50
        )
    )

    return fig
