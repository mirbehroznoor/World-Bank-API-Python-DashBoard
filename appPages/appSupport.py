import pandas as pd
import wbgapi as wb

from dash_iconify import DashIconify
from dash import html

# wb.db = 1
# database = pd.DataFrame(wb.source.info().items)
indicators = pd.DataFrame(wb.series.info(db=None).items)
economies = pd.DataFrame(wb.economy.info(db=None).items)

years = pd.DataFrame(wb.time.info().items)
years["value"] = years["value"].astype("int")
min_year = years["value"].min()
max_year = years["value"].max()

econ_dic = dict(economies.set_index("value")['id'])
ind_dic = dict(indicators.set_index("value")["id"])
# db_dic = dict(database.set_index("name")['id'])

if wb.db == 2:
    y_var = "NY.GDP.PCAP.CD"
    x_var = "AG.LND.AGRI.ZS"
    country_var = "KOR"
else:
    y_var = indicators["id"][0]
    x_var = indicators["id"][1]
    country_var = "KOR"


def ind_Developmentrelevance(ind):
    dr = wb.series_metadata.get(ind)
    for i in dr.metadata.keys():
        if i == "Developmentrelevance":
            devRel = dr.metadata["Developmentrelevance"]
            break
        else:
            devRel = "Not Available"
    return devRel


# period = [ld.metadata[i]
    # for i in ld.metadata.keys() if i == "Periodicity"]
# longDef = [ld.metadata[i]
    # for i in ld.metadata.keys() if i == "Longdefinition"]

def ind_periodicity(ind):
    period = wb.series_metadata.get(ind)
    for i in period.metadata.keys():
        if i == "Periodicity":
            periodicity = period.metadata[i]
            break
        else:
            periodicity = "Not Available"
    return periodicity


def ind_Longdefinition(ind):
    ld = wb.series_metadata.get(ind)
    for i in ld.metadata.keys():
        if i == "Longdefinition":
            longDef = ld.metadata["Longdefinition"]
            break
        else:
            longDef = "Not Available"

    return longDef


def return_key(dic, val):
    for key, value in dic.items():
        if value == val:
            return key
    return('Key Not Found')


def one_econ_data(wb, year, d_indicator, d_economies):
    data = (
        wb.data.DataFrame(d_indicator, d_economies,
                          numericTimeKeys=True,
                          labels=True,
                          )
        .iloc[:, 3:]
        .transpose()
    )
    data = data.rename_axis(None, axis=1)
    data = data.reset_index()
    data = data.rename(columns={"index": "Year"})
    data = data[(data["Year"] >= year[0]) & (data["Year"] <= year[1])]
    return data


def multi_econ_data(wb, year, d_indicator, d_economies):
    data = (
        wb.data.DataFrame(d_indicator, d_economies,
                          numericTimeKeys=True,
                          labels=True)
    )
    data = data.reset_index()
    data = data.melt(id_vars=data.columns[0:4],
                     var_name="Year")
    data = data.pivot(["Country", "Year"],
                      "series",
                      "value").reset_index()
    data = data[(data["Year"] >= year[0]) & (data["Year"] <= year[1])]
    return data


app_footer = html.Div([
    html.Div([
        html.Ul('Contributors', className="contributors"),
        # https://stackoverflow.com/questions/67221522/how-to-hyperlink-an-image-in-plotly-dash
        html.A([DashIconify(
            icon="ion:logo-github",
            width=30,
            color="black",
            inline=True,
        ),
            '@mirbehroznoor'],
            href='https://github.com/mirbehroznoor',
            title="GitHub",
            style={
                "color": "black",
        },

        ),
    ],
        style={
        "width": "auto",
            "float": "right",
            "marginTop": "0px",
            'marginRight': '13px',
            "color": "black",
    },
    ),
],
    style={
    "width": "100%",
    "float": "left",
    "marginTop": "5%",
    'marginBottom': '13px',
    # "background-color": "#ffdab9",
    "background": "lightsteelblue",
}
)
