# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2017. 11. 24.
"""
from data_cleaner import *

if __name__ == '__main__':
    file_name = 'FE539'
    stock_data = get_merged_data(file_name, vertical_axis_name='company', horizontal_axis_name='year')
    stock_data = stock_data.dropna()
    stock_data.to_csv(get_target_path(file_name, extension='csv'))
    stock_data.to_excel(get_writer(file_name))
