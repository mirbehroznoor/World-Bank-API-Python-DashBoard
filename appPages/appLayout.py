# -*- coding: utf-8 -*-

import dash_bootstrap_components as dbc

y_linear_log = dbc.RadioItems(
    id="y-axis-type-7",
    options=[
        {"label": "Linear", "value": "Linear"},
        {"label": "Log", "value": "Log"}
    ],
    value="Linear",
    inline=True,
)

x_linear_log = dbc.RadioItems(
    id="x-axis-type-7",
    options=[
        {"label": "Linear", "value": "Linear"},
        {"label": "Log", "value": "Log"}
    ],
    value="Linear",
    inline=True,
)

button_style = {
    "display": "inline-block",
    "marginTop": "1px",
    "marginBottom": "1px",
}

switch_ind_button = dbc.Button(
    "Switch Axis VARs",
    title="Switch VARs. for OLS Regression",
    id="ind-switch-7",
    n_clicks=0,
    outline=True,
)

plot_choice_radio = dbc.RadioItems(
    value="None",
    id="plot-choice-7",
    options=[
        {"label": "Scatter", "value": "markers"},
        {"label": "Line", "value": "lines+markers"},
        # {"label": "None", "value": "None"},
    ],
    inline=True,
)
regression_radio = dbc.RadioItems(
    value="ols",
    id="regression-choice-7",
    options=[
        {"label": "OLS", "value": "ols"},
        {"label": "Lowess", "value": "lowess"},
        # {"label": "None", "value": "None"},
    ],
    inline=True,
)

year_chcklist = dbc.Checklist(
    value=["Years"],
    id="label-choice-7",
    options=[
        {"label": "Years + Markers", "value": "Years"},
    ],
    inline=True,
)

trendline_chcklist = dbc.Checklist(
    value=[],
    id="trendline-choice-7",
    options=[
        {"label": "Trendline", "value": "show"}
    ],
    inline=True,
)

simple_app_button = dbc.Button("simple App",
                               title="goto//: simpleApp",
                               outline=False,
                               color="primary",
                               href="/simpleApp",
                               )

multi_app_button = dbc.Button("multi App",
                              title="goto//: multiApp",
                              outline=False,
                              color="primary",
                              href="/multiApp",
                              )
