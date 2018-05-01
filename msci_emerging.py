# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2018. 4. 28.
"""
from data_cleaner import *

if __name__ == '__main__':
    file_name = 'south_korea'
    stock_data = get_merged_data(file_name, vertical_axis_name='date', horizontal_axis_name='company')
    #stock_data = stock_data.bfill()
    stock_data.to_csv(get_target_path(file_name, extension='csv'))
