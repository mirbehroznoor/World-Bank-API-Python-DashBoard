import pandas as pd
import wbgapi as wb

# wb.db = 2
indicators = pd.DataFrame(wb.series.info().items)
economies = pd.DataFrame(wb.economy.info().items)

years = pd.DataFrame(wb.time.info().items)
years["value"] = years["value"].astype("int")
min_year = years["value"].min()
max_year = years["value"].max()

econ_dic = dict(economies.set_index("value")['id'])
ind_dic = dict(indicators.set_index("value")["id"])


def return_key(dic, val):
    for key, value in dic.items():
        if value == val:
            return key
    return('Key Not Found')


def extract_data(wb, year, d_economies, d_indicator):
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
