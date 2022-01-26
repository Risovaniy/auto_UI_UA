# -*- coding: utf-8 -*-

import sys
from datetime import datetime
import locale
import os
import pandas as pd
import docx
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.shared import Inches
from bin.load_data import load_and_preprocessing_data, read_config_and_language

#####################################################
#                                                   #
#                General logic                      #
#                                                   #
#####################################################

CONFIG, LANGUAGE = read_config_and_language()


def create_docx_fmt():
    """Create a document with a font name 'Times New Roman', font size is 12 Pt

    :return: New formatted blank document
    :rtype: docx.document.Document

    """
    # Initial Document object
    new_doc = docx.Document()


    # Specify the main name and font size for the document
    new_doc.styles['Normal'].font.name = 'Times New Roman'
    new_doc.styles['Normal'].font.size = docx.shared.Pt(12)

    return new_doc


def create_table_fmt(document, count_rows, count_cols):
    """Create a table in document size = (count_rows X count_cols)

    :param document: The document to which the table is added
    :type document: docx.document.Document
    :param count_rows: Count of rows of the table
    :type count_rows: int
    :param count_cols: Count of columns of the rows
    :type count_cols: int
    :return: The table with minimal formatting
    :rtype: docx.table.Table

    """
    # Initial the table
    table = document.add_table(rows=count_rows, cols=count_cols)

    # Alignment of the table to the center of the file
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Set the style to the table
    table.style = 'Table Grid'

    return table


#####################################################
#                                                   #
#                   UI LOGIC                        #
#                                                   #
#####################################################
def create_column_names_ui(current_table):
    """Create names for column in table of UI, prepare a table to filling.

    :param current_table: The empty table with styles and simple formatting
    :type current_table: docx.table.Table
    :return: The table with the correct names of the columns
    :rtype: docx.table.Table
    """
    # Create table with column names with an italic formatting
    current_table.cell(0, 0).text = 'п/п'
    current_table.cell(0, 0).paragraphs[0].alignment = WD_TABLE_ALIGNMENT.CENTER

    current_table.cell(0, 1).text = 'Полные ФИО автора РИД'
    current_table.cell(0, 1).paragraphs[0].alignment = WD_TABLE_ALIGNMENT.CENTER

    run_job = current_table.cell(0, 2).paragraphs[0].add_run()
    run_job.text = 'Сокращенное наименование организации-работодателя, ' \
                   'наименование структурного подразделения и должности ' \
                   'автора РИД '
    # Добавление курсивного текста
    run_job_help = current_table.cell(0, 2).paragraphs[0].add_run()
    run_job_help.text = '(на момент создания РИД)'
    run_job_help.italic = True
    current_table.cell(0, 2).paragraphs[0].alignment = WD_TABLE_ALIGNMENT.CENTER

    # run_agreement = current_table.cell(0, 3).paragraphs[0].add_run()
    current_table.cell(0, 3).paragraphs[0].add_run().text = \
        'Согласование включения в состав авторов (Не требуется / Получено ' \
        '(реквизиты письма о согласовании, при наличии) / ' \
        'Требуется согласование в Корпорации)'
    current_table.cell(0, 3).paragraphs[0].alignment = WD_TABLE_ALIGNMENT.CENTER

    return current_table


def create_df_ui(df_authors):
    """Creates a dataframe for the table in the Notification of Performers:
    | № | Full name | Place of work and position | Consent |

    :param df_authors: Source dataframe with all data on authors
    :type df_authors: pandas.core.frame.DataFrame
    :return: Dataframe for notifying performers
    :rtype: pandas.core.frame.DataFrame

    """
    try:
        # Initial an empty dataframe create uvedomlenie ispolniteley
        finish_df = pd.DataFrame()

        # Create the first column "serial number"
        finish_df['number'] = pd.Series(range(1, len(df_authors) + 1)).astype(str)

        # Create the full names of authors (ФИО)
        finish_df['full_name'] = df_authors['last_name'] + "\n" + \
                                 df_authors['first_name'] + "\n" + \
                                 df_authors['middle_name']

        # work_place is [organisation,\n post,\n academic]
        finish_df['work_place'] = df_authors['job'] + ",\n" + \
                                  df_authors['post'] + ",\n" + \
                                  df_authors['academic']
        # Delete marked absences of academic rank
        finish_df['work_place'] = finish_df['work_place'].apply(del_end_comma)

        # Create the approval column by default
        finish_df['approval'] = 'Не требуется'

        return finish_df
    except KeyError:
        raise KeyError(sys.exc_info())


def del_end_comma(element):
    """Remove the last "empty" comma

    :param element: Element from the 'work_space' column
    :type element: str
    :return: Correct value, without extra characters
    :rtype: str

    """
    # Remove leading and ending whitespace characters from name of the columns
    element = str(element).strip()

    # Find and remove the last and useless comma from the end of the line
    if element[-1] == ',':
        element = element[:-1]

    return element


def create_UI_docx(df_UI, path_dir_to_save):
    """Create a document (.docx) for UI and fill this doc a data about authors

    :param df_UI: Dataframe with special processing info about authors for UI
    :type df_UI: pandas.core.frame.DataFrame
    :param path_dir_to_save: The path to the directory to save the created files
    :type path_dir_to_save: str
    :return: Save 'table_for_UI.docx' document
    :rtype: None

    """
    # Initial Document object
    doc = create_docx_fmt()

    # Set a shape of the table
    table_rows, table_cols = df_UI.shape

    # Initial the table
    my_table = doc.add_table(rows=(table_rows + 1), cols=table_cols)

    # Set the style to the table
    my_table.style = 'Table Grid'

    # Add the column names with right formatting
    my_table = create_column_names_ui(my_table)

    # Fill the table
    for row in range(table_rows):
        for col in range(table_cols):

            # Get a cell from the table
            cell = my_table.cell((row + 1), col)

            # Write our data into cell
            cell.text = df_UI.iloc[row, col]

            # Center alignment of text inside a special cell (first and last)
            if col in (0, 3):
                cell.paragraphs[0].alignment = WD_TABLE_ALIGNMENT.CENTER
                cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

    # Save the newly created file in .docx format
    created_date = datetime.now().strftime('(%Y-%m-%d_%H-%M)')
    current_name = CONFIG.get(LANGUAGE, '-filename_UI-')
    doc.save(f"{path_dir_to_save}{os.sep}{current_name}{created_date}.docx")


def generate_file_UI(df_authors, dir_for_save=''):
    """The finished function for the full cycle of UI generation

    :param df_authors: A row dataframe with info about authors
    :type df_authors: pandas.core.frame.DataFrame
    :param dir_for_save: The path to the directory to save the created UI
    :type dir_for_save: str
    :return: Save table for UI document (.docx)
    :rtype: None

    """
    # Processing the df_input for table in UI.docx document
    df_UI = create_df_ui(df_authors)

    # Create UI.docx file with generated table for copying in the main UI

    create_UI_docx(df_UI, dir_for_save)


#####################################################
#                                                   #
#                   UA LOGIC                        #
#                    part1                          #
#####################################################
def create_df_ua_part1(df_authors):
    """Preparing a dataframe for creating the first part of the UA
    (long text for each author)

    :param df_authors: The original dataframe with all data about the authors
    :type df_authors: pandas.core.frame.DataFrame
    :return: Dataframe with info specifically for the first part of the UA
    :rtype: pandas.core.frame.DataFrame

    """
    try:
        finish_df = pd.DataFrame()

        # Full name for the first string
        finish_df['full_name'] = df_authors['last_name'] + ' ' + \
                                 df_authors['first_name'] + ' ' + \
                                 df_authors['middle_name']

        # It's a datetime column (employment contract or not)
        finish_df['date_employ'] = pd.to_datetime(df_authors['date_employ'])

        # Name and number of contract
        finish_df['contract'] = df_authors['contract']

        # Contribution of each authors in the total result
        finish_df['contribution'] = df_authors['contribution']

        return finish_df
    except KeyError:
        raise KeyError(sys.exc_info())


def generate_text_for_one(df_row, doc, organization):
    """Adding to the document (UA.docx ) the text part for the author from this
    df_row

    :param df_row: A string from a dataframe with information from one author
    :type df_row: pandas.core.series.Series
    :param doc: The document in which to write the text part by the author
    :type doc: docx.document.Document
    :param organization: The organization that we are notifying
    :type organization: str
    :return: The document with added text information about the author
    :rtype: docx.document.Document

    """
    doc.add_paragraph()

    # First number is the paragraph, second number - run in this paragraph
    run_0_0 = doc.paragraphs[-1].add_run()
    run_0_0.text = "Я, "

    run_0_1 = doc.paragraphs[-1].add_run()
    run_0_1.text = f"\t\t{df_row['full_name']}\t\t\t\t\t,"
    run_0_1.font.underline = True

    doc.add_paragraph()

    doc.paragraphs[-1].alignment = WD_TABLE_ALIGNMENT.CENTER
    run_1 = doc.paragraphs[-1].add_run()
    run_1.text = "(ФИО автора)"
    # run_1.font = docx.shared.Pt(10)

    doc.add_paragraph()

    run_2_0 = doc.paragraphs[-1].add_run()
    run_2_0.text = "настоящим уведомляю "

    run_2_1 = doc.paragraphs[-1].add_run()
    run_2_1.text = f"\t\t{organization}\t\t\t\t\t"
    run_2_1.font.underline = True

    doc.add_paragraph()

    doc.paragraphs[-1].alignment = WD_TABLE_ALIGNMENT.CENTER
    run_3 = doc.paragraphs[-1].add_run()
    run_3.text = "(название Организации)"
    # run_3.font = docx.shared.Pt(10)

    doc.add_paragraph()

    run_4 = doc.paragraphs[-1].add_run()
    run_4.text = "о том, что будучи"

    # Logic for own or not employers
    doc.add_paragraph()

    if type(df_row['date_employ']) != pd._libs.tslibs.nattype.NaTType:
        run_5_0 = doc.paragraphs[-1].add_run()
        run_5_0.text = "☒ работником указанной организации на основании " \
                       "трудового договора от «"

        employ_date = df_row['date_employ']

        # Write a day
        run_5_1 = doc.paragraphs[-1].add_run()
        run_5_1.text = str(employ_date.strftime("%d"))
        run_5_1.font.underline = True

        # Write the space between the day and month
        run_5_2 = doc.paragraphs[-1].add_run()
        run_5_2.text = "» "

        # Write a month
        run_5_3 = doc.paragraphs[-1].add_run()
        run_5_3.text = str(employ_date.strftime("%m"))
        run_5_3.font.underline = True

        # Write the space between the month and year
        run_5_4 = doc.paragraphs[-1].add_run()
        run_5_4.text = " "

        # Write the year
        run_5_5 = doc.paragraphs[-1].add_run()
        run_5_5.text = str(employ_date.year)
        run_5_5.font.underline = True

    else:
        run_5 = doc.paragraphs[-1].add_run()
        run_5.text = "☐ работником указанной организации на основании " \
                     "трудового договора от «   »      20   "

    doc.add_paragraph()
    run_6 = doc.paragraphs[-1].add_run()
    run_6.text = "\t\tи действуя"

    doc.add_paragraph()
    run_7 = doc.paragraphs[-1].add_run()
    run_7.text = "\t\t☐ в рамках своих служебных обязанностей в соответствии с ____________ " \
                 "_____________________________________________________________________________;"

    doc.add_paragraph()
    doc.paragraphs[-1].alignment = WD_TABLE_ALIGNMENT.CENTER
    run_8 = doc.paragraphs[-1].add_run()
    run_8.text = "(номера пунктов трудового договора и / или должностной инструкции)"
    # run_8.font = docx.shared.Pt(10)

    doc.add_paragraph()
    run_9 = doc.paragraphs[-1].add_run()
    run_9.text = "\t\t☒ на основании служебного задания, предусмотренного _________"

    doc.add_paragraph()
    doc.paragraphs[-1].alignment = WD_TABLE_ALIGNMENT.CENTER
    run_10_0 = doc.paragraphs[-1].add_run()
    run_10_0.text = '__________'

    run_10_1 = doc.paragraphs[-1].add_run()
    run_10_1.text = df_row['contract']
    run_10_1.font.underline = True

    run_10_2 = doc.paragraphs[-1].add_run()
    run_10_2.text = '__________;'

    doc.add_paragraph()
    doc.paragraphs[-1].alignment = WD_TABLE_ALIGNMENT.CENTER
    run_11 = doc.paragraphs[-1].add_run()
    run_11.text = "(наименование документа, регламентирующего выданное работнику задание)"

    doc.add_paragraph()
    run_12 = doc.paragraphs[-1].add_run()
    run_12.text = "☐ исполнителем по договору №______________ от «____» _______________ 20____ г.,"

    # White space
    doc.add_paragraph()

    doc.add_paragraph()
    run_13 = doc.paragraphs[-1].add_run()
    run_13.text = "я создал охраноспособный результат интеллектуальной деятельности."

    # White space
    doc.add_paragraph()

    doc.add_paragraph()
    run_14_0 = doc.paragraphs[-1].add_run()
    run_14_0.text = "Творческий вклад: __________"
    run_14_1 = doc.paragraphs[-1].add_run()
    run_14_1.text = df_row['contribution']
    run_14_1.font.underline = True
    run_14_2 = doc.paragraphs[-1].add_run()
    run_14_2.text = "_____________________________"

    # White spaces x2
    doc.add_paragraph()
    doc.add_paragraph()

    return doc


def create_doc_with_UA_1part(df_authors):
    """Creating the text part of the UA in a doc file, by all authors

    :param df_authors: Prepared dataframe with authors data for the text block
    :type df_authors: pandas.core.frame.DataFrame
    :return: Doc file with the finished first (text) part of the UA
    :rtype: docx.document.Document

    """
    df = create_df_ua_part1(df_authors)

    finish_doc = create_docx_fmt()

    org = "АО «ГНЦ РФ ТРИНИТИ»"

    for index in df.index:
        finish_doc = generate_text_for_one(df.iloc[index], finish_doc, org)

    return finish_doc


#####################################################
#                                                   #
#                   UA LOGIC                        #
#                    part2                          #
#####################################################
def create_df_ua_part2(df_authors):
    """Preparing a dataframe for creating the second part (table) of the UA

    :param df_authors: The original dataframe with all data about the authors
    :type df_authors: pandas.core.frame.DataFrame
    :return: Dataframe with info specifically for the second part of the UA
    :rtype: pandas.core.frame.DataFrame

    """
    # Initial an empty dataframe create UI
    try:
        finish_df = pd.DataFrame()
        finish_df['name'] = df_authors['last_name'] + ' ' + \
                            [x[:1] for x in df_authors['first_name']] + '.' + \
                            [x[:1] for x in df_authors['middle_name']] + '.'
        # Remove double dot for events when not exist a middle name
        finish_df['name'] = finish_df['name'].\
            apply(lambda x: str(x).replace('..', '.'))

        finish_df['date_UA'] = df_authors['date_UA']
        return finish_df

    except KeyError:
        raise KeyError(sys.exc_info())


def create_UA_docx(doc, df_UA, path_dir_to_save):
    """Add the table in UA and save the result UA document (both text and table)

    :param doc: Doc with added text by authors
    :type doc: docx.document.Document
    :param df_UA: Prepared dataframe with authors data for the table
    :type df_UA: pandas.core.frame.DataFrame
    :param path_dir_to_save: The path to the directory to save the created doc
    :type path_dir_to_save: str
    :return: Saves the created UA document (both text and table)
    :rtype: None

    """
    # Space between the text about the authors and the table with signatures
    [doc.add_paragraph()]*5

    # Calculate a shape of the table
    count_authors = df_UA.shape[0]
    table_rows = count_authors * 3
    table_cols = 3

    # Initial the table
    table = create_table_fmt(doc, table_rows, table_cols)

    # Processing for formatting
    font_size_hint = docx.shared.Pt(9)

    # To write a month in letters in Russian
    locale.setlocale(locale.LC_ALL, '')

    # Fill the table of the data
    for row in range(table_rows):
        # Short cell names of one row of the table
        cell_0 = table.cell(row, 0)
        cell_1 = table.cell(row, 1)
        cell_2 = table.cell(row, 2)

        if (row + 1) % 3 == 1:
            # For signature the

            # Center alignment of text inside a cell
            cell_0.paragraphs[0].alignment = WD_TABLE_ALIGNMENT.CENTER
            run_0 = cell_0.paragraphs[0].add_run()
            # Filling a cell with text
            run_0.text = '________________/'

            # Center alignment of text inside a cell
            cell_1.paragraphs[0].alignment = WD_TABLE_ALIGNMENT.CENTER
            run_1 = cell_1.paragraphs[0].add_run()
            # Filling a cell with text
            run_1.text = df_UA['name'].iloc[int(row / 3)]
            # Make underline at the name of an author
            run_1.font.underline = True

            # Center alignment of text inside a cell
            cell_2.paragraphs[0].alignment = WD_TABLE_ALIGNMENT.CENTER
            run_2 = cell_2.paragraphs[0].add_run()
            # Filling a cell with text
            run_2.text = create_sign_date(date=df_UA['date_UA'].iloc[int(row / 3)])

        elif (row + 1) % 3 == 2:

            # Center alignment of text inside cells
            cell_0.paragraphs[0].alignment = WD_TABLE_ALIGNMENT.CENTER
            cell_1.paragraphs[0].alignment = WD_TABLE_ALIGNMENT.CENTER

            run_0 = cell_0.paragraphs[0].add_run()
            run_1 = cell_1.paragraphs[0].add_run()

            # Filling cells with text
            run_0.text = '(подпись)'
            run_1.text = '(Фамилия И. О.)'

            # Setting the font size of the cell text
            run_0.font.size = font_size_hint
            run_1.font.size = font_size_hint

    # Save the newly created file in .docx format
    created_date = datetime.now().strftime('(%d-%m-%Y_%H-%M)')
    current_name = CONFIG.get(LANGUAGE, '-filename_UA-')
    doc.save(f"{path_dir_to_save}{os.sep}{current_name}{created_date}.docx")


def create_sign_date(date):
    """Creating a line with the signature date in the desired design

    :param date: The date of signing of the UA,If there is no value,
                 then a mask is created to enter the date manually
    :type date: str
    :return: The date in the desired format for insertion into the table
    :rtype: str

    """
    if date == '':
        sign_date = f'Дата: «__» __ 20__г.'

    else:
        dateFormatter = "%d.%m.%y"
        date = datetime.strptime(str(date), dateFormatter)
        sign_date = f'Дата: «{date.strftime("%d")}» {date.strftime("%m")} {date.year}г.'

    return sign_date


def generate_file_UA(df_authors, dir_for_save=''):
    """Creating the UA doc file based on the authors' data

    :param df_authors: The original dataframe with all the info about the authors
    :type df_authors: pandas.core.frame.DataFrame
    :param dir_for_save: The path to the directory to save the created file
    :type dir_for_save: str
    :return: Save the created file
    :rtype: None

    """
    # Create doc with text part of UA
    doc_with_text_UA = create_doc_with_UA_1part(df_authors)

    # Adding the table create_df_ua_part2(df_in)

    create_UA_docx(doc_with_text_UA, create_df_ua_part2(df_authors),
                   dir_for_save)


def make_UI_and_UA(path_to_authors_data, dir_for_save_file):
    """Launch creating UI and UA

    :param path_to_authors_data: The path to the source data about the authors
    :type path_to_authors_data: str
    :param dir_for_save_file: The path to the directory to save the created docs
    :type dir_for_save_file: str
    :return: Saved doc files
    :rtype: None

    """
    df_in = load_and_preprocessing_data(path_to_authors_data)

    generate_file_UI(df_in, dir_for_save=dir_for_save_file)
    generate_file_UA(df_in, dir_for_save=dir_for_save_file)


def make_only_UI(path_to_authors_data, dir_for_save_file):
    """Launch creating only UI

    :param path_to_authors_data: The path to the source data about the authors
    :type path_to_authors_data: str
    :param dir_for_save_file: The path to the directory to save the created file
    :type dir_for_save_file: str
    :return: Saved a doc file
    :rtype: None

    """
    df_in = load_and_preprocessing_data(path_to_authors_data)

    generate_file_UI(df_in, dir_for_save_file)


def make_only_UA(path_to_authors_data, dir_for_save_file):
    """Launch creating only UA

    :param path_to_authors_data: The path to the source data about the authors
    :type path_to_authors_data: str
    :param dir_for_save_file: The path to the directory to save the created file
    :type dir_for_save_file: str
    :return: Saved a doc file
    :rtype: None

    """
    df_in = load_and_preprocessing_data(path_to_authors_data)

    generate_file_UA(df_in, dir_for_save=dir_for_save_file)
