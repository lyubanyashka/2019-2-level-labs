"""
Labour work #3
 Building an own N-gram model
"""

import math

REFERENCE_TEXT = ''
if __name__ == '__main__':
    with open('not_so_big_reference_text.txt', 'r') as f:
        REFERENCE_TEXT = f.read()


class WordStorage:
    def __init__(self):
        self.storage = {}

    def put(self, word: str) -> int:
        identifier = 0
        if word not in self.storage and isinstance(word, str):
            identifier += 1
            self.storage[word] = identifier
        return identifier

    def get_id_of(self, word: str) -> int:
        if word in self.storage:
            return self.storage.get(word)
        return -1

    def get_original_by(self, id_word: int) -> str:
        if id_word in self.storage.values():
            id_index = list(self.storage.values()).index(id_word)  # индексируем значение
            return list(self.storage.keys())[id_index]  # возвращаем ключ заданног индекса
        return "UNK"

    def from_corpus(self, corpus: tuple):
        if isinstance(corpus, tuple):
            for word in corpus:
                self.put(word)
        return corpus


class NGramTrie:
    def __init__(self, number):
        self.size = number
        self.gram_frequencies = {}
        self.gram_log_probabilities = {}
        self.prefixes = {}


    def fill_from_sentence(self, sentence: tuple) -> str:
        if not isinstance(sentence, tuple) or len(sentence) < self.size:
            return 'ERROR'
        n_gram = []
        for index, _ in enumerate(sentence[:-self.size + 1]):
            n_gram = []
            count = 0
            while count < self.size:
                n_gram.append(sentence[index + count])
                count += 1
            n_gram = tuple(n_gram)
            if n_gram in self.gram_frequencies:
                self.gram_frequencies[n_gram] += 1
            else:
                self.gram_frequencies[n_gram] = 1
        if n_gram == []:
            return 'ERROR'
        return 'OK'


    def calculate_log_probabilities(self):
        for gram in self.gram_frequencies:
            pref = gram[:-1]
            if pref in self.prefixes:
                self.prefixes[pref] += self.gram_frequencies[gram]
            else:
                self.prefixes[pref] = self.gram_frequencies[gram]
        for gram in self.gram_frequencies:
            if gram in self.gram_log_probabilities:
                continue
            else:
                self.gram_log_probabilities[gram] = math.log(self.gram_frequencies[gram] /
                                                             self.prefixes[gram[:-1]])


    def predict_next_sentence(self, prefix: tuple) -> list:
        if not isinstance(prefix, tuple) or len(prefix) + 1 != self.size:
            return []
        sentence = list(prefix)
        while True:
            prob_list = []
            for gram in list(self.gram_log_probabilities.keys()):
                if gram[:-1] == prefix:
                    prob_list.append(self.gram_log_probabilities[gram])
            if prob_list == []:
                break
            new_word = max(prob_list)
            for word, prob in list(self.gram_log_probabilities.items()):
                if new_word == prob:
                    new_word = word[-1]
            sentence.append(new_word)
            new_prefix = list(prefix[1:])
            new_prefix.append(new_word)
            prefix = tuple(new_prefix)
        return sentence


def encode(storage_instance, corpus) -> list:
    code_sentences = []
    for sentence in corpus:
        code_sentence = []
        for word in sentence:
            code_word = storage_instance.get_id_of(word)
            code_sentence += [code_word]
        code_sentences += [code_sentence]
    return code_sentences


def split_by_sentence(text: str) -> list:
    if not text or '.' not in text:
        return []
    text = text.lower()
    text = text.replace('\n', ' ')
    text = text.replace('!', '.')
    text = text.replace('?', '.')
    text = text.replace('  ', ' ')
    new_text = ''
    corpus = []
    for s in text:
        if s.isalpha() or s == '.' or s == ' ':
            new_text += s
    text_splitted = new_text.split(".")
    for sentence in text_splitted:
        if sentence != '':
            new_sentence = ['<s>']
            sentence = sentence.split()
            for word in sentence:
                if word != sentence:
                    new_sentence.append(word)
            new_sentence.append('</s>')
            corpus.append(new_sentence)
    return corpus




