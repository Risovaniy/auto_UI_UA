import docx
from docx.shared import Inches


def open_docx_file(path):
    return docx.Document(path)

    # return doc


if __name__ == '__main__':
    doc = open_docx_file('/home/risovaniy/auto_UI_UA/resources/UA_template.docx')
    doc2 = open_docx_file('/home/risovaniy/auto_UI_UA/resources/UA_template.docx')

    doc.styles['Normal'].font.name = 'Times New Roman'
    doc.styles['Normal'].font.size = docx.shared.Pt(12)

    doc.add_paragraph()

    # First number is the paragraph, second number - run in this paragraph
    run_0_0 = doc.paragraphs[-1].add_run()
    run_0_0.text = "Я, "

    run_0_1 = doc.paragraphs[-1].add_run()
    run_0_1.text = f"\t\tМоя информация строка 670\t\t\t\t\t,"
    run_0_1.font.underline = True

    doc.add_paragraph()

    # doc.paragraphs[-1].alignment = WD_TABLE_ALIGNMENT.CENTER
    run_1 = doc.paragraphs[-1].add_run()
    run_1.text = "(ФИО автора)"
    run_1.font.size = docx.shared.Pt(10)  # 8 it is just for tests

    doc.add_paragraph()

    run_2_0 = doc.paragraphs[-1].add_run()
    run_2_0.text = "настоящим уведомляю "

    [doc.add_paragraph()]*5

    # parag = doc.paragraphs[-1]
    # parag.text = doc2
    print(f'\tЯ, ____\n{doc.paragraphs[3].text}\n\n'
          f'\tНаименование созданного РИД:\n{doc.paragraphs[-45].text}')


    input()

    doc.save('/home/risovaniy/auto_UI_UA/trash/my_first_test.docx')
