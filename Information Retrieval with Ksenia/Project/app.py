import flask
from flask import Flask, request, render_template
import re
import nltk
from nltk.tokenize import word_tokenize
import string
import pymorphy2
import stop_words
from stop_words import get_stop_words
from IPython.display import HTML, display
import numpy as np
import pickle

def delete_stop_words(s, lng):
    stop_words = get_stop_words(lng)
    s -= set(stop_words)
    return s

def preprocessing(text):
    text = ''.join([i for i in text if i not in set(string.punctuation)])
    text = text.lower()
    words = word_tokenize(text)
    morph = pymorphy2.MorphAnalyzer()
    lemmas = set()
    for word in words:
        lemmas.add(morph.parse(word)[0].normal_form)
    lemmas_new = delete_stop_words(lemmas, 'ru')
    return lemmas_new

def average_len(D):
    return np.mean([len(i) for i in D])

from math import log

k1 = 1.2
k2 = 100
b = 0.75
R = 0.0

from math import log

k1 = 2.0
b = 0.75

def score_BM25_i(n, fq, N, dl, avdl):
    K = compute_K(dl, avdl)
    IDF = log((N - n + 0.5) / (n + 0.5))
    frac = ((k1 + 1) * fq) / (K + fq)
    return IDF * frac


def compute_K(dl, avdl):
    return k1 * ((1-b) + b * (float(dl)/float(avdl)))

def score_BM25(Q, D, D_j, i_reverse, avdl):
    s = 0
    for i in Q:
        f = 0
        if i in i_reverse:
            f = len([j==i for j in D_j])
            s += score_BM25_i(len(i_reverse[i]), f, len(D), len(D_j), average_len(D))
    return s

def search(Q):
    if type(Q) != str:
        raise BaseException('Request must be str type')
    if re.compile("\w+( \w+)*").match(Q).span() != (0, len(Q)):
        raise BaseException('Input words seperated by spaces')
    
    Q = Q.lower()
    Q_words = word_tokenize(Q)
    morph = pymorphy2.MorphAnalyzer()
    Q_lemmas = set()
    for word in Q_words:
        Q_lemmas.add(morph.parse(word)[0].normal_form)
    Q_lemmas = delete_stop_words(Q_lemmas, 'ru')
    
    with open('collection.pickle', 'rb') as f:
        D = pickle.load(f)
        
    with open('ir.pickle', 'rb') as f:
        ir = pickle.load(f)
    
    with open('collection_with_data.pickle', 'rb') as f:
        collection_with_data = pickle.load(f)
        
    good_Ds = []
    for lemma in Q_lemmas:
        if lemma in ir:
            good_Ds += ir[lemma]
    good_Ds = set(good_Ds)
    scores = {}
    for i in good_Ds:
        d = D[i]
        link = collection_with_data[i][0]
        head = collection_with_data[i][2]
        scores[(link, head)] = score_BM25(Q_lemmas, D, d, ir, average_len(D))
    return sorted(scores, key=scores.get, reverse=True)[:10]


app = Flask(__name__)
@app.route('/')

def index():
    if request.args:
        query = request.args.get['query']
        links = search(query)
        return render_template('index.html',links=links)
    return render_template('index.html',links=[])

if __name__ == '__main__':
    app.run()
