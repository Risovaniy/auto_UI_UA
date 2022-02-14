import os

import pathlib as path


path1 = f'{path.Path.cwd()}{os.sep}ui_finish.docx'
path2 = f'.{os.sep}ui_finish.docx'

print(path1, '\n\n\n', path2)


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