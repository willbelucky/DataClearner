# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2017. 12. 14.
"""
from data_cleaner import *


def get_file_names():
    file_names = []
    for period in [1611, 1612, 1701, 1702, 1703, 1704, 1705, 1706, 1707, 1708, 1709, 1710, 1711]:
        file_names.append('source/kse1m{}.csv'.format(period))

    return file_names


def merge_minute_price(file_names):
    merged_data = pd.DataFrame()

    for file_name in file_names:
        new_data = pd.read_csv(file_name, header=None, sep='|', engine='c')
        merged_data = pd.concat([merged_data, new_data])

    # Set column names.
    merged_data.columns = ['date', 'code', 'time', 'open', 'high', 'low', 'close', 'volume', 'turnover']

    # ['date', 'time'] -> ['date'] and delete ['time']
    merged_data['date'] = merged_data['date'].apply(str)
    merged_data['time'] = merged_data['time'].apply(str)
    merged_data['time'] = merged_data['time'].str.pad(8, fillchar='0')
    merged_data['date'] = merged_data['date'] + merged_data['time']
    merged_data['date'] = merged_data['date'].str.slice(start=0, stop=12)
    merged_data = merged_data.drop(['time'], axis=1)
    merged_data['date'] = pd.to_datetime(merged_data['date'], format='%Y%m%d%H%M')

    # Make long codes to short codes
    merged_data['code'] = merged_data['code'].str.slice(start=3, stop=9)

    # Delete ['turnover']
    merged_data = merged_data.drop(columns=['turnover'], axis=1)

    # Set index
    merged_data = merged_data.set_index(keys=['code', 'date'])

    return merged_data


if __name__ == '__main__':
    file_name = 'volume'
    stock_data = get_merged_data(file_name, vertical_number_only=True)
    stock_data = stock_data.dropna()
    stock_data.to_csv(get_target_path(file_name, extension='csv'))
    stock_data.to_excel(get_writer(file_name))

    # file_names = get_file_names()
    # merged_data = merge_minute_price(file_names)
    # merged_data.to_csv(get_target_path(file_name, extension='csv'))
