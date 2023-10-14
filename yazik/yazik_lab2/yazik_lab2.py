"""Практическая работа №2"""
import os
import re

from docx import Document
from PyPDF2 import PdfReader

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def read_file(file_name):
    """Чтение файла"""
    if file_name.endswith('.docx'):
        document = Document(file_name)
        text = '\n\n'.join(
            [paragraph.text for paragraph in document.paragraphs])
    elif file_name.endswith('.pdf'):
        document = PdfReader(file_name)
        text = ''
        for page in document.pages:
            text += page.extract_text()
    else:
        text = ''
    return text


def preprocess_data(data):
    """Предобработка данных"""
    ref_data = re.sub(r'\b(\w+\.\w+)\b', r'__\1__', data).replace("\n", " ")
    symbols = ["!", "?", "…", "..", ".", ":", ";", "–", "«", "»", "* * *", ","]
    for symbol in symbols:
        ref_data = ref_data.replace(symbol, "")
    ref_data = ref_data.lower()
    return ref_data.split()


def main():
    """Main function"""
    pdf = read_file("Фрагмент.pdf")
    pdf_ = preprocess_data(pdf)
    print("Количество слов pdf: ", len(pdf_))
    print("Количество уникальных слов pdf: ", len(set(pdf_)))
    less_words_pdf = [word for word in pdf_ if len(word) < 3]
    docx = read_file("Фрагмент.docx")
    docx_ = preprocess_data(docx)
    print("Количество слов docx: ", len(docx_))
    print("Количество уникальных слов docx: ", len(set(docx_)))
    less_words_docx = [word for word in docx_ if len(word) < 3]
    print("Слова которые есть в pdf, но нет в docx: ",
          set(less_words_pdf) - set(less_words_docx))
    print("Слова которые есть в docx, но нет в pdf: ",
          set(less_words_docx) - set(less_words_pdf))
    # Вывод:
    # pdf имеет большее количество слов, чем docx, так как в pdf происходит неверное чтение текста.


if __name__ == '__main__':
    main()
