import docx
with open(r'/home/risovaniy/auto_UI_UA/resources/UA_template_utf_8.docx',) as f_1:
    with open(r'/home/risovaniy/auto_UI_UA/resources/UI_template.docx',
              'a',
              ) as f:

        f.write(f_1.readlines())
