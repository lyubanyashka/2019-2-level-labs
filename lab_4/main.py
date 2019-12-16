import math


def clean_tokenize_corpus(reference_texts: list) -> list:
    if not reference_texts or not isinstance(reference_texts, list):
        return []
    ref_texts_tokenized = []
    for reference_text in reference_texts:
        if not isinstance(reference_text, str):
            print("Incorrect type of text", reference_text)
            continue
        reference_text = reference_text.replace('<br />', " ")
        reference_text = reference_text.lower()
        reference_text = reference_text.replace('\n', ' ')
        ref_text_clean = []
        for word in reference_text.split(" "):
            word = ''.join([i for i in word if i.isalpha()])
            if word:
                ref_text_clean.append(word)
        ref_texts_tokenized += [ref_text_clean]
    return ref_texts_tokenized


class TfIdfCalculator:
    def __init__(self, corpus):
        self.corpus = corpus  # список из токенированных строк
        self.tf_values = []  # cписок из словарей
        self.idf_values = {}
        self.tf_idf_values = []

    def calculate_tf(self):
        if not self.corpus:
            return self.tf_values
        for text in self.corpus:
            term_to_frequency = {}
            if not text:
                continue

            total_words_num = 0
            for word in text:
                if isinstance(word, str):
                    total_words_num = total_words_num + 1
                    term_to_frequency[word] = term_to_frequency.get(word, 0) + 1
            for word, count in term_to_frequency.items():
                term_to_frequency[word] = count/total_words_num
            self.tf_values += [term_to_frequency]
        return self.tf_values

    def calculate_idf(self):
        if not self.corpus:
            return self.idf_values
        unique_words = set()
        for words_in_text in self.corpus:
            if not isinstance(words_in_text, list):
                continue
            for word in words_in_text:
                if not isinstance(word, str):
                    continue
                unique_words.add(word)

        # calculate word freq
        for unique_word in unique_words:
            counter = 0
            for words_in_text in self.corpus:
                if not words_in_text or unique_word in words_in_text:
                    counter += 1
            if counter != 0:
                self.idf_values[unique_word] = math.log(len(self.corpus) / counter)
        return self.idf_values

    def calculate(self):
        if not self.idf_values or not self.tf_values:
            return self.tf_idf_values
        for word_to_frequency in self.tf_values:
            tf_idf_values = {}
            for word, frequency in word_to_frequency.items():
                tf_idf_values[word] = frequency * self.idf_values.get(word)
            self.tf_idf_values += [tf_idf_values]
        return self.tf_idf_values

    def report_on(self, word, document_index):  # doc index - номер токенизир. текста из списка
        if not self.tf_idf_values or document_index >= len(self.corpus):
            return ()
        tf_idf = self.tf_idf_values[document_index][word]
        sort = sorted(self.tf_idf_values[document_index],
                      key=lambda w: int(self.tf_idf_values[document_index][w]), reverse=True)
        return tf_idf, sort.index(word)


def main():
    for text in ['5_7.txt', '15_2.txt', '10547_3.txt', '12230_7.txt']:
        with open(text, 'r') as f:
            reference_texts = [f.read()]

    # scenario to check your work
    test_texts = clean_tokenize_corpus(reference_texts)
    tf_idf = TfIdfCalculator(test_texts)
    tf_idf.calculate_tf()
    tf_idf.calculate_idf()
    tf_idf.calculate()
    print(tf_idf.report_on('good', 0))
    print(tf_idf.report_on('and', 1))


if __name__ == '__main__':
    main()
