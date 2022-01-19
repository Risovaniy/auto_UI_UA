# # # -*- coding: utf-8 -*-
# #
# #### Copy GUI.py
#
# import os
#
# import PySimpleGUIQt as sg
# from configparser import ConfigParser
#
# import pathlib
#
# from bin.create_UI_and_UA import make_only_UI, make_UI_and_UA, make_only_UA
#
#
# MY_ICON = str(f"{pathlib.Path.cwd()}{os.sep}resources{os.sep}assist_icon.png")
#
#
# def my_popup(text='',
#              title='Main title',
#              custom_text=('Button Yes', 'Button No'),
#              icon=MY_ICON,
#              line_width=None,
#              font=('ANY', 16),  # , 'Bold'),
#              grab_anywhere=True,
#              keep_on_top=True,
#              location=None):
#     answer = sg.Popup(text,
#                       title=title,
#                       custom_text=custom_text,
#                       icon=icon,
#                       line_width=line_width,
#                       font=font,
#                       grab_anywhere=grab_anywhere,
#                       keep_on_top=keep_on_top,
#                       location=location)
#
#     return True if answer == custom_text[0] else False
#
#
# def popup_close(config,
#                 language,
#                 icon=MY_ICON,
#                 line_width=None,
#                 font=('ANY', 16),  # , 'Bold'),
#                 grab_anywhere=True,
#                 keep_on_top=True,
#                 location=None,
#                 ):
#     title = config.get(language, 'popup_close_title')
#
#     text = config.get(language, 'popup_close_text')
#
#     b_text_yes = config.get(language, 'popup_close_b_yes')
#     b_text_no = config.get(language, 'popup_close_b_no')
#     buttons_text = (b_text_yes, b_text_no)
#
#     return my_popup(text=text,
#                     title=title,
#                     custom_text=buttons_text,
#                     icon=icon,
#                     line_width=line_width,
#                     font=font,
#                     grab_anywhere=grab_anywhere,
#                     keep_on_top=keep_on_top,
#                     location=location)
#
#
# # New main window
# def create_main_layout(conf, language):
#     main_layout = [
#         [sg.Stretch(),
#          sg.Text(conf.get(language, 'm_welcome'), justification='center'),
#          sg.Stretch()],
#
#         [sg.Text()],
#
#         [sg.Button(conf.get(language, 'b_manual_work'),
#                    size_px=(230, 30),
#                    key='b_manual_work'),
#          sg.Stretch(),
#          sg.Stretch(),
#          sg.Button(conf.get(language, 'b_manual_table'),
#                    size_px=(230, 30),
#                    key='b_manual_table')],
#
#         [sg.Text()],
#         [sg.Text()],
#         [sg.Text(conf.get(language, 'l_please_input_path'))],
#
#         [sg.Text(conf.get(language, 'l_input_path')),
#          sg.InputText(default_text=str(pathlib.Path.home()), key='input_path'),
#          sg.FileBrowse(conf.get(language, 'b_file_browse'),
#                        size=(125, 30))],
#
#         [sg.Text()],
#         [sg.Text()],
#         [sg.Text(conf.get(language, 'l_please_output_path'))],
#
#         [sg.Text(conf.get(language, 'l_output_path')),
#          sg.InputText(default_text=str(pathlib.Path.home()), key='output_path'),
#          sg.FolderBrowse(conf.get(language, 'b_folder_browse'),
#                          size=(125, 30), pad=True)],
#
#         [sg.Text()],
#         [sg.Text()],
#         [sg.Text()],
#         [sg.Text()],
#
#         # Задать размеры кнопок (какие-то относительные выбрать)
#         [sg.Stretch(),
#          sg.Button(conf.get(language, 'b_create_UI'),
#                    key='b_create_UI',
#                    size_px=(200, 30)),
#          sg.Button(conf.get(language, 'b_create_UA'),
#                    key='b_create_UA',
#                    size_px=(200, 30)),
#          sg.Button(conf.get(language, 'b_create_UI_and_UA'),
#                    key='b_create_all',
#                    size_px=(200, 30)),
#          sg.Stretch()],
#
#         [sg.Text()],
#         [sg.Text()],
#
#         [sg.Stretch(), sg.Button(conf.get(language, 'b_close'),
#                                  key='b_close',
#                                  size_px=(100, 30))]
#     ]
#
#     return main_layout
#
#
# def create_main_window(config, language):
#     # Add a theme
#     sg.ChangeLookAndFeel(config.get('THEMES', "theme"))
#     # sg.SetOptions(window_location=(300, 250))
#     # Create the Window
#     window = sg.Window(
#         title=config.get(language, 'program_fullname'),
#         layout=create_main_layout(config, language),
#         icon=MY_ICON,
#         resizable=(350, 450)
#     )
#     return window
#
#
# def read_config_and_language():
#     # instantiate configs
#     config = ConfigParser()
#
#     # parse existing file (c - config)
#
#     config.read('resources/config.ini')
#
#     # read the language selected by the user (l - language)
#     language = (config.get('LOCALLY', "language")).upper()
#
#     return config, language
#
#
# def start_main_window():
#     # Preparations and settings for the main window of program
#
#     # Load configurations and language
#     config, language = read_config_and_language()
#
#     # Create the Window
#     # window = create_main_window(config, language)
#     window = sg.Window(
#         title=config.get(language, 'program_fullname'),
#         layout=create_main_layout(config, language),
#         icon=MY_ICON,
#         resizable=(350, 450))
#
#     print(window.close())
#     # Start my cycle for active interaction with the program interface
#     while True:
#         # Reading the current state of the interface
#         event, values = window.read()
#
#         # Determine which event was triggered and execute it
#
#         # ToDo Если открыто окно "Точно закрыть?" и закрыть прогру на крестик -
#         #  окно останется - но это бесмысленно
#
#         # If the "close program" button was pressed
#         if event in (sg.WIN_CLOSED, config.get(language, 'b_close')):
#             if popup_close(config, language):
#                 break
#             else:
#                 continue
#
#         # If the "create file(s)" button(s) was(re) pressed
#         elif event in (config.get(language, 'b_create_UI'),
#                        config.get(language, 'b_create_UA'),
#                        config.get(language, 'b_create_UI_and_UA')):
#             if create_files(MY_ICON, event, values, config, language):
#                 print('Successfully')
#             else:
#                 print('Line 191 have an error into fn on 188 line')
#
#         # If the "show the manual to program work" button was pressed
#         elif event == config.get(language, 'b_manual_work'):
#             show_manual_how_work_program(config, language)
#
#         # If the "show the manual to table with authors data" button was pressed
#         elif event == config.get(language, 'b_manual_table'):
#             show_manual_how_fill_authors_table(config, language)
#
#     # Exit from cycle and close the main window
#     window.close()
#     return window
#
#
# def close_program(event, config, language, icon):
#     # If the "close program" button was pressed
#     # ToDo Если открыто окно "Точно закрыть?" и закрыть прогру на крестик -
#     #  окно останется - но это бесмысленно
#     if event in (sg.WIN_CLOSED, config.get(language, 'b_close')):
#         # if user closes window or clicks cancel
#         if event == config.get(language, 'b_close') and \
#                 are_you_sure(config, language):
#             return True
#
#
# def are_you_sure(config, language, path_files, path_authors_data):
#     title = config.get(language, 'popup_create_title')
#
#     text = config.get(language, 'popup_create_text')
#     # ToDo: Check when i have two files: in 1 line or split for 2 lines?
#     text = text.replace('$create_files$', str(path_files))
#     text = text.replace('$authors_table$', str(path_authors_data))
#
#     button_1_text = config.get(language, 'popup_create_b_yes')
#     button_2_text = config.get(language, 'popup_create_b_no')
#     buttons_text = (button_1_text, button_2_text)
#
#     return my_popup(text=text,
#                     title=title,
#                     custom_text=buttons_text
#                     )
#
#
# def create_files(event, values, config, language):
#     path_input_data = values['input_path']
#     path_output_dir = values['output_path']
#
#     if event == (config.get(language, 'b_create_UI')) and \
#             are_you_sure(config,
#                          language,
#                          config.get(language, 'b_create_UI'),
#                          path_input_data):
#         make_only_UI(path_input_data, path_output_dir)
#
#
#     elif event == (config.get(language, 'b_create_UA')) and \
#             are_you_sure(config,
#                          language,
#                          config.get(language, 'b_create_UA'),
#                          path_input_data):
#         make_only_UA(path_input_data, path_output_dir)
#
#     elif event == (config.get(language, 'b_create_UI_and_UA')) and \
#             are_you_sure(config,
#                          language,
#                          config.get(language, 'b_create_UI_and_UA'),
#                          path_input_data):
#         make_UI_and_UA(path_input_data, path_output_dir)
#
#     else:
#         return False
#
#     return True
#
#
# def show_manual_how_work_program(config, language):
#     # If the "show the manual to program work" button was pressed
#     # if event == config.get(language, 'b_manual_work'):
#     message = config.get(language, 'manual_work')
#     return sg.popup_ok(message,
#                        icon=MY_ICON,
#                        keep_on_top=True,
#                        grab_anywhere=True)
#
#
# def show_manual_how_fill_authors_table(config, language):
#     # If the "show the manual to table with authors data" button was pressed
#     # if event == config.get(language, 'b_manual_table'):
#     message = config.get(language, 'manual_table')
#     return sg.popup_ok(message,
#                        icon=MY_ICON,
#                        keep_on_top=True,
#                        grab_anywhere=True)
#
#
# def testing():
#     config, language = read_config_and_language()
#
#     window = sg.Window(
#         title=config.get(language, 'program_fullname'),
#         layout=create_main_layout(config, language),
#         icon=MY_ICON,
#         resizable=(350, 450))
#     # layout = [[sg.Text()],
#     #           [sg.Text()],
#     #
#     #           [sg.Stretch(), sg.Button('b_close',
#     #                                    key='b_close',
#     #                                    size_px=(100, 30))]
#     #           ]
#     # window = sg.Window('Test window', layout)
#
#     while True:
#         event, values = window.read()
#         print(event, values)
#     # show(window)
#     window.close()
#     return window
#
#
# if __name__ == "__main__":
#     # start_main_window()
#     testing()
#
# #### Copy GUIqnfig.get(language, 'b_create_UI'),
#         #                config.get(language, 'b_create_UA'),
#         #                config.get(language, 'b_create_UI_and_UA')):
#         #     if create_files(GLOBAL_ICON, event, values, config, language):
#         #         print('Successfully')
#         #     else:
#         #         print('Lt5.py
#
#
# import sys
#
# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QApplication, QMainWindow
#
#
# class Window(QMainWindow):
#     def __init__(self):
#         super(Window, self).__init__()
#
#         self.setGeometry(300, 200, 500, 400)
#         self.setWindowTitle('My window title')
#         self.main_label = QtWidgets.QLabel(self)
#         self.main_label.setText(
#             'Это просто длинный текст: алодвыафвыарвыфравфавыфафвыафравфырдарыфварвыфрдавыдфадрыфоавыфлавыфадфвыдрафвырдафрыфварфвы')
#
#         self.new_text = QtWidgets.QLabel(self)
#
#         # Подстроить ширину объекта под его содержимое!!!
#         self.main_label.adjustSize()
#
#         self.main_label.move(100, 300)
#
#         # Added simple button
#         self.main_btn = QtWidgets.QPushButton(self)
#         self.main_btn.setText('Push me!!!')
#         self.main_btn.setFixedWidth(700)
#         self.main_btn.move(10, 30)
#         self.main_btn.clicked.connect(self.add_label)
#
#     def add_label(self):
#         print('add')
#         self.new_text.setText('Second text')
#
#
#
#
# def application():
#     # Set parameters of current PC
#     app = QApplication(sys.argv)
#
#     # Create the main window
#     window = Window()
#
#     # Different settings of the main window
#
#
#     # Show our window
#     window.show()
#
#     # To display the window correctly
#     sys.exit(app.exec_())
#
#
# if __name__=='__main__':
#     application()
#
#
#
#
#
# #
# #
# #
# # # Qt5
# #
# #
# # import sys
# # from configparser import ConfigParser
# #
# # from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, \
# #     QGridLayout, QLCDNumber
# # from PyQt5.QtGui import QIcon, QFont
# #
# # # from bin.GUI import read_config_and_language
# #
# # # ToDo: Rename and move icon
# # MY_ICON = "TRASH_assist_icon.png"
# #
# #
# #
# #
# # def create_main_window(title='Title', left=None, top=None, width=None, height=None):
# #     if not left:
# #         # Getting the parameters of the active monitor
# #         desktop_width = QApplication.desktop().availableGeometry().width() #QApplication.desktop().width()
# #         desktop_height = QApplication.desktop().availableGeometry().height() #QApplication.desktop().height()
# #
# #         # Set parameters of window
# #         width = desktop_height * 0.5
# #         height = desktop_height * 0.5
# #         left = desktop_width * 0.25
# #         top = desktop_height * 0.25
# #
# #     window = QMainWindow()
# #     window.setGeometry(left, top, width, height)
# #     window.setWindowTitle(title)
# #     window.setWindowIcon(QIcon(MY_ICON))
# #
# #     return window
# #
# #
# # # ToDo: Remove this fn or edit - this is local copy from GUI
# # def read_config_and_language():
# #     # instantiate configs
# #     config = ConfigParser()
# #
# #     # parse existing file (c - config)
# #
# #     config.read('../resources/config.ini')
# #
# #     # read the language selected by the user (l - language)
# #     language = (config.get('LOCALLY', "language")).upper()
# #
# #     return config, language
# #
# #
# # def create_main_label(window):
# #     label = QLabel(window)
# #
# #     window_width = window.size().width()
# #     window_height = window.size().height()
# #
# #     config, language = read_config_and_language()
# #
# #     text = config.get(language, 'm_welcome')
# #
# #     label.setMinimumWidth(window_width*0.9)
# #     label.setText(text)
# #     label.setFont(QFont('System', 22, QFont.Bold))
# #
# #     label.move(0.015*window_height, 0.015*window_width)
# #     return label
# #
# #
# # def main():
# #     app = QApplication(sys.argv)
# #
# #     win = create_main_window()
# #
# #     numbers = QLCDNumber()
# #
# #     win.setCentralWidget(QWidget())
# #     QGridLayout(win).addWidget(numbers)
# #     # win.
# #
# #
# #     # Label Text
# #     create_main_label(win)
# #     # label.setText("Hi this is Pyqt5")
# #     # label.move(100,100)
# #
# #     win.show()
# #     sys.exit(app.exec_())
# #
# #
# #
# #
# # # class App(QWidget):
# # #
# # #     def __init__(self, title='Title', left=10, top=10, width=300, height=250):
# # #         super().__init__()
# # #         self.textbox = QLineEdit(self)
# # #         self.title = title
# # #         self.left = left
# # #         self.top = top
# # #         self.width = width
# # #         self.height = height
# # #         self.icon = MY_ICON
# # #         self.initUI()
# # #
# # #     def initUI(self):
# # #         self.setWindowTitle(self.title)
# # #         self.setGeometry(self.left, self.top, self.width, self.height)
# # #         self.setWindowIcon(QIcon(self.icon))
# # #         self.show()
# # #
# # #     def add_lable(self, text):
# # #         self.textbox.move(20, 20)
# # #         self.textbox.resize(280, 40)
# #
# #
# # if __name__ == '__main__':
# #     # app = QApplication(sys.argv)
# #     # ex = App()
# #     # sys.exit(app.exec_())
# #
# #     main()
# #
# # import sys
# # from PySide6.QtWidgets import QApplication, QLabel
# #
# # app = QApplication(sys.argv)
# # label = QLabel("Hello World!")
# # label.show()
# # app.exec()
import pandas
import PySimpleGUIQt as sg

a = window = sg.Window(title='test',
        location=(300, 200),
        # resizable=False,
        grab_anywhere=True,
        # size=(1000, 600)
    )

print(type(a))

