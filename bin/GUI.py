# -*- coding: utf-8 -*-

import os
import pathlib as path
import sys
import traceback
from configparser import ConfigParser
import PySimpleGUIQt as sg
from bin.create_UI_UA import make_only_UI, make_only_UA, make_UI_and_UA, CONFIG, \
    LANGUAGE

# Location of my global icon
GLOBAL_ICON = str(f"{path.Path.cwd()}{os.sep}resources{os.sep}global_icon.png")


def popup_Yes_No(text='Just text',
                 title='Main title',
                 buttons_text=('Button Yes', 'Button No'),
                 buttons_size=(70, 40),
                 icon=GLOBAL_ICON,
                 font=('Arial', 16),
                 grab_anywhere=False,
                 keep_on_top=True,
                 location=(600, 400)
                 ):
    """Displays a confirmation pop-up window, the names of the buttons can be changed

    :param text: Clarifying text - "Are you sure?"
    :type text: str
    :param title: Title of the popup window
    :type title: str
    :param buttons_text: A tuple of button names, the first button returns True
    :type buttons_text: tuple
    :param buttons_size: Tuple of button sizes in pixels (width, height)
    :type buttons_size: tuple
    :param icon: The path to the popup icon
    :type icon: str
    :param font: A tuple with the characteristics of the text (size, outline, etc.)
    :type font: tuple
    :param grab_anywhere: Is it possible to move the window with a grip anywhere
    :type grab_anywhere: bool
    :param keep_on_top: Whether to support a window from above
    :type keep_on_top: bool
    :param location: Coordinates of the window appearance (centered if 1 screen)
    :type location: tuple
    :return: Confirmation or Rejection (True or False)
    :rtype: bool

    """
    # Add a theme
    sg.ChangeLookAndFeel(CONFIG.get('THEMES', "-theme_popup-"))

    # Create the layout for popup
    layout = [
        [sg.Stretch(),
         sg.Text(text, font=font),
         sg.Stretch()
         ],

        [sg.Text(size=(1, 20))],

        [sg.Stretch(),
         sg.Button(button_text=buttons_text[0],
                   size=buttons_size,
                   font=font,
                   ),
         sg.Button(button_text=buttons_text[1],
                   size=buttons_size,
                   font=font
                   )
         ]
        ]

    # Create the popup
    window_Yes_No = sg.Window(title=title,
                              layout=layout,
                              icon=icon,
                              location=location,
                              resizable=False,
                              grab_anywhere=grab_anywhere,
                              keep_on_top=keep_on_top,
                              )

    # Show and read the popup
    event, values = window_Yes_No.Show()

    # Close the popup
    window_Yes_No.Close()

    return True if event == buttons_text[0] else False


def popup_Ok(text='',
             title='Main title',
             buttons_text='Ok',
             buttons_size=(150, 40),
             icon=GLOBAL_ICON,
             font=('Arial', 16),
             grab_anywhere=False,
             keep_on_top=True,
             location=(600, 400)
             ):
    """Displays a confirmation pop-up window, with a changeable button name

    :param text: Clarifying text - "Are you sure?"
    :type text: str
    :param title: Title of the popup window
    :type title: str
    :param buttons_text: The name of the button, usually "close"
    :type buttons_text: str
    :param buttons_size: Tuple of button sizes in pixels (width, height)
    :type buttons_size: tuple
    :param icon: The path to the popup icon
    :type icon: str
    :param font: A tuple with the characteristics of the text (size, outline, etc.)
    :type font: tuple
    :param grab_anywhere: Is it possible to move the window with a grip anywhere
    :type grab_anywhere: bool
    :param keep_on_top: Whether to support a window from above
    :type keep_on_top: bool
    :param location: Coordinates of the window appearance (centered if 1 screen)
    :type location: tuple
    :return: The window is informational, it can only be closed
    :rtype: None

    """
    # Add a theme
    sg.ChangeLookAndFeel(CONFIG.get('THEMES', "-theme_popup-"))

    # Create the layout for popup
    layout = [
        [sg.Stretch(),
         sg.Text(text, font=font),
         sg.Stretch()
         ],

        [sg.Text(size=(1, 20))],

        [sg.Stretch(),
         sg.Button(button_text=buttons_text,
                   size=buttons_size,
                   font=font,
                   )
         ]
        ]

    # Create the popup
    window_Ok = sg.Window(
            title=title,
            layout=layout,
            icon=icon,
            location=location,
            resizable=False,
            grab_anywhere=grab_anywhere,
            keep_on_top=keep_on_top,
            )

    # Show the popup
    window_Ok.Show()

    # Close the popup
    window_Ok.Close()

    return None


def popup_close(buttons_size=(70, 40),
                icon=GLOBAL_ICON,
                font=('Arial', 16),
                grab_anywhere=True,
                keep_on_top=True,
                location=(600, 400),
                ):
    """Displays a pop-up window confirming the intention to close the program

    :param buttons_size: Tuple of button sizes in pixels (width, height)
    :type buttons_size: tuple
    :param icon: The path to the popup icon
    :type icon: str
    :param font: A tuple with the characteristics of the text (size, outline, etc.)
    :type font: tuple
    :param grab_anywhere: Is it possible to move the window with a grip anywhere
    :type grab_anywhere: bool
    :param keep_on_top: Whether to support a window from above
    :type keep_on_top: bool
    :param location: Coordinates of the window appearance (centered if 1 screen)
    :type location: tuple
    :return: Logical value to close or not the program
    :rtype: bool

    """
    title = CONFIG.get(LANGUAGE, '-n_pop_close-')

    text = CONFIG.get(LANGUAGE, '-t_pop_close-')

    b_text_yes = CONFIG.get(LANGUAGE, '-b_yes-')
    b_text_no = CONFIG.get(LANGUAGE, '-b_no-')

    return popup_Yes_No(text=text,
                        title=title,
                        buttons_text=(b_text_yes, b_text_no),
                        buttons_size=buttons_size,
                        icon=icon,
                        font=font,
                        grab_anywhere=grab_anywhere,
                        keep_on_top=keep_on_top,
                        location=location
                        )


def popup_long_text(text='',
                    title='Main title',
                    button_text='Ok',
                    button_size=(150, 40),
                    icon=GLOBAL_ICON,
                    font=('Arial', 16),
                    grab_anywhere=True,
                    keep_on_top=True,
                    location=(600, 400)
                    ):
    """Display a popup for a long text (browser text)

    :param text: The long text for showing
    :type text: str
    :param title: Title of the popup window
    :type title: str
    :param button_text: The name of the button, usually "close"
    :type button_text: str
    :param button_size: Tuple of button sizes in pixels (width, height)
    :type button_size: tuple
    :param icon: The path to the popup icon
    :type icon: str
    :param font: A tuple with the characteristics of the text (size, outline, etc.)
    :type font: tuple
    :param grab_anywhere: Is it possible to move the window with a grip anywhere
    :type grab_anywhere: bool
    :param keep_on_top: Whether to support a window from above
    :type keep_on_top: bool
    :param location: Coordinates of the window appearance (centered if 1 screen)
    :type location: tuple
    :return: The window is informational (often manuals), it can only be closed
    :rtype: None

    """
    # Add a theme
    sg.ChangeLookAndFeel(CONFIG.get('THEMES', "-theme_popup-"))

    # Create the layout for popup
    layout = [
        [sg.Multiline(default_text=text,
                      font=font,
                      background_color='white',
                      change_submits=True,
                      enable_events=True,
                      )],

        [sg.Text(size=(600, 20))],

        [sg.Stretch(),
         sg.Button(button_text=button_text,
                   # auto_size_button=True ,
                   size=button_size,
                   font=font
                   )
         ]]

    # Create the popup
    window = sg.Window(
            title=title,
            layout=layout,
            icon=icon,
            location=location,
            resizable=True,
            grab_anywhere=grab_anywhere,
            keep_on_top=keep_on_top,
            size=(600, 400),
            )

    # Show the popup
    window.Show()

    # Close the popup
    window.Close()

    return None


def show_manual_work_program():
    """Show a popup with a guide to working in the program
    (without blocking the main window)

    :param icon: The path to the popup icon
    :type icon: str
    :return: The window with the manual can only be closed
    :rtype: None

    """
    message = CONFIG.get(LANGUAGE, '-t_manual_prog-')
    title = CONFIG.get(LANGUAGE, '-n_manual_prog-')
    button_text = CONFIG.get(LANGUAGE, '-b_close-')
    icon = GLOBAL_ICON

    return popup_long_text(text=message,
                           title=title,
                           button_text=button_text,
                           # location=(100, 60),
                           icon=icon,
                           )


def show_manual_input_data():
    """Show a popup with a guide to filling out a table with data about authors
    (without blocking the main window)

    :param icon: The path to the popup icon
    :type icon: str
    :return: The window with the manual can only be closed
    :rtype: None

    """
    message = CONFIG.get(LANGUAGE, '-t_manual_data-')
    title = CONFIG.get(LANGUAGE, '-n_manual_data-')
    button_text = CONFIG.get(LANGUAGE, '-b_close-')
    icon = GLOBAL_ICON

    return popup_long_text(text=message,
                           title=title,
                           button_text=button_text,
                           # location=(100, 110),
                           icon=icon
                           )


def popup_error(error_raport, icon=GLOBAL_ICON):
    """Show a popup signaling that an error has occurred during the execution
    of the program, and calling for a restart

    :param error_raport: Ready error report to display on the screen in popup
    :type error_raport: str
    :param icon: The path to the popup icon
    :type icon: str
    :return: Popup with error report, popup can only be closed
    :rtype: None

    """
    title = CONFIG.get(LANGUAGE, '-n_popup_error-')
    buttons_text = CONFIG.get(LANGUAGE, '-b_close-')

    return popup_Ok(text=error_raport,
                    title=title,
                    buttons_text=buttons_text,
                    icon=icon
                    )


def popup_success(buttons_size=(70, 40),
                  grab_anywhere=True,
                  ):
    """Show a window signaling the successful completion of the program

    :param buttons_size: Tuple of button sizes in pixels (width, height)
    :type buttons_size: tuple
    :param icon: The path to the popup icon
    :type icon: str
    :param font: A tuple with the characteristics of the text (size, outline, etc.)
    :type font: tuple
    :param grab_anywhere: Is it possible to move the window with a grip anywhere
    :type grab_anywhere: bool
    :param keep_on_top: Whether to support a window from above
    :type keep_on_top: bool
    :param location: Coordinates of the window appearance (centered if 1 screen)
    :type location: tuple
    :return: Logical value to close or not the program
    :rtype: bool

    """
    title = CONFIG.get(LANGUAGE, '-n_pop_close-')

    text = CONFIG.get(LANGUAGE, '-t_successful-')

    b_text_yes = CONFIG.get(LANGUAGE, '-b_yes-')
    b_text_no = CONFIG.get(LANGUAGE, '-b_no-')

    return popup_Yes_No(text=text,
                        title=title,
                        buttons_text=(b_text_yes, b_text_no),
                        buttons_size=buttons_size,
                        grab_anywhere=grab_anywhere,
                        )


def create_main_layout():
    """Assembling all the elements of the main window

    :return: A list with all the elements of the interface (with a clear order)
    :rtype: list

    """
    main_layout = [
        # Welcome message
        [sg.Stretch(),
         sg.Text(CONFIG.get(LANGUAGE, '-t_welcome_prog-'),
                 justification='center',
                 auto_size_text=True,
                 font=('Arial', 16)
                 ),
         sg.Stretch(),
         ],

        # Buttons for manuals
        [sg.Button(CONFIG.get(LANGUAGE, '-b_manual_prog-'),
                   size_px=(400, 40),
                   key='-b_manual_prog-',
                   font=('Arial', 14),
                   # auto_size_button=True
                   ),
         sg.Stretch(),
         sg.Stretch(),
         sg.Button(CONFIG.get(LANGUAGE, '-b_manual_data-'),
                   size_px=(400, 40),
                   key='-b_manual_data-',
                   font=('Arial', 14),
                   # auto_size_button=True
                   )
         ],

        # Horizontal separator
        [sg.HorizontalSeparator()],

        # Input data
        [sg.Text(size=(1, 20))],
        [sg.Text(CONFIG.get(LANGUAGE, '-t_welcome_data-'),
                 font=('Arial', 12),
                 )
         ],

        [sg.Text(CONFIG.get(LANGUAGE, '-t_data-'),
                 font=('Arial', 12),
                 ),
         sg.InputText(default_text=str(path.Path.home()),
                      key='-input_path-',
                      font=('Arial', 12),
                      ),
         sg.FileBrowse(CONFIG.get(LANGUAGE, '-b_data-'),
                       key='-b_browse_file-',
                       size=(150, 40),
                       font=('Arial', 12),
                       )

         ],

        # Spaces
        [sg.Text(size=(1, 20))],

        # Dir for saving
        [sg.Text(CONFIG.get(LANGUAGE, '-t_welcome_dir-'),
                 font=('Arial', 12),
                 )
         ],

        [sg.Text(CONFIG.get(LANGUAGE, '-t_dir-'),
                 font=('Arial', 12),
                 ),
         sg.InputText(default_text=str(path.Path.home()),
                      key='-output_path-',
                      font=('Arial', 12),
                      ),
         sg.FolderBrowse(CONFIG.get(LANGUAGE, '-b_dir-'),
                         key='-b_browse_dir-',
                         initial_folder=str(path.Path.home()),
                         size=(150, 40),
                         font=('Arial', 12),
                         ),
         ],

        # Spaces
        [sg.Text(size=(1, 50))],

        # Create buttons
        [sg.Button(CONFIG.get(LANGUAGE, '-b_create_UI-'),
                   key='-b_create_UI-',
                   font=('Arial', 12),
                   size_px=(300, 40)
                   ),
         sg.Button(CONFIG.get(LANGUAGE, '-b_create_UA-'),
                   key='-b_create_UA-',
                   font=('Arial', 12),
                   size_px=(300, 40)
                   ),
         sg.Button(CONFIG.get(LANGUAGE, '-b_create_UI_and_UA-'),
                   key='-b_create_UI_and_UA-',
                   font=('Arial', 12),
                   size_px=(300, 40)
                   ),
         ],

        # Spaces
        [sg.Text(size=(1, 50))],

        # Close button
        [sg.Stretch(),
         sg.Button(CONFIG.get(LANGUAGE, '-b_close-'),
                   key='-b_close-',
                   size_px=(120, 40),
                   font=('Arial', 12),
                   )
         ],
        ]

    return main_layout


def create_main_window():
    """Creating the main window of the program, styles and localization are
    immediately applied

    :return: The main window of the program is ready for interaction
    :rtype: PySimpleGUIQt.PySimpleGUIQt.Window

    """
    # Add a theme
    sg.ChangeLookAndFeel(CONFIG.get('THEMES', "-theme_global-"))

    # sg.SetOptions(window_location=(300, 250))
    # Create the Window
    window = sg.Window(
            title=CONFIG.get(LANGUAGE, '-n_main_window-'),
            layout=create_main_layout(),
            icon=GLOBAL_ICON,
            location=(300, 200),
            # resizable=False,
            grab_anywhere=True,
            # size=(1000, 600)
            )

    return window


def launch_main_window():
    """Launch and operation of the main working window of the program

    :return: Interaction with the interface takes place inside the function
    :rtype: None

    """
    # It is necessary that the first click is processed and not passed into empty
    start = True
    # Preparations and settings for the main window of program

    # Create the main window
    window = create_main_window()

    # Start my cycle for active interaction with the program interface
    while True:
        if start:
            # Show interface and reading the first user action
            event, values = window.Show()
            # The main window is running, now this part of the code is skipped
            start = False
        else:
            # Reading user actions
            event, values = window.read()

        # ToDo: Remove it (it's temporary, for debugs)
        print('\n', event, values)

        # Determine which event was triggered and execute it

        # If the "close program" button was pressed
        if event in (sg.WIN_CLOSED, '-b_close-'):
            # Blocking the main window until a response is received from popup
            window.Disable()

            if event == sg.WIN_CLOSED:
                break
            elif popup_close():
                break
            else:
                # Unlocking the main window, ready to accept new commands
                window.Enable()
                continue

        # If the "create file(s)" button(s) was(re) pressed
        elif event in (
                '-b_create_UI-', '-b_create_UA-', '-b_create_UI_and_UA-'):
            # Blocking the main window until a response is received from popup
            window.Disable()

            # Fill the input path with the home directory if the field is empty
            if values['-input_path-'] == '':
                values['-input_path-'] = str(path.Path.home())

            # Fill the output path with the home directory if the field is empty
            if values['-output_path-'] == '':
                values['-output_path-'] = str(path.Path.home())

            error = create_files_fault_tolerant(event=event, values=values)

            # Refusal to create documents
            if error is False:
                window.Enable()
                continue

            elif error is True:
                if popup_success():
                    break

            else:
                popup_error(error_raport=error)
                print(f'Some error: \nEvent {event} \nValues {values}')

            # Unlocking the main window, ready to accept new commands
            window.Enable()

        # If the "show the manual to program work" button was pressed
        elif event == '-b_manual_prog-':
            show_manual_work_program()

        # If the "show the manual to table with authors data" button was pressed
        elif event == '-b_manual_data-':
            show_manual_input_data()

    # Exit from cycle and close the main window
    window.close()

    return None


def make_question_for_sure(config_key, path_data, path_dir):
    """Assembling the text to clarify the creation of a document with the
    selected parameters

    :param config_key: The key that will get the desired text from the config
    :type config_key: str
    :param path_dir: Absolute path to the file with data about authors
    :type path_dir: str
    :param path_data: Absolute path to the directory for save creating files
    :type path_data: str
    :return: Clarifying question to the user with the settings selected by him
    :rtype: str

    """
    # Transformation of the key to get the text of the question, not the buttons
    config_key = config_key.replace('-b_create_', '-t_sure_')

    # Add contextual data of the current session of the program to the question
    question = CONFIG.get(LANGUAGE, config_key). \
        replace('$input_path$', path_data). \
        replace('$output_path$', path_dir)

    return question


def error_processing_col_names(err):
    """Preparing ErrorKey and return the message with info for fix it

    :param err: Full error information for deployment via .args
    :type err: BaseException
    :return: Information about the error and how to fix it
    :rtype: str

    """
    dict_for_translate = {'last_name': 'Фамилия',
                          'first_name': 'Имя',
                          'middle_name': 'Отчество',
                          'post': 'Должность',
                          'academic': 'Ученое звание',
                          'job': 'Место работы',
                          'contribution': 'Творческий вклад',
                          'contract': 'Контракт/Договор',
                          'date_UA': 'Дата подписания УА',
                          'date_employ': 'Дата трудоустройства'}
    # Remove "'", else we have keys like "'job'"
    err = str(err.args[0][1])[1:-1]

    # Error handling of column names in source data
    if err in dict_for_translate:
        message = CONFIG.get(LANGUAGE, '-t_error_ErrorKey-'). \
            replace('$ErrorKey$', dict_for_translate[err])
        return message

    # In case the KeyError got out not from the column names
    else:
        type_err = str(err.args[0][0])
        object_id = err.args[0][2]
        message = CONFIG.get(LANGUAGE, '-t_error-'). \
            replace('$TypeError$', str(type_err)). \
            replace('$Error$', str(err))
        return message


def error_processing():
    """Error handling of any type and formation of correction information

    :return: Error report text to output to popup
    :rtype: str

    """
    type_err = sys.exc_info()[0]
    err = sys.exc_info()[1]
    object_id = sys.exc_info()[2]

    print(f'\tsys.exc_info()\t\t{sys.exc_info()}\n'
          f'\t\ttype_err\t\t{type_err}\n'
          f'\t\terr\t\t{err}\n'
          f'\t\tobject_id\t\t{object_id}\n'
          # f'\t\tsys.last_traceback\t\t{sys.last_traceback()}\n'
          f'\t\t2sys.last_traceback\t\t{traceback.print_tb(object_id)}\n\n')

    if type_err == KeyError:
        return error_processing_col_names(err)

    elif type_err == Exception:
        # print(f'type_err\t{type_err}\nerr\t{err}\nsys.exc_info()\t{sys.exc_info()}')
        type_err = err.args[0][0]

        if type_err == 'FormatError':
            return CONFIG.get(LANGUAGE, '-t_error_FormatError-')

        elif type_err == 'ExtensionError':
            return CONFIG.get(LANGUAGE, '-t_error_ExtensionError-')

        elif type_err == 'FileNotFoundError':
            return CONFIG.get(LANGUAGE, '-t_error_FileNotFoundError-')

    else:
        message = CONFIG.get(LANGUAGE, '-t_error-'). \
            replace('$TypeError$', str(type_err)). \
            replace('$Error$', str(err)). \
            replace('$ObjectID$', str(object_id))
        return message


def create_files_fault_tolerant(event, values):
    """Processing the pressed button and calling the corresponding function
    for creating documents

    :param event: The key of the current event in the GUI (button key)
    :type event: str
    :param values: Dictionary with current interface parameters
    :type values: dict
    :return: Error report text to output to popup, or True - success,
             or False - refusal,
    :rtype: str

    """
    # Catching errors when generating files (the basis is incorrect source data)
    try:
        result = create_files(event, values)
        return result

    except:
        return error_processing()


def create_files(event, values):
    """Processing the pressed button and calling the corresponding function
    for creating documents

    :param event: The key of the current event in the GUI (button key)
    :type event: str
    :param values: Dictionary with current interface parameters
    :type values: dict
    :return: The function creates files: True - if successful, False - if you
            decide not to create. Errors are called in functions separately
    :rtype: bool

    """
    path_input_data = values['-input_path-']
    path_output_dir = values['-output_path-']
    question = make_question_for_sure(config_key=event,
                                      path_data=path_input_data,
                                      path_dir=path_output_dir,
                                      )

    # The key that informs about the success of the function
    if popup_Yes_No(text=question,
                    title=CONFIG.get(LANGUAGE,
                                     str(event).replace('-b_create_', '-n_sure_')
                                     ),
                    buttons_text=(CONFIG.get(LANGUAGE, '-b_yes-'),
                                  CONFIG.get(LANGUAGE, '-b_no-')),
                    ):
        if event == '-b_create_UI-':
            make_only_UI(path_input_data, path_output_dir)

        elif event == '-b_create_UA-':
            make_only_UA(path_input_data, path_output_dir)

        elif event == '-b_create_UI_and_UA-':
            make_UI_and_UA(path_input_data, path_output_dir)

        return True

    return False


def check_exit_from_def(window):
    window.close()
