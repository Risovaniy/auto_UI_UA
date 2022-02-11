# -*- coding: utf-8 -*-

import sys
from datetime import datetime
import os
import pathlib as path
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

# ToDo Создать шаблоны документов: часть первая (которую можно дополнять),
#  часть вторая (у УИ - финишная закрывашка, у УА я еще поработаю с ней),
#  часть третья - только для УА - финишная закрывашка

# ToDo Почистить код, удалить неиспользуемые функции и документы, написать
#  документации и комментарии

# ToDo Сделать упаковку и установочный скрипт для Астра линукс и проверить на
#  работоспособность

# ToDo Прописать системные требования к проге (винда 7 не подходит)


def combine_word_documents(based_doc, path_merged_doc):
    """Copies the entire document from path_marged_doc to the end of based_doc
    Formatting of the copied elements is preserved if possible

    :param based_doc: The main doc at the end of which the new info is copied
    :type based_doc: docx.document.Document
    :param path_merged_doc: The path to the template to copy (my constants)
    :type path_merged_doc: str
    :return: Glued Word document
    :rtype: docx.document.Document

    """
    merged_doc = docx.Document(path_merged_doc)

    for element in merged_doc.element.body:
        based_doc.element.body.append(element)

    return based_doc


def save_to_docx(document, path_dir_to_save, filename_key):
    """Saves the Word document (AA or UI) to the desired directory with an
    indication of the creation date

    :param document: The document to be saved
    :type document: docx.document.Document
    :param path_dir_to_save: The path to the directory to save the word doc to
    :type path_dir_to_save: str
    :param filename_key: A key file name from configs
    :type filename_key: str
    :return: Just saves
    :rtype: None

    """
    # Save the newly created file in .docx format
    created_date = datetime.now().strftime('(%Y-%m-%d_%H-%M)')
    docx_name = CONFIG.get(LANGUAGE, filename_key)
    document.save(f"{path_dir_to_save}{os.sep}{docx_name}{created_date}.docx")


#####################################################
#                                                   #
#                   UI LOGIC                        #
#                                                   #
#####################################################

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
        finish_df['number'] = pd.Series(range(1, len(df_authors) + 1)).astype(
            str)

        # Create the full names of authors (ФИО)
        finish_df['full_name'] = df_authors['last_name'] + "\n" + \
                                 df_authors['first_name'] + "\n" + \
                                 df_authors['middle_name']

        # work_place is [organisation,\n post,\n academic]
        finish_df['work_place'] = df_authors['job'] + ",\n" + \
                                  df_authors['post'] + ",\n" + \
                                  df_authors['academic']
        # Delete marked absences of academic rank
        finish_df['work_place'] = finish_df['work_place'].apply(
            delete_final_comma)

        return finish_df
    except KeyError:
        raise KeyError(sys.exc_info())


def delete_final_comma(element):
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


def fill_table_in_ui(df_ui):
    """Open the 1-th part of UI document (.docx) and fill the table in this doc

    :param df_ui: Dataframe with special processing info about authors for UI
    :type df_ui: pandas.core.frame.DataFrame
    :return: The 1-th part of UI for saving
    :rtype: docx.document.Document

    """
    # Open of template for ui
    document = docx.Document(f'{path.Path.cwd()}{os.sep}resources{os.sep}ui_part_1.docx')

    # Take the last table (1.5 Authors)
    table = document.tables[-1]

    # Save parameters of the table
    table_rows = df_ui.shape[0]
    # table_cols = df_ui.shape[1]

    # Add all the rows in the table
    for _ in range(table_rows):
        table.add_row()

    # Create the approval column by default
    approval = 'Не требуется'

    # Fill the table
    for row in range(1, 2):
        # Skip headers
        for col in range(4):
            # Get a cell from the table
            cell = table.cell(row, col)

            # Write our data into cell
            if col == 3:
                cell.text = approval

            else:
                cell.text = df_ui.iloc[row, col]

            # Center alignment of text inside a special cell (first and last)
            if col in (0, 3):
                cell.paragraphs[0].alignment = WD_TABLE_ALIGNMENT.CENTER
                cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

    return document


def generate_file_ui(df_authors, dir_for_save=''):
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

    # Open template and fill the table
    document = fill_table_in_ui(df_UI)

    # Finishing of document
    path_merged_doc = f'{path.Path.cwd()}{os.sep}ui_finish.docx'
    document = combine_word_documents(document, path_merged_doc)

    # Save the document
    save_to_docx(document=document,
                 path_dir_to_save=dir_for_save,
                 filename_key='-filename_UI-')


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
    run_1.font.size = docx.shared.Pt(10)  # 8 it is just for tests

    doc.add_paragraph()

    run_2_0 = doc.paragraphs[-1].add_run()
    run_2_0.text = "настоящим уведомляю "

    run_2_1 = doc.paragraphs[-1].add_run()
    run_2_1.text = f"\t\t{organization}\t\t\t\t\t"
    run_2_1.font.underline = True

    doc.add_paragraph()

    doc.paragraphs[-1].alignment = WD_TABLE_ALIGNMENT.CENTER
    run_3 = doc.paragraphs[-1].add_run()
    run_3.text = "(название организации)"
    run_3.font.size = docx.shared.Pt(10)  # 8 it is just for tests

    doc.add_paragraph()

    run_4 = doc.paragraphs[-1].add_run()
    run_4.text = "о том, что будучи"

    # Logic for own or not employers
    doc.add_paragraph()

    if df_row['date_employ'] is not pd.NaT:
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

        run_5_6 = doc.paragraphs[-1].add_run()
        run_5_6.text = "г."
    else:
        run_5 = doc.paragraphs[-1].add_run()
        run_5.text = "☐ работником указанной организации на основании " \
                     "трудового договора от «___» ___ 20___г."

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
    run_8.font.size = docx.shared.Pt(10)

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
    run_11.font.size = docx.shared.Pt(10)

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
    [doc.add_paragraph()] * 2

    return doc


def create_doc_with_ua_1part(df_authors):
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
        finish_df['name'] = finish_df['name']. \
            apply(lambda x: str(x).replace('..', '.'))

        finish_df['date_UA'] = pd.to_datetime(df_authors['date_UA'])

        return finish_df

    except KeyError:
        raise KeyError(sys.exc_info())


def create_ua_docx(doc, df_ua, path_dir_to_save):
    """Add the table in UA and save the result UA document (both text and table)

    :param doc: Doc with added text by authors
    :type doc: docx.document.Document
    :param df_ua: Prepared dataframe with authors data for the table
    :type df_ua: pandas.core.frame.DataFrame
    :param path_dir_to_save: The path to the directory to save the created doc
    :type path_dir_to_save: str
    :return: Saves the created UA document (both text and table)
    :rtype: None

    """
    # Space between the text about the authors and the table with signatures
    [doc.add_paragraph()] * 5

    # Calculate a shape of the table
    count_authors = df_ua.shape[0]
    table_rows = count_authors * 3
    table_cols = 3

    # Initial the table
    table = create_table_fmt(doc, table_rows, table_cols)

    # Processing for formatting
    font_size_hint = docx.shared.Pt(9)

    # Fill the table with the data
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
            run_1.text = df_ua['name'].iloc[int(row / 3)]
            # Make underline at the name of an author
            run_1.font.underline = True

            # Center alignment of text inside a cell
            cell_2.paragraphs[0].alignment = WD_TABLE_ALIGNMENT.CENTER
            run_2 = cell_2.paragraphs[0].add_run()
            # Filling a cell with text
            run_2.text = create_sign_date(
                date=df_ua['date_UA'].iloc[int(row / 3)])

        elif (row + 1) % 3 == 2:

            # Center alignment of text inside cells
            cell_0.paragraphs[0].alignment = WD_TABLE_ALIGNMENT.CENTER
            cell_1.paragraphs[0].alignment = WD_TABLE_ALIGNMENT.CENTER

            run_0 = cell_0.paragraphs[0].add_run()
            run_1 = cell_1.paragraphs[0].add_run()

            # Filling cells with text
            run_0.text = '(подпись)'
            run_0.font.size = docx.shared.Pt(10)
            run_1.text = '(Фамилия И. О.)'
            run_1.font.size = docx.shared.Pt(10)

            # Setting the font size of the cell text
            run_0.font.size = font_size_hint
            run_1.font.size = font_size_hint

    # Save the newly created file in .docx format
    created_date = datetime.now().strftime('(%d-%m-%Y_%H-%M)')
    current_name = CONFIG.get(LANGUAGE, '-filename_UA-')
    doc.save(f"{path_dir_to_save}{os.sep}{current_name}{created_date}.docx")


def create_sign_date(date):
    """Creating a line with the signature date in the desired design

    :param date: The date of signing of the UA, If there is no value,
                 then a mask is created to enter the date manually
    :type date: pandas._libs.tslibs.timestamps.Timestamp
    :return: The date in the desired format for insertion into the table
    :rtype: str

    """
    if date is pd.NaT:
        sign_date = f'Дата: «__» __ 20__г.'

    else:
        sign_date = f'Дата: «{date.strftime("%d")}»' \
                    f' {date.strftime("%m")} {date.year}г.'

    return sign_date


def generate_file_ua(df_authors, dir_for_save=''):
    """Creating the UA doc file based on the authors' data

    :param df_authors: The original dataframe with all the info about the authors
    :type df_authors: pandas.core.frame.DataFrame
    :param dir_for_save: The path to the directory to save the created file
    :type dir_for_save: str
    :return: Save the created file
    :rtype: None

    """
    # Create doc with text part of UA
    doc_with_text_UA = create_doc_with_ua_1part(df_authors)

    # Adding the table create_df_ua_part2(df_in)

    create_ua_docx(doc_with_text_UA, create_df_ua_part2(df_authors),
                   dir_for_save)


def make_ui_and_ua(path_to_authors_data, dir_for_save_file):
    """Launch creating UI and UA

    :param path_to_authors_data: The path to the source data about the authors
    :type path_to_authors_data: str
    :param dir_for_save_file: The path to the directory to save the created docs
    :type dir_for_save_file: str
    :return: Saved doc files
    :rtype: None

    """
    df_in = load_and_preprocessing_data(path_to_authors_data)

    generate_file_ui(df_in, dir_for_save=dir_for_save_file)
    generate_file_ua(df_in, dir_for_save=dir_for_save_file)


def make_only_ui(path_to_authors_data, dir_for_save_file):
    """Launch creating only UI

    :param path_to_authors_data: The path to the source data about the authors
    :type path_to_authors_data: str
    :param dir_for_save_file: The path to the directory to save the created file
    :type dir_for_save_file: str
    :return: Saved a doc file
    :rtype: None

    """
    df_in = load_and_preprocessing_data(path_to_authors_data)

    generate_file_ui(df_in, dir_for_save_file)


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

    generate_file_ua(df_in, dir_for_save=dir_for_save_file)


#####################################################
#                                                   #
#          New version (use templates)              #
#                                                   #
#####################################################

def open_docx_file(path):
    return docx.Document(path)

    # return doc

# if __name__ == '__main__':
#     doc = open_docx_file('/home/risovaniy/auto_UI_UA/resources/UA_template.docx')
#
#     doc.add_paragraph()
#
#     # First number is the paragraph, second number - run in this paragraph
#     run_0_0 = doc.paragraphs[-1].add_run()
#     run_0_0.text = "Я, "
#
#     run_0_1 = doc.paragraphs[-1].add_run()
#     run_0_1.text = f"\t\tМоя информация строка 670\t\t\t\t\t,"
#     run_0_1.font.underline = True
#
#     doc.add_paragraph()
#
#     doc.paragraphs[-1].alignment = WD_TABLE_ALIGNMENT.CENTER
#     run_1 = doc.paragraphs[-1].add_run()
#     run_1.text = "(ФИО автора)"
#     run_1.font.size = docx.shared.Pt(10)  # 8 it is just for tests
#
#     doc.add_paragraph()
#
#     run_2_0 = doc.paragraphs[-1].add_run()
#     run_2_0.text = "настоящим уведомляю "
#
#     doc.save('/home/risovaniy/auto_UI_UA/trash/my_first_test.docx')
