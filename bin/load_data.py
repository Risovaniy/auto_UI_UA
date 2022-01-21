# -*- coding: utf-8 -*-

"""Loading source data into a dataframe about authors and initial preprocessing
of this dataframe"""
import re
import sys

import pandas as pd
import os.path
from pandas_ods_reader import read_ods


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
    """Loading source data from a file into a DataFrame, an error is thrown when
    a failure occurs.

    Additional installing for different formats:
    odf  - pip install odfpy
    xls  - pip install xlrd
    xlsx - pip install openpyxl
    read_ods - pip install pandas-ods-reader

    :param full_filename: Full path to the source data file
    :type full_filename: str
    :param separator: Separator in csv and txt files
    :type separator: str
    :return: DataFrame with source data about authors
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

            else:
                # Unsupported a file format
                raise sys.exc_info()

        else:
            # It was not possible to get its extension from the full file path
            raise sys.exc_info()

    else:
        # The file specified by this path does not exist
        raise sys.exc_info()


def check_input_df_for_UI(input_df):
    """Check of the necessary columns in the input_df for the UI
    Required columns:
    'last_name': 'Фамилия'
    'first_name': 'Имя'
    'middle_name': 'Отчество'
    'job': 'Место работы'
    'post': 'Должность'
    'academic': 'Ученое звание'

    :param input_df: A DaraFrame with data about authors, newly loaded
    :type input_df: pandas.core.frame.DataFrame
    :return: The verdict on the availability of all the necessary columns
    :rtype: bool

    """
    necessary_name = {'last_name', 'first_name', 'middle_name', 'job', 'post',
                      'academic'}
    input_names = set(input_df.columns)
    set(necessary_name).issubset(input_names)




def check_input_df_for_UA(input_df):
    """Check of the necessary columns in the input_df for the UA
    Required columns
    'last_name': 'Фамилия'
    'first_name': 'Имя'
    'middle_name': 'Отчество'
    'date_employ': 'Дата трудоустройства'
    'contract': 'Контракт/Договор'
    'contribution': 'Творческий вклад'

    :param input_df: A DaraFrame with data about authors, newly loaded
    :type input_df: pandas.core.frame.DataFrame
    :return: The verdict on the availability of all the necessary columns
    :rtype: bool

    """
    necessary_name = {'last_name', 'first_name', 'middle_name', 'date_employ',
                      'contract', 'contribution'}
    input_names = set(input_df.columns)
    set(necessary_name).issubset(input_names)



def rename_columns(df_raw):
    """Rename the columns of the original raw dataframe using a dictionary

    :param df_raw: A DaraFrame with data about authors, newly loaded
    :type df_raw: pandas.core.frame.DataFrame
    :return: DF with new column names that are used in the documents creating
    :rtype: pandas.core.frame.DataFrame

    """
    # Dictionary for unambiguous renaming of columns, so as not to depend on
    # the order of the columns themselves
    dict_for_renaming = {'Фамилия': 'last_name',
                         'Имя': 'first_name',
                         'Отчество': 'middle_name',
                         'Должность': 'post',
                         'Ученое звание': 'academic',
                         'Место работы': 'job',
                         'Творческий вклад': 'contribution',
                         'Контракт/Договор': 'contract',
                         'Дата трудоустройства': 'date_employ'}

    df_renamed_cols = df_raw.rename(dict_for_renaming, axis=1)

    return df_renamed_cols


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
