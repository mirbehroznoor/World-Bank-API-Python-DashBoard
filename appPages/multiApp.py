# -*- coding: utf-8 -*-
import dash
from dash import dcc, html, callback, no_update
from dash.dependencies import Output, Input, State

import dash_bootstrap_components as dbc

import plotly.express as px
import wbgapi as wb

from appPages.appSupport import ind_dic, econ_dic, min_year, max_year
from appPages.appSupport import return_key, one_econ_data, multi_econ_data
from appPages.appSupport import y_var, x_var, country_var
from appPages.appSupport import ind_Longdefinition, ind_Developmentrelevance
from appPages.appSupport import ind_periodicity
from appPages.appSupport import app_footer

from appPages.appLayout import y_linear_log, x_linear_log
from appPages.appLayout import button_style
from appPages.appLayout import switch_ind_button
from appPages.appLayout import plot_choice_radio, regression_radio
from appPages.appLayout import year_chcklist, trendline_chcklist
from appPages.appLayout import simple_app_button


ind_dropdown = dbc.Row([
    dbc.Col([
        html.Div([
            dcc.Dropdown(
                id="y-indicator-7",
                options=[
                    {"label": key, "value": value}
                    for key, value in ind_dic.items()
                ],
                value=y_var,
                multi=False,
                optionHeight=50
            ),
        ],
            style={
            "width": "100%",
            "display": "inline-block",
            "float": "left",
            "font-size": "85%",
            "marginTop": "5px",
            "marginBottom": "5px",
        },
        ),
    ]),
    dbc.Col([
        html.Div([
            dcc.Dropdown(
                id="x-indicator-7",
                options=[
                    {"label": key, "value": value}
                    for key, value in ind_dic.items()
                ],
                value=x_var,
                multi=False,
                optionHeight=50
            ),
        ],
            style={
            "width": "100%",
            "float": "right",
            "display": "inline-block",
            "font-size": "85%",
            "marginTop": "5px",
            "marginBottom": "5px",
        },
        ),
    ])
])

linear_log_radio = dbc.Row([
    dbc.Col([
        html.Div(
            y_linear_log,
            style=button_style
        ),
        html.Div([
            dbc.Button(
                "Info",
                title="Definition & Relevance & Periodicity",
                id="y-open",
                n_clicks=0,
                outline=True,
            ),
            dbc.Modal([
                dbc.ModalBody(
                    dbc.Accordion([
                        dbc.AccordionItem(
                            id='y-period-7',
                            title="Data Periodicity",
                            item_id="item-3",
                        ),
                        dbc.AccordionItem(
                            id='y-long-def-7',
                            title="Long Definition",
                            item_id="item-1",
                        ),
                        dbc.AccordionItem(
                            id='y-dev-rel-7',
                            title="Development Relevance",
                            item_id="item-2",
                        ),
                    ],
                        id="y-accordion",
                        # change styling, including removing borders,
                        # and rounding some of the edges
                        flush=True,
                        active_item="item-1",
                    ),
                ),
            ],
                id="y-modal",
                is_open=False,
            )
        ],
            style=button_style
        ),
    ]),
    dbc.Col([
            html.Div(
                x_linear_log,
                style=button_style),
            html.Div([dbc.Button("Info",
                                 title="Definition & Relevance & Periodicity",
                                 id="x-open",
                                 n_clicks=0,
                                 outline=True,
                                 ),
                      dbc.Modal([
                          dbc.ModalBody(
                              dbc.Accordion([
                                  dbc.AccordionItem(
                                      id='x-period-7',
                                      title="Data Periodicity",
                                      item_id="item-3",
                                  ),
                                  dbc.AccordionItem(
                                      id='x-long-def-7',
                                      title="Long Definition",
                                      item_id="item-1",
                                  ),
                                  dbc.AccordionItem(
                                      id='x-dev-rel-7',
                                      title="Development Relevance",
                                      item_id="item-2",
                                  ),
                              ],
                                  id="y-accordion",
                                  # change styling, including removing borders,
                                  # and rounding some of the edges
                                  flush=True,
                                  active_item="item-1",
                              ),
                          ),
                      ],
                id="x-modal",
                is_open=False,
            )
            ],
                # simple app button, alternate place
                style=button_style)
            ]),
]
)

econ_dropdown = dbc.Row([
    html.Div([
        dbc.Col([
            html.Div(
                dcc.Dropdown(
                    id="economies-7",
                    options=[
                        {"label": key, "value": value}
                        for key, value in econ_dic.items()
                    ],
                    value=[country_var],
                    clearable=True,
                    multi=True
                ),
                style={
                    "width": "70%",
                    "float": "left",
                    "marginTop": "1px",
                    "marginRight": "15px",
                }),
            html.Div(
                switch_ind_button,
                style={
                    "padding": "0px 0px 0px 0px",
                }
            ),
        ])
    ],
        style={
        "width": "100%",
        "font-size": "85%",
        "display": "inline-block",
        "marginTop": "5px",
        "marginBottom": "5px",
    })
])

slider_radio_checklist = dbc.Row([
    html.Div([
        dbc.Col([
                dcc.RangeSlider(
                    id="year-slider-7",
                    min=min_year,
                    max=max_year,
                    step=1,
                    tooltip={"placement": "bottom",
                             "always_visible": True},
                    marks=None,
                    dots=False,
                    # value=years["value"].max(),
                    value=[min_year, max_year],
                ),
                ])
    ],
        style={
            "width": "49%",
            'float': 'left',
            "display": "inline-block",
            "marginTop": "8px",
            "font-size": "50%",
            "padding": "0px 0px 0px 0px",
    }
    ),
    html.Div([
        dbc.Col([
            plot_choice_radio,
            regression_radio,
        ],
            style={
            'float': 'left',
            # "display": "inline-block",
            # "marginTop": "8px",
            # "marginLeft": "10px",
        }
        ),
        dbc.Col([
            year_chcklist,
            trendline_chcklist,
        ],
            style={
            'float': 'left',
            # "display": "inline-block",
            "marginLeft": "50px",
        }),
    ],
        style={
            "width": "49%",
            "marginTop": "8px",
            "marginLeft": "30px",
            # "font-size": "80%",
    }
    )
])

graph_container = dbc.Row([
    dbc.Col(
        dcc.Graph(id="data-graph-7"),
        style={
            "width": "99%",
            "display": "inline-block",
            "marginTop": "5px",
            # "font-size": "50%",
        },
    )]
)

switch_app = dbc.Row([
    html.Div([
        simple_app_button,
    ],
        style={
        "width": "40%",
        "display": "inline-block",
        "marginTop": "5px",
        "marginBottom": "5px",
    }
    )
])


layout = dbc.Container([
    ind_dropdown,
    linear_log_radio,
    econ_dropdown,
    slider_radio_checklist,
    graph_container,
    html.Br(),
    switch_app,
    app_footer,
],
    fluid=True,
)


@ callback(
    Output("data-graph-7", "figure"),
    Output("label-choice-7", "value"),
    Output("plot-choice-7", "value"),
    Output("regression-choice-7", "value"),
    Output("trendline-choice-7", "value"),
    [Input("year-slider-7", "value"),
     Input("economies-7", "value"),
     Input("y-indicator-7", "value"),
     Input("x-indicator-7", "value"),
     Input("plot-choice-7", "value"),
     Input("y-axis-type-7", "value"),
     Input("x-axis-type-7", "value"),
     Input("label-choice-7", "value"),
     Input("trendline-choice-7", "value"),
     Input("ind-switch-7", "n_clicks"),
     Input("regression-choice-7", "value")],
)
def update_data(
    year,
    economies,
    y_ind,
    x_ind,
    plot_choice,
    y_axis_type,
    x_axis_type,
    label_choice,
    trendline_choice,
    switch_indicators,
    regression_choice,
):

    econ_len = len(economies)
    col_cond = "no"

    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if switch_indicators % 2 == 0:
        y_ind
        x_ind
    else:
        # https://theprogrammingexpert.com/python-even-or-odd/
        x_switched = y_ind
        y_switched = x_ind
        x_ind = x_switched
        y_ind = y_switched

    if input_id == "plot-choice-7":
        regression_choice = "None"
        text_label = []
        trendline_choice = []
    elif input_id == "regression-choice-7":
        plot_choice = "None"
        text_label = label_choice
    elif input_id == "label-choice-7":
        plot_choice = "None"
        trendline_choice = []
        text_label = label_choice
    elif input_id == "trendline-choice-7":
        plot_choice = "None"
        text_label = []
        if regression_choice == "None":
            regression_choice = "ols"
    else:
        text_label = label_choice

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
        # symbol=(f"{y_ind}" if y_ind else x_ind),
        labels={
            x_ind: x_axis_title,
            y_ind: y_axis_title,
            # economies: return_key(econ_dic, economies),
        },
        trendline=(regression_choice if regression_choice !=
                   "None" else None),
        # text=("Year" if x_ind and y_ind else None),
        text=("Year" if text_label else None),
    )

    # nans_indices = Report_Card.columns[Report_Card.isna().any()].tolist()

    # nans = Report_Card.loc[:,nans]

    fig.update_traces(
        marker=dict(
            size=10,
            # line=dict(
            # width=2,
            # color='DarkSlateGrey'
            # )
        ),
        line=dict(
            width=3,
            # color='DarkSlateGrey'
        ),

        # selector=dict(mode='markers')
    )

    # fig.update_layout(
    # transition_duration=500,
#        # title=(f"{economies}")
    # title=(plot_title),
    # )

    fig.update_xaxes(
        title=("Year" if x_axis == "Year" else f"{x_axis_title} :: {x_ind}"),
        showgrid=False,
        type="linear" if x_axis_type == "Linear" else "log",
    )

    fig.update_yaxes(
        title=f"{y_axis_title} :: {y_ind}",
        type="linear" if y_axis_type == "Linear" else "log",
    )

    fig.update_layout(
        height=500,
        margin={
            # "l": 20,
            "r": 10,
            "b": 20,
            "t": 70
        },
    )

    plot_title = (f"{return_key(econ_dic, economies[0])}"
                  if econ_len == 1 else None)

    fig.update_layout(
        legend=dict(
            title_text=plot_title,
            orientation="h",
            yanchor="bottom",
            y=1,
            # xanchor="right",
            # x=0.50
        )
    )
    if econ_len == 1:
        # fig.update_layout(hovermode="x")
        if regression_choice == "ols":
            # https://stackoverflow.com/questions/66146489/plotly-how-to-retrieve-regression-results-using-plotly-express
            # retrieve model estimates
            model = px.get_trendline_results(fig)
            try:
                results = model.iloc[0]["px_fit_results"]
                alpha = str(round(results.params[0], 3))
                beta = str(round(results.params[1], 3))
                r_squared = str(round(results.rsquared, 5))
                p_beta = results.pvalues[1]

                beta_1 = ("Year" if x_axis == "Year" else f"{x_ind}")
                line1 = f"{y_ind} = <b>{beta}</b>*{beta_1} + {alpha}"
                line2 = 'p-value = ' + '{:.5f}'.format(p_beta)
                line3 = f"R^2 = {r_squared}"

                summary = f"<br>   {line1}<b>... </b>{line3}<b>... </b>{line2}<br>"
                fig.update_layout(
                    title={
                        'text': (summary if econ_len == 1 else None),
                        'y': 1,
                        'yanchor': 'top',
                    }
                )
            # https://stackoverflow.com/a/64756640
            except IndexError:
                None
        elif plot_choice != "None":
            fig.update_layout(
                title={
                    'text': plot_title,
                    'y': 1,
                    'yanchor': 'top',
                }
            )
    else:
        None

    if plot_choice != "None":
        fig.update_traces(mode=plot_choice)
    elif trendline_choice:
        fig.update_traces(selector=dict(mode="markers"),
                          visible=(False if trendline_choice else True))
        fig.update_traces(textposition="top center",
                          showlegend=True)
    else:
        fig.update_traces(textposition="top center",
                          showlegend=True)

    return fig, text_label, plot_choice, regression_choice, trendline_choice


@ callback(
    Output("y-dev-rel-7", "children"),
    Output("y-long-def-7", "children"),
    Output("y-period-7", "children"),
    Output("x-dev-rel-7", "children"),
    Output("x-long-def-7", "children"),
    Output("x-period-7", "children"),
    [Input("y-indicator-7", "value"),
     Input("x-indicator-7", "value")],


)
def update_definitions(y_ind, x_ind):

    if y_ind:
        y_devRel = ind_Developmentrelevance(y_ind)
        y_longDef = ind_Longdefinition(y_ind)
        y_period = ind_periodicity(y_ind)
    else:
        y_devRel = ""
        y_longDef = ""
        y_period = ""

    if x_ind:
        x_devRel = ind_Developmentrelevance(x_ind)
        x_longDef = ind_Longdefinition(x_ind)
        x_period = ind_periodicity(x_ind)
    else:
        x_devRel = ""
        x_longDef = ""
        x_period = ""

    return y_devRel, y_longDef, y_period, x_devRel, x_longDef, x_period


@ callback(
    Output("y-modal", "is_open"),
    [Input("y-open", "n_clicks")],
    [State("y-modal", "is_open")],
)
def toggle_y_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open


@ callback(
    Output("x-modal", "is_open"),
    [Input("x-open", "n_clicks")],
    [State("x-modal", "is_open")],
)
def toggle_x_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open
