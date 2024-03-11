import json
from os import listdir, path
from bs4 import BeautifulSoup


storage_directory = path.dirname('crawling/result/ru/')
lemmas_file = 'tokenizer/lemmas.txt'
inverted_index_file = 'inverted_index/inverted_index.txt'
inverted_index_json = 'inverted_index/inverted_index.json'


def get_texts():
    texts = dict()
    for file_name in listdir(storage_directory):
        html = open(storage_directory + '/' + file_name, 'r',
                    encoding='utf-8', errors='ignore')
        text = BeautifulSoup(html, features='html.parser').get_text().lower()
        html.close()
        texts[file_name] = text
    return texts


# def get_lemmas():
#     lemmas = dict()
#     lines = open(lemmas_file, encoding='windows-1251',
#                  errors='ignore').read().splitlines()
#     for l in lines:
#         lemmas[l.split(": ")[0]] = l.split(": ")[1].split(' ')
#     return lemmas

def get_lemmas():
    lemmas = dict()
    with open(lemmas_file, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) > 1:  # Проверка, что строка содержит хотя бы два элемента
                lemma = parts[0]  # Первый элемент считается леммой
                words = parts[1:]  # Остальные элементы - это слова
                lemmas[lemma] = words
            else:
                print(f"Ошибка: неправильный формат строки: {line}")
    return lemmas


def build_index():
    inverted_index = dict()
    lemmas = get_lemmas()
    texts = get_texts()

    for key, lemmas in lemmas.items():
        for file_name, text in texts.items():
            if any([l in text for l in lemmas]):
                if key not in inverted_index:
                    inverted_index[key] = set()
                inverted_index[key].add(file_name)

    for key in inverted_index.keys():
        inverted_index[key] = list(inverted_index[key])

    with open(inverted_index_file, 'w+', encoding='utf-8') as index:
        for key, files in inverted_index.items():
            index.write(key + ' ' + str(files) + '\n')

    with open(inverted_index_json, 'w', encoding='utf-8') as index:
        json.dump(inverted_index, index)

if __name__ == "__main__":
    build_index()
