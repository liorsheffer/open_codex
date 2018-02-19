# -*- coding: utf-8 -*-

"""Main module."""
import pandas as pd
import numpy as np
from pick import pick

raw_data_path = "https://gist.githubusercontent.com/seankross/a412dfbd88b3db70b74b/raw/5f23f993cd87c283ce766e7ac6b329ee7cc2e1d1/mtcars.csv"

data = pd.read_csv(raw_data_path)

def prompt_col(data, title = "Please select the column name to recode:"):
    options = data.columns.tolist()
    option, index = pick(options, title)
    return option


def make_data(data, selected_column):
    output = (
        data[selected_column]
            .str.strip()
            .str.lower()
            .value_counts()
            .reset_index()
    )
    output.columns = ['raw', 'count']
    output['clean'] = np.nan
    return output.sort_values(by=['count','raw']).reset_index(drop=True)


def get_groups(group_file):
    df_tmp = pd.read_csv(group_file)
    option = prompt_col(data=df_tmp, title="Please select the group codings:")
    return df_tmp[option].tolist()


group_file = raw_data_path
groups = get_groups(group_file)
selected_column = prompt_col(data)
tmp_data = make_data(data, selected_column)

current_pct = 1-tmp_data.clean.isna().sum()/tmp_data.shape[0]

while current_pct < 1:
    tmp_id = tmp_data[tmp_data.clean.isna()]['count'].idxmax()
    title = (
        """
        {}% Complete
        Please select group for:
          - {}
        """.format(round(current_pct*100, 2), tmp_data.iloc[tmp_id, 0])
    )
    options = groups
    option, index = pick(options, title)
    tmp_data.iloc[tmp_id, 2] = option
    tmp_data.iloc[tmp_id, 2] = option
    current_pct = 1-tmp_data.clean.isna().sum()/tmp_data.shape[0]
