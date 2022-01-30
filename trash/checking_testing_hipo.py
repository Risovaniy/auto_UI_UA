# import os
#
# import docx
# from docx.shared import Inches
#
#
# def find_table_in_ui_template(doc):
#     for table in doc.tables:
#         if table.cell(0, 0).text == 'п/п':
#             return table
#
#
# def open_docx_file(path):
#     return docx.Document(path)
#
#     # return doc
#
#
# if __name__ == '__main__':
#     doc = open_docx_file(r'C:\Users\Risov\Desktop\Prog\auto_ui_ua\auto_UI_UA\resources\UI_template.docx')
#
#     ui_table = find_table_in_ui_template(doc)
#
#     ui_table.add_row()
#     ui_table.add_row()
#     ui_table.add_row()
#     ui_table.add_row()
#     ui_table.add_row()
#
#     ui_table.style = 'table_ui' #ui_table._TableStyle('table_ui')
#     ui_table.style = 'table_ui_title' #ui_table._TableStyle('table_ui')
#
#     doc.save(f"{os.sep}test_ui_table.docx")


if __name__ == '__main__':









