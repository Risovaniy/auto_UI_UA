# ***Assistant for creating documentation for the RID (UI and UA)*** or  ***auto_UI_UA***

The program, based on input data about the authors who created the SERIES, 
generates blanks for accompanying documentation: *notification of performers* 
(**UI**) and *notification of authors* (**UA**)

### Lounch program
1. Clone this repository 
2. Go to the main program directory (it is important for correct working of program)
3. Launch the main.py


### Features
Works in graphical mode


### Imports and installs

- os 
  - file access all depends on the OS (operating system)
  - included in the standard package

- pathlib
  - loading standard PC paths
  - included in the standard package
  
- sys
  - error handling from sys.exc_info()
  - included in the standard package

- PySimpleGUIQt
  - implementation of all graphical interface
  - pip install PySimpleGUIQt
  - PySide - following package

- datetime 
  - working with dates
  - included in the standard package

- locale
  - Russian names of months creates
  - included in the standard package

- pandas as pd
  - working with data
  - pip install pandas 

- docx
  - creating .docx files
  - pip install python-docx

- re
  - extract an extension from the filename
  - included in the standard package 

- configparser 
  - loading data from a file with .ini configurations
  - included in the standard package 

- pandas_ods_reader 
  - Reading tables from LibreOffice
  - lxml, ezodf - following packages
  - pip install pandas_ods_reader

- openpyxl
  - Reading data from xlsx files 
  - they are not directly imported, but they are required for installation to support this extension.
  - pip install openpyxl

- xlrd
  - Reading data from xls files 
  - they are not directly imported, but they are required for installation to support this extension.
  - pip install xlrd
