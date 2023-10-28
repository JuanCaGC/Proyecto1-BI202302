import nltk
import re, string, unicodedata
import pandas as pd
import numpy as np
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
import num2words
from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin

nltk.download("punkt")
nltk.download('wordnet')
nltk.download("stopwords")
stop_words = stopwords.words("spanish")

# Limpieza de datos 
def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words

def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words

def replace_numbers(words):
    """Replace all interger occurrences in list of tokenized words with textual representation"""
    #p = inflect.engine()
    new_words = []
    for word in words:
        if word.isdigit():
            #new_word = p.number_to_words(word)
            new_word = num2words.num2words(word, lang='es')
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words

def remove_specialCoders(words):
    new_words = []
    for word in words:
        if  "Ã¡" in word:
            new_word = re.sub(r'Ã¡', 'á', word)
            new_words.append(new_word)
        elif "ao" in word:
            new_word = re.sub(r'ao', 'ú', word)
            new_words.append(new_word)
        elif "Ã" in word:
            new_word = re.sub(r'Ã', 'í', word)
            new_words.append(new_word)
        elif "a3" in word:
            new_word = re.sub(r'a3', 'ó', word)
            new_words.append(new_word)
        elif "Ã©" in word:
            new_word = re.sub(r'Ã©', 'é', word)
            new_words.append(new_word)
    
        else:
            new_words.append(word)
    return new_words

def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    return [word.lower() for word in words]

def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    return [word for word in words if word not in stop_words]


def preprocessing(words):
    words = to_lowercase(words)
    words = replace_numbers(words)
    words = remove_punctuation(words)
    words = remove_non_ascii(words)
    words = remove_stopwords(words)
    words = remove_specialCoders(words)
    return words

# Funciones para stem y lemmatize

def stem_words(words):
    """Stem words in list of tokenized words"""
    stemmer = LancasterStemmer()
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems

def lemmatize_verbs(words):
    """Lemmatize verbs in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas.append(lemma)
    return lemmas

def stem_and_lemmatize(words):
    stems = stem_words(words)
    lemmas = lemmatize_verbs(words)
    return stems + lemmas

# Agregar una clase personalizada para el preprocesamiento como parte del pipeline
class TextPreprocessor(BaseEstimator, TransformerMixin):
    def fit(self, x, y=None):
        return self

    def transform(self, X):
        return [preprocessing(text) for text in X]

# Agregar una clase personalizada para tokenizar como parte del pipeline
class TextWordTokenizer(BaseEstimator, TransformerMixin):
    def fit(self, x, y=None):
        return self

    def transform(self, X):
        return [word_tokenize(text) for text in X]

# Agregar una clase personalizada para el  lematización y eliminación de prefijos y sufijos como parte del pipeline
class TextStemLemmatizer(BaseEstimator, TransformerMixin):
    def fit(self, x, y=None):
        return self

    def transform(self, X):
        return [stem_and_lemmatize(text) for text in X]

# Agregar una clase personalizada para desTokenizar  como parte del pipeline
class TokensToTextTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return [(lambda x: ' '.join(map(str, x)))(text) for text in X]