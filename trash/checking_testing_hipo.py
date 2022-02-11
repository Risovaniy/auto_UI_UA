from docx import Document

files = [r'/home/risovaniy/auto_UI_UA/resources/UI_template_utf_8.docx',
         r'/home/risovaniy/auto_UI_UA/resources/UA_template_utf_8.docx']


def combine_word_documents(files):
    merged_document = Document()

    for index, file in enumerate(files):
        sub_doc = Document(file)

        if index < len(files) - 1:
            sub_doc.add_page_break()

        for element in sub_doc.element.body:
            merged_document.element.body.append(element)

    merged_document.save('d3.docx')


combine_word_documents(files)


