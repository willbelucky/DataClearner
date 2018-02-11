# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2018. 1. 8.
"""
from data_cleaner import *


def get_stock_daily_price():
    stock_masters = pd.read_csv(get_source_path('stock_master', 'csv'), low_memory=False)
    stock_daily_prices = pd.read_csv(get_source_path('stock_daily_price', 'csv'), low_memory=False,
                                     parse_dates=['date'])
    stock_daily_prices['short_code'] = 'A' + stock_daily_prices['code']
    stock_daily_prices = stock_daily_prices.drop('code', axis=1)
    stock_daily_prices = pd.merge(stock_daily_prices, stock_masters, on=['short_code'])
    stock_daily_prices = stock_daily_prices.drop('short_code', axis=1)
    stock_daily_prices = stock_daily_prices.drop('company_name', axis=1)
    stock_daily_prices = stock_daily_prices.drop('market_name', axis=1)
    stock_daily_prices = stock_daily_prices.set_index(['code', 'date'])
    stock_daily_prices.loc[stock_daily_prices['volume'] == 0.0, 'open'] = \
        stock_daily_prices['close']
    stock_daily_prices.loc[stock_daily_prices['volume'] == 0.0, 'high'] = \
        stock_daily_prices['close']
    stock_daily_prices.loc[stock_daily_prices['volume'] == 0.0, 'low'] = \
        stock_daily_prices['close']

    return stock_daily_prices


if __name__ == '__main__':
    stock_daily_prices = get_stock_daily_price()
    stock_daily_prices.to_csv(get_target_path('stock_daily_price', 'csv'))
