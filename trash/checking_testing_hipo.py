# import pandas as pd
# #
# # df_xls_as_csv = pd.read_csv('authors_3p1.xls', sep=';', encoding='utf-8')
# # df_csv_as_xls = pd.read_excel('authors_3p1.csv', sep=';', encoding='utf-8')
# df_xls_as_xods = pd.read_excel('authors_3p1.xods')  # All right!!!
# # df_norm_csv = pd.read_csv('authors_3p1.csv', sep=';')  # All right!!!
# # df_norm_xls = pd.read_excel('authors_3p1.xls')  # All right!!!
# # df_xlsx = pd.read_excel('authors_3p1.xlsx')  # All right!!!
#
#
# print(
#     # 'df_xls_as_csv', df_xls_as_csv,
#     # 'df_csv_as_xls', df_csv_as_xls,
#     'df_xls_as_xods', df_xls_as_xods,  # All right!!! pip install odfpy
#     # 'df_xls_as_ods', df_xls_as_ods,  # All right!!! pip install odfpy
#     # 'df_norm_csv', df_norm_csv,  # All right!!!
#     # 'df_norm_xls', df_norm_xls,  # All right!!! pip install xlrd
#     # 'df_xlsx', df_xlsx,  # All right!!! pip install openpyxl
#
# )
# from bin.create_UI_UA import create_docx_fmt
# from docx.enum.table import WD_TABLE_ALIGNMENT
# import docx
# from docx.enum.table import WD_TABLE_ALIGNMENT
#
#
# def create_docx_fmt():
#     """Create a document with a font name 'Times New Roman', font size is 12 Pt
#
#     :return: New formatted blank document
#     :rtype: docx.document.Document
#
#     """
#     # Initial Document object
#     new_doc = docx.Document()
#
#     # ToDo Create a template in MS Word with my table style
#     # # Initial Document object
#     # new_doc = docx.Document('TEMPLATE_table_for_UA.docx')
#
#     # Specify the main name and font size for the document
#     new_doc.styles['Normal'].font.name = 'Times New Roman'
#     new_doc.styles['Normal'].font.size = docx.shared.Pt(12)
#
#     return new_doc
#
#
# def create_table_fmt(document, count_rows, count_cols):
#     """Create a table in document size = (count_rows X count_cols)
#
#     :param document: The document to which the table is added
#     :type document: docx.document.Document
#     :param count_rows: Count of rows of the table
#     :type count_rows: int
#     :param count_cols: Count of columns of the rows
#     :type count_cols: int
#     :return: The table with minimal formatting
#     :rtype: docx.table.Table
#
#     """
#     # Initial the table
#     table = document.add_table(rows=count_rows, cols=count_cols)
#
#     # Alignment of the table to the center of the file
#     table.alignment = WD_TABLE_ALIGNMENT.CENTER
#
#     # Set the style to the table
#     table.style = 'Table Grid'
#
#     table.cell(1, 2).test = 'Это по центру?'
#     table.cell(1, 5).test = 'по?'
#     table.cell(1, 1).test = 'кк'
#
#
#     return table
#
#
# def create_column_names_ui(current_table):
#     """Create names for column in table of UI, prepare a table to filling.
#
#     :param current_table: The empty table with styles and simple formatting
#     :type current_table: docx.table.Table
#     :return: The table with the correct names of the columns
#     :rtype: docx.table.Table
#     """
#     # Create table with column names with an italic formatting
#     current_table.cell(0, 0).text = 'п/п'
#     current_table.cell(0, 0).paragraphs[0].alignment = WD_TABLE_ALIGNMENT.CENTER
#
#     current_table.cell(0, 1).text = 'Полные ФИО автора РИД'
#     current_table.cell(0, 1).paragraphs[0].alignment = WD_TABLE_ALIGNMENT.CENTER
#
#     run_job = current_table.cell(0, 2).paragraphs[0].add_run()
#     run_job.text = 'Сокращенное наименование организации-работодателя, ' \
#                    'наименование структурного подразделения и должности ' \
#                    'автора РИД '
#     # Добавление курсивного текста
#     run_job_help = current_table.cell(0, 2).paragraphs[0].add_run()
#     run_job_help.text = '(на момент создания РИД)'
#     run_job_help.italic = True
#     current_table.cell(0, 2).paragraphs[0].alignment = WD_TABLE_ALIGNMENT.CENTER
#
#     # run_agreement = current_table.cell(0, 3).paragraphs[0].add_run()
#     current_table.cell(0, 3).paragraphs[0].add_run().text = \
#         'Согласование включения в состав авторов (Не требуется / Получено ' \
#         '(реквизиты письма о согласовании, при наличии) / ' \
#         'Требуется согласование в Корпорации)'
#     current_table.cell(0, 3).paragraphs[0].alignment = WD_TABLE_ALIGNMENT.CENTER
#
#     return current_table
#
# doc = create_docx_fmt()
#
#
# [doc.add_paragraph() for i in range(5)]
#
# create_column_names_ui(create_table_fmt(doc, 3, 8))
#
# # tbl.cell(1, 2).test = 'Это по центру?'
# # tbl.cell(1, 5).test = 'по?'
# # tbl.cell(1, 1).test = 'кк'
#
# print(type(doc))
#
# doc.save(f"my_check_of_5_paragraphs.docx")
# from datetime import datetime
#
#
# date = datetime.now()
#
# a = '12.03.2022'
# date_a = datetime.strftime(a, "%Y.%m.%d")
#
#
# print(type(date), datetime.strftime(a, "%Y.%m.%d"))

# from datetime import datetime
#
#
# "2018-01-31", "%Y-%m-%d"
#
# dateString = "2018.01.31"
# dateFormatter = "%Y.%m.%d"
# a = (datetime.strptime(dateString, dateFormatter))
# print(a)

import pandas as pd


print(pd._libs.tslibs.nattype.NaTType)