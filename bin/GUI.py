# -*- coding: utf-8 -*-

import os
import pathlib as path
from configparser import ConfigParser
import PySimpleGUIQt as sg
from bin.create_UI_UA import make_only_UI, make_only_UA, make_UI_and_UA

# Location of my global icon
GLOBAL_ICON = str(f"{path.Path.cwd()}{os.sep}resources{os.sep}global_icon.png")


def read_config_and_language():
    """Read the file with the localization block configs
    (all text fields are written there)

    :return: An object with configs according to the set locale
    :rtype: tuple

    """
    # instantiate configs
    config = ConfigParser()

    # parse existing file (c - config)

    config.read('./resources/config.ini')

    # read the language selected by the user (l - language)
    language = (config.get('LOCALLY', "-language-")).upper()

    return config, language


def popup_Yes_No(config,
                 text='Just text',
                 title='Main title',
                 buttons_text=('Button Yes', 'Button No'),
                 buttons_size=(70, 40),
                 icon=GLOBAL_ICON,
                 font=('Arial', 14),
                 grab_anywhere=True,
                 keep_on_top=True,
                 location=(600, 400)
                 ):
    """Displays a confirmation pop-up window, the names of the buttons can be changed

    :param config: A file with configs for the current localization
    :type config: configparser.ConfigParser
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
    sg.ChangeLookAndFeel(config.get('THEMES', "-theme_popup-"))

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
                   font=font
                   ),
         sg.Button(button_text=buttons_text[1],
                   size=buttons_size,
                   font=font
                   )
         ]
        ]

    # Create the popup
    window = sg.Window(
            title=title,
            layout=layout,
            icon=icon,
            location=location,
            resizable=False,
            grab_anywhere=grab_anywhere,
            keep_on_top=keep_on_top,
            )


    # Show and read the popup
    event, values = window.Show()

    # Close the popup
    window.Close()

    return True if event == buttons_text[0] else False


def popup_Ok(config,
             text='',
             title='Main title',
             buttons_text='Ok',
             buttons_size=(150, 40),
             icon=GLOBAL_ICON,
             font=('Arial', 14),
             grab_anywhere=True,
             keep_on_top=True,
             location=(600, 400)
             ):
    """Displays a confirmation pop-up window, with a changeable button name

    :param config: A file with configs for the current localization
    :type config: configparser.ConfigParser
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
    sg.ChangeLookAndFeel(config.get('THEMES', "-theme_popup-"))

    # Create the layout for popup
    layout = [
        [sg.Stretch(),
         sg.Text(text, font=font),
         sg.Stretch()
         ],

        [sg.Text(size=(1, 20))],

        [sg.Stretch(),
         sg.Button(button_text=buttons_text,
                   # auto_size_button=True ,
                   size=buttons_size,
                   font=font
                   )
         ]
        ]

    # Create the popup
    window = sg.Window(
            title=title,
            layout=layout,
            icon=icon,
            location=location,
            resizable=False,
            grab_anywhere=grab_anywhere,
            keep_on_top=keep_on_top,
            )

    # Show and read the popup
    window.Show()

    # Close the popup
    window.Close()

    return None


def popup_close(config,
                language,
                buttons_size=(70, 40),
                icon=GLOBAL_ICON,
                font=('Arial', 18),
                grab_anywhere=True,
                keep_on_top=True,
                location=(600, 400),
                ):
    """Displays a pop-up window confirming the intention to close the program

    :param config: A file with configs for the current localization
    :type config: configparser.ConfigParser
    :param language: The current localization
    :type language: str
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
    title = config.get(language, '-n_pop_close-')

    text = config.get(language, '-t_pop_close-')

    b_text_yes = config.get(language, '-b_yes-')
    b_text_no = config.get(language, '-b_no-')

    return popup_Yes_No(config=config,
                        text=text,
                        title=title,
                        buttons_text=(b_text_yes, b_text_no),
                        buttons_size=buttons_size,
                        icon=icon,
                        font=font,
                        grab_anywhere=grab_anywhere,
                        keep_on_top=keep_on_top,
                        location=location
                        )


def show_manual_work_program(config, language, icon=GLOBAL_ICON):
    """Show a popup with a guide to working in the program
    (without blocking the main window)

    :param config: A file with configs for the current localization
    :type config: configparser.ConfigParser
    :param language: The current localization
    :type language: str
    :param icon: The path to the popup icon
    :type icon: str
    :return: The window with the manual can only be closed
    :rtype: None

    """
    message = config.get(language, '-t_manual_prog-')
    title = config.get(language, '-n_manual_prog-')
    buttons_text = config.get(language, '-b_close-')

    return popup_Ok(config=config,
                    text=message,
                    title=title,
                    buttons_text=buttons_text,
                    location=(100, 60),
                    icon=icon
                    )


def show_manual_input_data(config, language, icon=GLOBAL_ICON):
    """Show a popup with a guide to filling out a table with data about authors
    (without blocking the main window)

    :param config: A file with configs for the current localization
    :type config: configparser.ConfigParser
    :param language: The current localization
    :type language: str
    :param icon: The path to the popup icon
    :type icon: str
    :return: The window with the manual can only be closed
    :rtype: None

    """
    message = config.get(language, '-t_manual_data-')
    title = config.get(language, '-n_manual_data-')
    buttons_text = config.get(language, '-b_close-')

    return popup_Ok(config=config,
                    text=message,
                    title=title,
                    buttons_text=buttons_text,
                    location=(100, 60),
                    icon=icon
                    )


def popup_error(config, language, icon=GLOBAL_ICON):
    """Show a popup signaling that an error has occurred during the execution
    of the program, and calling for a restart

    :param config: A file with configs for the current localization
    :type config: configparser.ConfigParser
    :param language: The current localization
    :type language: str
    :param icon: The path to the popup icon
    :type icon: str
    :return: The window with the message can only be closed
    :rtype: None

    """
    pass
    # message = config.get(language, '-t_manual_data-')
    # title = config.get(language, '-n_manual_data-')
    # buttons_text = config.get(language, '-b_close-')
    #
    # return popup_Ok(config=config,
    #                 text=message,
    #                 title=title,
    #                 buttons_text=buttons_text,
    #                 location=(100, 60),
    #                 icon=icon)


# ToDo: Если успешно: "Закрыть программу? -> Да / Нет"
def popup_success(config, language, icon=GLOBAL_ICON):
    """Show a window signaling the successful completion of the program

    :param config: A file with configs for the current localization
    :type config: configparser.ConfigParser
    :param language: The current localization
    :type language: str
    :param icon: The path to the popup icon
    :type icon: str
    :return: The window with the message can only be closed
    :rtype: None

    """
    pass


def create_main_layout(config, language):
    """Assembling all the elements of the main window

    :param config: A file with configs for the current localization
    :type config: configparser.ConfigParser
    :param language: The current localization
    :type language: str
    :return: A list with all the elements of the interface (with a clear order)
    :rtype: list

    """
    main_layout = [
        # Welcome message
        [sg.Stretch(),
         sg.Text(config.get(language, '-t_welcome_prog-'),
                 justification='center',
                 auto_size_text=True,
                 font=('Arial', 16)
                 ),
         sg.Stretch(),
         ],

        # Buttons for manuals
        [sg.Button(config.get(language, '-b_manual_prog-'),
                   size_px=(400, 40),
                   key='-b_manual_prog-',
                   font=('Arial', 14),
                   # auto_size_button=True
                   ),
         sg.Stretch(),
         sg.Stretch(),
         sg.Button(config.get(language, '-b_manual_data-'),
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
        [sg.Text(config.get(language, '-t_welcome_data-'),
                 font=('Arial', 12),
                 )
         ],

        [sg.Text(config.get(language, '-t_data-'),
                 font=('Arial', 12),
                 ),
         sg.InputText(default_text=str(path.Path.home()),
                      key='-input_path-',
                      font=('Arial', 12),
                      ),
         sg.FileBrowse(config.get(language, '-b_data-'),
                       key='-b_browse_file-',
                       size=(150, 40),
                       font=('Arial', 12),
                       )

         ],

        # Spaces
        [sg.Text(size=(1, 20))],

        # Dir for saving
        [sg.Text(config.get(language, '-t_welcome_dir-'),
                 font=('Arial', 12),
                 )
         ],

        [sg.Text(config.get(language, '-t_dir-'),
                 font=('Arial', 12),
                 ),
         sg.InputText(default_text=str(path.Path.home()),
                      key='-output_path-',
                      font=('Arial', 12),
                      ),
         sg.FolderBrowse(config.get(language, '-b_dir-'),
                         key='-b_browse_dir-',
                         initial_folder=str(path.Path.home()),
                         size=(150, 40),
                         font=('Arial', 12),
                         ),
         ],

        # Spaces
        [sg.Text(size=(1, 50))],

        # Create buttons
        [sg.Button(config.get(language, '-b_create_UI-'),
                   key='-b_create_UI-',
                   font=('Arial', 12),
                   size_px=(300, 40)
                   ),
         sg.Button(config.get(language, '-b_create_UA-'),
                   key='-b_create_UA-',
                   font=('Arial', 12),
                   size_px=(300, 40)
                   ),
         sg.Button(config.get(language, '-b_create_UI_and_UA-'),
                   key='-b_create_UI_and_UA-',
                   font=('Arial', 12),
                   size_px=(300, 40)
                   ),
         ],

        # Spaces
        [sg.Text(size=(1, 50))],

        # Close button
        [sg.Stretch(),
         sg.Button(config.get(language, '-b_close-'),
                   key='-b_close-',
                   size_px=(120, 40),
                   font=('Arial', 12),
                   )
         ],
        ]

    return main_layout


def create_main_window(config, language):
    """Creating the main window of the program, styles and localization are
    immediately applied

    :param config: A file with configs for the current localization
    :type config: configparser.ConfigParser
    :param language: The current localization
    :type language: str
    :return: The main window of the program is ready for interaction
    :rtype: PySimpleGUIQt.PySimpleGUIQt.Window

    """
    # Add a theme
    sg.ChangeLookAndFeel(config.get('THEMES', "-theme_global-"))

    # sg.SetOptions(window_location=(300, 250))
    # Create the Window
    window = sg.Window(
            title=config.get(language, '-n_main_window-'),
            layout=create_main_layout(config, language),
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

    # Load configurations and language
    config, language = read_config_and_language()
    # Create the main window
    window = create_main_window(config, language)

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
            elif popup_close(config, language):
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
            if create_files(event=event,
                            values=values,
                            config=config,
                            language=language,
                            icon=GLOBAL_ICON
                            ):
                popup_success(config=config,
                              language=language
                              )
                print('Successfully')

            else:
                popup_error(config=config,
                            language=language
                            )
                print(f'Some error: \nEvent {event} \nValues {values}')

            # Unlocking the main window, ready to accept new commands
            window.Enable()

        # If the "show the manual to program work" button was pressed
        elif event == '-b_manual_prog-':
            show_manual_work_program(config, language)

        # If the "show the manual to table with authors data" button was pressed
        elif event == '-b_manual_data-':
            show_manual_input_data(config, language)

    # Exit from cycle and close the main window
    window.close()

    return None


def make_question_for_sure(config, language, config_key, path_data, path_dir):
    """Assembling the text to clarify the creation of a document with the
    selected parameters

    :param config: A file with configs for the current localization
    :type config: configparser.ConfigParser
    :param language: The current localization
    :type language: str
    :param config_key: The key that will get the desired text from the config
    :type config_key: str
    :param path_dir: Absolute path to the file with data about authors
    :type path_dir: str
    :param path_data: Absolute path to the directory for save creating files
    :type path_data: str
    :return: Clarifying question to the user with the settings selected by him
    :rtype: str

    """
    answer = config.get(language, config_key). \
        replace('$input_path$', path_data). \
        replace('$output_path$', path_dir)

    return answer


def create_files(event, values, config, language, icon):
    """Processing the pressed button and calling the corresponding function
    for creating documents

    :param event: The key of the current event in the GUI (button key)
    :type event: str
    :param values: Dictionary with current interface parameters
    :type values: dict
    :param config: A file with configs for the current localization
    :type config: configparser.ConfigParser
    :param language: The current localization
    :type language: str
    :param icon: The path to the popup icon
    :type icon: str
    :return: The key that informs about the success of the function
    :rtype: bool

    """
    path_input_data = values['-input_path-']
    path_output_dir = values['-output_path-']
    question = make_question_for_sure(config=config,
                                      language=language,
                                      config_key=event,
                                      path_data=path_input_data,
                                      path_dir=path_output_dir
                                      )

    # The key that informs about the success of the function
    status = False
    if popup_Yes_No(config=config,
                    text=question,
                    title=config.get(language, '-n_sure-'),
                    buttons_text=(config.get(language, '-b_yes-'),
                                  config.get(language, '-b_no-')),
                    icon=icon
                    ):
        if event == '-b_create_UI-':
            # result =
            make_only_UI(path_input_data, path_output_dir)

        elif event == '-b_create_UA-':
            # result =
            make_only_UA(path_input_data, path_output_dir)

        elif event == '-b_create_UI_and_UA-':
            # result =
            make_UI_and_UA(path_input_data, path_output_dir)

    return status


