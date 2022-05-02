import pandas as pd
import wbgapi as wb

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
    first_var = "NY.GDP.PCAP.CD"
    second_var = "AG.LND.AGRI.ZS"
    country_var = "KOR"
else:
    first_var = indicators["id"][0]
    second_var = indicators["id"][1]
    country_var = "KOR"


def return_key(dic, val):
    for key, value in dic.items():
        if value == val:
            return key
    return('Key Not Found')


def extract_data(wb, year, d_economies, d_indicator):
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
