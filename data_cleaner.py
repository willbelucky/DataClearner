# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2017. 11. 24.
"""
import pandas as pd
import progressbar


def get_source_path(file_name, extension='xlsx'):
    """

    :param file_name: (str)
    :param extension: (str) one of 'xlsx', 'csv', 'h5'
    :return path_to_file: (str)
    """
    assert extension in ['xlsx', 'csv', 'h5']
    return './source/' + file_name + '.' + extension


def get_target_path(file_name, extension='xlsx'):
    """

    :param file_name: (str)
    :param extension: (str) one of 'xlsx', 'csv', 'h5'
    :return path_to_file: (str)
    """
    assert extension in ['xlsx', 'csv', 'h5']
    return './target/' + file_name + '.' + extension


def get_excel_data(file_name, sheet_name):
    return pd.read_excel(open(get_source_path(file_name), 'rb'), sheet_name=sheet_name)


def get_sheet_names(file_name):
    return pd.ExcelFile(get_source_path(file_name), on_demand=True).sheet_names


def get_merged_data(file_name, vertical_axis_name='code', horizontal_axis_name='date', vertical_number_only=False):
    sheet_names = get_sheet_names(file_name)

    # Initialize result DataFrame.
    result_data = pd.DataFrame(columns=[])

    # Initialize a progressbar.
    widgets = [progressbar.Percentage(), progressbar.Bar(), progressbar.DynamicMessage('sheet_name')]
    bar = progressbar.ProgressBar(widgets=widgets, max_value=(len(sheet_names) + 1)).start()
    for index, sheet_name in enumerate(sheet_names):
        bar.update(index + 1, sheet_name=sheet_name)
        original_data = get_excel_data(file_name, sheet_name)
        flatten_data = pd.melt(original_data, id_vars=[vertical_axis_name], var_name=horizontal_axis_name,
                               value_name=sheet_name)

        # If vertical_number_only is True, extract only number from vertical_axis_name column.
        if vertical_number_only:
            flatten_data[vertical_axis_name] = flatten_data[vertical_axis_name].str.extract('(\d+)', expand=False)

        flatten_data = flatten_data.set_index(keys=[vertical_axis_name, horizontal_axis_name])
        result_data = pd.concat([result_data, flatten_data], axis=1, join='outer')

    # Finish the progressbar.
    bar.finish()

    result_data = result_data.dropna()
    return result_data


def get_writer(file_name):
    return pd.ExcelWriter(get_target_path(file_name), engine='xlsxwriter')
