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

    # Delete ['turnover']
    merged_data = merged_data.drop(columns=['turnover'], axis=1)

    # Get a set of datetime from 09:00 to 13:30 for every business day.
    # And fill blank data.
    date_set = set(merged_data['date'])
    minutes = pd.DataFrame(data=date_set, columns=['date'])
    merged_data = pd.merge(merged_data, minutes, on=['date'], how='outer')
    merged_data['volume'] = merged_data['volume'].fillna(0)
    merged_data['close'] = merged_data['close'].fillna(method='ffill')
    merged_data['close'] = merged_data['close'].fillna(method='bfill')
    merged_data['open'] = merged_data['open'].fillna(merged_data['close'])
    merged_data['high'] = merged_data['high'].fillna(merged_data['close'])
    merged_data['low'] = merged_data['low'].fillna(merged_data['close'])

    # Set index
    merged_data = merged_data.set_index(keys=['code', 'date'])

    return merged_data


def adjust_minute_price(stock_minute_prices, stock_daily_prices):
    """
    Adjust open, high, low, close prices of stock_minute_prices by stock_daily_prices.

    :param stock_minute_prices:
    :param stock_daily_prices:
    :return adjusted_stock_minute_prices:
    """
    stock_daily_prices['adj_close'] = stock_daily_prices['market_capitalization'] / stock_daily_prices['listed_stocks_number']
    stock_daily_prices['adj_ratio'] = stock_daily_prices['adj_close'] / stock_daily_prices['close']

    stock_minute_prices['just_date'] = stock_minute_prices.index.get_level_values(1).str.slice(0, 10)
    stock_daily_prices['just_date'] = stock_daily_prices['date'].str.slice(0, 10)

    print(type(stock_minute_prices['just_date'][0]))
    print(type(stock_daily_prices['just_date'][0]))

    print(stock_daily_prices.head())
    print(stock_minute_prices.head())

    adjusted_stock_minute_prices = pd.merge(stock_minute_prices, stock_daily_prices[['just_date', 'adj_ratio']], on=['just_date'])

    print(adjusted_stock_minute_prices.head())

    adjusted_stock_minute_prices['open'] = adjusted_stock_minute_prices['open'] * adjusted_stock_minute_prices['adj_ratio']
    adjusted_stock_minute_prices['high'] = adjusted_stock_minute_prices['high'] * adjusted_stock_minute_prices['adj_ratio']
    adjusted_stock_minute_prices['low'] = adjusted_stock_minute_prices['low'] * adjusted_stock_minute_prices['adj_ratio']
    adjusted_stock_minute_prices['close'] = adjusted_stock_minute_prices['close'] * adjusted_stock_minute_prices['adj_ratio']

    adjusted_stock_minute_prices = adjusted_stock_minute_prices.drop('adj_ratio', axis=1)
    adjusted_stock_minute_prices = adjusted_stock_minute_prices.drop('just_date', axis=1)

    print(adjusted_stock_minute_prices.head())

    return adjusted_stock_minute_prices


if __name__ == '__main__':
    # file_name = 'stock_minute_price'
    #
    # source_file_names = get_file_names()
    #
    # merged_data = merge_minute_price(source_file_names)
    # merged_data.to_csv(get_target_path(file_name, extension='csv'))

    stock_minute_prices = pd.read_hdf('source/{}.h5'.format('stock_minute_price'), 'table', encoding='utf-8')
    stock_daily_prices = pd.read_csv('source/{}.csv'.format('stock_daily_price'), encoding='utf-8', low_memory=False)
    adjusted_stock_minute_prices = adjust_minute_price(stock_minute_prices, stock_daily_prices)
    adjusted_stock_minute_prices.to_csv('target/{}.csv'.format('stock_minute_price'))
