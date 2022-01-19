# -*- coding: utf-8 -*-

"""Loading source data into a dataframe about authors and initial preprocessing
of this dataframe"""
import re
import pandas as pd
import os.path
from pandas_ods_reader import read_ods

# from main import write_to_log

# STOP HERE!!!
# ToDo: Add to load fns for only UI and only UA creating (need fewer columns)
def check_exists_file(filename):
    """The simple file existence check

    :param filename: The full or relative path and name of the file
    :type filename: str
    :return: True if the file is existing, False in otherwise
    :rtype: bool
    """
    return os.path.exists(filename)


def extract_extension_from_filename(filename):
    """According to the template, I get only its extension from the file name

    :param filename: The full or relative path and name of the file
    :type filename: str
    :return: Extension of the transferred file
    :rtype: str

    """
    # Splitting separating the file extension from the file name itself
    split_filename = re.search('(.+)(\.)([a-z]+$)', filename)
    # $ - binds to the end of the string,
    # the characters before $ should end the string

    # Checking for a fool, whether the name fits the template
    if split_filename:
        return split_filename.groups()[-1]

    return None


def load_file_to_df(full_filename, separator=';'):
    """Loading source data from a file into a DataFrame
    Additional installing for different formats:
    odf  - pip install odfpy
    xls  - pip install xlrd
    xlsx - pip install openpyxl
    read_ods - pip install pandas-ods-reader

    :param full_filename: Full path to the source data file
    :type full_filename: str
    :param separator: Separator in csv and txt files
    :type separator: str
    :return: DataFrame with source data about authors.
     If get an error - "None"
    :rtype: pandas.core.frame.DataFrame

    """
    # Removing leading and ending whitespace characters
    full_filename = full_filename.strip()

    if check_exists_file(full_filename):
        extension = extract_extension_from_filename(full_filename)
        if extension:
            office_MS_extension = ['xlsx', 'xls', 'xlsm', 'xlsb']
            office_Open_extension = ['ods', 'odt', 'xods', 'xots']
            csv_extension = ['csv', 'txt']

            if extension in office_MS_extension:
                return pd.read_excel(full_filename)

            elif extension in office_Open_extension:
                return read_ods(full_filename)

            elif extension in csv_extension:
                return pd.read_csv(full_filename, sep=separator)

        # write_to_log(
        #     f'This file format {extension} ({full_filename}) is not supported',
        #     fn_name='load_file_to_df',
        #     filename='load_data.py',
        #     line_number=57)

        return None

    # write_to_log(
    #     f'This file {full_filename} is not exist',
    #     fn_name='load_file_to_df',
    #     filename='load_data.py',
    #     line_number=64)

    return None


def rename_columns(df_raw):
    """Renames the columns of the original raw dataframe using a dictionary

    :param df_raw: A DaraFrame with data about authors, newly loaded
    :type df_raw: pandas.core.frame.DataFrame
    :return: DF with column names that are used in the document creation code.
    If we get an error - "None"
    :rtype: pandas.core.frame.DataFrame

    """
    # Dictionary for unambiguous renaming of columns, so as not to depend on
    # the order of the columns themselves
    dict_for_renaming = {'Фамилия': 'last_name',
                         'Имя': 'first_name',
                         'Отчество': 'middle_name',
                         'Должность и ученое звание': 'post',
                         'Место работы': 'job',
                         'Творческий вклад': 'contribution',
                         'Контракт/Договор': 'contract',
                         'Дата трудоустройства': 'date_employ'}

    # Renaming columns with protection from incorrect primary names
    try:
        df_renamed_cols = df_raw.rename(dict_for_renaming, axis=1)

        return df_renamed_cols

    except KeyError as error:
        print('Столбцы таблицы с исходными данными должны иметь следующие '
              'названия:\n'
              'Фамилия\n'
              'Имя\n'
              'Отчество\n'
              'Должность\n'
              'Место работы\n'
              'Творческий вклад\n'
              'Контракт/Договор\n'
              'Дата трудоустройства\n\n '
              f'P.S. Порядок колонок не важен.\n\n {error}')

        # write_to_log(
        #     f'Столбцы в исходных данных имеют некорректные названия '
        #     f'({df_raw.columns})',
        #     fn_name='rename_columns',
        #     filename='load_data.py',
        #     line_number=112)

        return None


def remove_first_last_whitespaces_from_df(df_raw):
    """Removes extra spaces from the end and beginning of all lines and
    names of columns

    :param df_raw: A DaraFrame with data about authors, newly loaded
    :type df_raw: pandas.core.frame.DataFrame
    :return: A clean dataframe without unnecessary start and end whitespaces
    :rtype: pandas.core.frame.DataFrame

    """
    # Remove leading and ending whitespace characters from name of the columns
    df_raw.columns = list(map(str.strip, df_raw.columns))

    # Remove leading and ending whitespace characters from features
    for col in df_raw.columns:
        df_raw[col] = df_raw[col].str.strip()

    return df_raw


def all_preprocessing_df(df_raw):
    """Starting preprocessing of a raw dataframe with data about authors

    :param df_raw: A DaraFrame with data about authors, newly loaded
    :type df_raw: pandas.core.frame.DataFrame
    :return: Preprocessed dataframe with data about authors
    :rtype: pandas.core.frame.DataFrame

    """
    result = remove_first_last_whitespaces_from_df(df_raw)

    result = rename_columns(result)

    return result


def load_and_preprocessing_data(full_filename, **kwargs):
    """Load data into df and a simple preprocessing one

    :param full_filename: Absolute filepath
    :type full_filename: str
    :param kwargs: To transfer the separator to csv
    :type kwargs: dict
    :return: Correct DF for further processing and operation in the program
    :rtype: pandas.core.frame.DataFrame

    """
    df_raw = load_file_to_df(full_filename, **kwargs)

    df_raw = all_preprocessing_df(df_raw)

    return df_raw
