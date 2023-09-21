# -*- coding: utf-8 -*-
"""Contains tools for preprocess text data.
@author scorrea
"""
import re
import string
import numpy as np
from nltk.stem import SnowballStemmer
import spacy
nlp = spacy.load("es_core_news_sm")



SUPPPORTED_LANG_STEMMER = {
    'SPA': SnowballStemmer('spanish'),
    'ENG': SnowballStemmer('english'),
    'PRT': SnowballStemmer('portuguese'),
}


def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)

    return input_txt

def rm_pun_num_esp_cha(pandas_input):
   return pandas_input.str.replace("[^a-zA-Z#]", " ")

def rm_links(pandas_input):
   return pandas_input.str.replace("[http\S+#]", " ")


def rm_esp_cha(pandas_input):
   return pandas_input.str.replace("[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕñçÇ: ]", " ")

def rm_length_word(input_data, word_length=3):
    return input_data.apply(lambda x: ' '.join([w for w in x.split() if len(w) > word_length]))

def tokenize(input_data):
    return input_data.apply(lambda x: x.split())

def to_lower(input_data):
    return input_data.apply(lambda x: x.lower())

def clean(text):
    text = re.sub(r"#(\w+)",'', text)
    text = re.sub('\S*@\S*\s?', '', text)  # remove emails
    return text

def clean_text(input_data):
    return input_data.apply(lambda x: clean(x))

def clean_text_spacy(input_data):
    return input_data.apply(lambda x: clean_spacy(x))
def clean_spacy(text):
    resultado = list()
    for token in nlp(text):
        if not token.is_punct and not token.is_space and not token.is_stop and not token.like_num and not token.pos_ == "PROPN" and len(token.lemma_)>3 and not token.lemma_=="abrir" and not token.lemma_=="hilo":
            resultado.append(token.lemma_.split()[0])
    return " ".join(resultado)

def _check_lang(lang):
   if lang in SUPPPORTED_LANG_STEMMER:
        return True
   else:
        return False

def stemmer(input_data, language='ENG'):
    if  _check_lang(language):
        stemmer = SUPPPORTED_LANG_STEMMER[language]
        return input_data.apply(lambda x: [stemmer.stem(i) for i in x])
    else:
        raise "Language {} not sopported for stemming".format(language)

def join_tokenize(input_data, join_char=' '):
    return input_data.apply(lambda x: join_char.join(x))

def hashtag_extract(input_data, flatten=True):
    hashtags = []
    for i in input_data:
        ht = re.findall(r"#(\w+)", i)
        if flatten:
            hashtags.append(ht)
        else:
            hashtags.append([ht])

    return sum(hashtags, [])

def hashtag_rm(input_data):
    return input_data.replace('#', '')



def obtener_bigramas(input_data):
    resultado=[]
    bigrams = [b for l in input_data for b in zip(l.split(" ")[:-1], l.split(" ")[1:])]
    #print(bigrams)
    for big in bigrams:
        resultado.append("-".join(big))
    return resultado



if __name__ == "__main__":
   
   #print(clean_spacy('Me sabia las respuestas, pero los demas no debian saberlo'))
   list = ['Stop. look left right. go']
   print ("The given list is : \n" + str(list))
   output = [m for n in list for m in zip(n.split(" ")[:-1], n.split(" ")[1:])]
   print ("Bigram formation from given list is: \n" + str(output))
