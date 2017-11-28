# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2017. 11. 24.
"""
import pandas as pd


def get_source_path(file_name, extension='xlsx'):
    return './source/' + file_name + '.' + extension


def get_target_path(file_name, extension='xlsx'):
    return './target/' + file_name + '.' + extension


def get_flatten_data(file_name, sheet_name):
    return pd.read_excel(open(get_source_path(file_name), 'rb'), sheetname=sheet_name)


def get_sheet_names(file_name):
    return pd.ExcelFile(get_source_path(file_name), on_demand=True).sheet_names


def get_merged_data(file_name):
    sheet_names = get_sheet_names(file_name)

    result_data = pd.DataFrame(columns=[])
    for sheet_name in sheet_names:
        original_data = get_flatten_data(file_name, sheet_name)
        flatten_data = pd.melt(original_data, id_vars=['company'], var_name='year', value_name=sheet_name)
        flatten_data = flatten_data.set_index(keys=['company', 'year'])
        result_data = pd.concat([result_data, flatten_data], axis=1, join='outer')

    return result_data


def get_writer(file_name):
    return pd.ExcelWriter(get_target_path(file_name), engine='xlsxwriter')
