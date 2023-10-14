"""Практическая работа №1"""
import re
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def read_file(path):
    """Чтение файла"""
    with open(path, 'r', encoding='utf-8') as file:
        data = file.read()
    return data


def preprocess_data(data):
    """Предобработка данных"""
    ref_data = re.sub(r'\b(\w+\.\w+)\b', r'__\1__', data)
    symbols = ["!", "?", "...", ".."]
    for symbol in symbols:
        ref_data = ref_data.replace(symbol, ".")
    ref_data = ref_data.replace("\n", " ")
    return ref_data


def main():
    """Main function"""
    data = read_file('text.txt')
        # Удаление знаков препинания
    ref_data = preprocess_data(data)
    sentences = re.split(r'(?<=[.])\s+', ref_data)
    for i, sentence in enumerate(sentences):
        sentences[i] = re.sub(r'[^\w\s]', '', sentence).split()
    words = [word for sentence in sentences for word in sentence]
    print("Количество слов: ", len(words))
    unique_words = set(words)
    print("Количество уникальных слов: ", len(unique_words))
    print("Количество предложений: ", len(sentences))
        # Самое короткое и самое длинное слово (Слова которые больше 1 символа)
    words_ = [word for word in words if len(word) > 1]
        # Удаление стоп-слов
    with open('stop_words_russian.txt', 'r', encoding='utf-8') as file:
        stop_words = file.read().split()
        # Массив слов без стоп-слов
    words_ = [word for word in words_ if word not in stop_words]
    print("Самое короткое слово: ", min(words_, key=len))
    print("Самое длинное слово: ", max(words_, key=len))
    print("Средняя длина слов: ", round(sum(len(word)
          for word in words_) / len(words_)))
    # Средняя длина предложений (по количеству слов)
    print("Средняя длина предложений: ", round(sum(len(sentence)
          for sentence in sentences) / len(sentences)))
    print("Медианная длина слов: ", len(
        sorted(words_, key=len)[len(words_) // 2]))
    # Медианная длина предложений (по количеству слов)
    print("Медианная длина предложений: ", len(
        sorted(sentences, key=len)[len(sentences) // 2]))
    print("Введите первую букву: ")  # Номер по списку 4 - Вариант 1
    letter = input()
    while len(letter) != 1:
        print("Введите только одну букву: ")
        letter = input()
    words_letter = [word.lower() for word in words_ if word[0] == letter.lower()]
    print(set(words_letter))
    print("Количество слов начинающихся с буквы ",
          letter, ": ", len(words_letter))


if __name__ == '__main__':
    main()
