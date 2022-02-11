import os

import pathlib as path


path1 = f'{path.Path.cwd()}{os.sep}ui_finish.docx'
path2 = f'.{os.sep}ui_finish.docx'

print(path1, '\n\n\n', path2)
