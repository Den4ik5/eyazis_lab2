from pyquery import PyQuery
import nltk

bi_grams = {}
tri_grams = {}
quad_grams = {}
all_grams = {}

dict_with_grams = {
    1: bi_grams,
    2: tri_grams,
    3: quad_grams
}


def tokenize(sentences):
    list_word = []
    for sent in nltk.sent_tokenize(sentences.lower()):
        for word in nltk.word_tokenize(sent):
            list_word.append(word)
    return list_word


def check_word(word, n):
    words_dict = dict_with_grams[n - 1]
    try:
        int(word)
    except ValueError:
        try:
            if words_dict[word]:
                words_dict[word] += 1
        except KeyError:
            words_dict.update({word: 1})


def n_gram(word, n):
    if len(word) == n:
        check_word(word, n)
    if len(word) > n - 1:
        start_pos = 0
        while start_pos + n - 1 < len(word):
            check_word(word[start_pos:start_pos + n], n)
            start_pos += 1


def n_gram_model_create(list_word):
    all_grams.clear()
    bi_grams.clear()
    tri_grams.clear()
    quad_grams.clear()
    for item in list_word:
        n_gram(item, 2)
        n_gram(item, 3)
        n_gram(item, 4)
    all_grams.update(bi_grams)
    all_grams.update(tri_grams)
    all_grams.update(quad_grams)
    t = (sorted(all_grams.items(), key=lambda x: x[1]))[::-1][0:400]
    return [x[0] for x in t]


def read_file(route):
    with open(route, encoding='utf-8') as file:
        return file.read()


def html_parser(html):
    pq = PyQuery(html)
    tag = pq('p')
    return tag.text()


def distance(first, second):
    all_dist = 0
    count = 0
    for item in first:
        if item in second:
            count += 1
            x = first.index(item)
            y = second.index(item)
            dist = abs(x-y)
            all_dist += dist
    return count


def start_n_gram():
    text_fr = html_parser(read_file('text_fr.html'))
    text_de = html_parser(read_file('text_de.html'))
    model_fr = n_gram_model_create(tokenize(text_fr))
    model_de = n_gram_model_create(tokenize(text_de))
    i = 1
    print('Метод n-грамм:')
    while i < 5:
        name = 'test' + str(i) + '.html'
        text = html_parser(read_file(name))
        model = n_gram_model_create(tokenize(text))
        count_fr = distance(model, model_fr)
        count_de = distance(model, model_de)
        if count_fr > count_de:
            print('Текст ' + name + ' на французском')
        else:
            print('Текст ' + name + ' на английском')
        i += 1
    print('\n')


start_n_gram()
################################################

fr_al = 'abcdefghijklmnopqrstuvwxyzàèùéâêîôûçëïüÿ'
de_al = 'abcdefghijklmnopqrstuvwxyzäöüß'

t = []


def start_al():
    d = 1
    print('Алфавитный метод:')
    while d < 5:
        name = 'test' + str(d) + '.html'
        text = html_parser(read_file(name))
        model = tokenize(text)
        for item in model:
            for i in item:
                t.append(i)
        letter = set(t)
        count_fr = 0
        count_de = 0
        for k in letter:
            for j in fr_al:
                if k == j:
                    count_fr += 1
            for l in de_al:
                if k == l:
                    count_de += 1
        if count_fr > count_de:
            print('Текст ' + name + ' на французском')
        else:
            print('Текст ' + name + ' на английском')
        d += 1
    print('\n')


start_al()

############################

service_words_fr = ['cette', 'ce', 'cet', 'сes ', 'ma', 'ta', 'sa', 'mon', 'ton', 'son',
                    'mes', 'tes', 'ses', 'notre', 'votre', 'leur', 'nos', 'vos', 'leurs',
                    'un', 'une', 'des', 'du', 'dela', 'le', 'la', 'les', 'au', 'aux',
                    'quel', 'quelle', 'quels', 'quellles', 'de', 'à']

service_words_de = ['as', 'I', 'his', 'that', 'he', 'was', 'for', 'on', 'are',
                    'with', 'they', 'be', 'at', 'one', 'have', 'this', 'from', 'by',
                    'hot', 'word', 'but', 'what', 'some', 'is', 'it', 'you', 'or', 'had', 'the']


def start_s_w():
    d = 1
    print('Метод служебных слов:')
    while d < 5:
        name = 'test' + str(d) + '.html'
        text = html_parser(read_file(name))
        model = tokenize(text)
        count_fr = 0
        count_de = 0
        for item in model:
            for ser_w_fr in service_words_fr:
                if item == ser_w_fr:
                    count_fr += 1
            for ser_w_de in service_words_de:
                if item == ser_w_de:
                    count_de += 1
        if count_fr > count_de:
            print('Текст ' + name + ' на французском')
        else:
            print('Текст ' + name + ' на английском')
        d += 1


start_s_w()
