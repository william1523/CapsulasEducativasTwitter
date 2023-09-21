import json
import traceback
import pandas as pd
import datetime
import numpy as np
import mglearn
from ..models import Tema, Busqueda, Tweet
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from .functions import tokenize,to_lower,clean_text,clean_text_spacy, obtener_bigramas
import gensim
import gensim.corpora as corpora
from gensim.corpora import Dictionary
from gensim.models.coherencemodel import CoherenceModel
from gensim.models.ldamodel import LdaModel
from twitter.util.openaiapi import openai_api
import pickle
import re
import itertools
from collections import defaultdict
import pyLDAvis
import pyLDAvis.gensim
import base64
import io
from sentiment_analysis_spanish import sentiment_analysis
import spacy
nlp = spacy.load("es_core_news_sm")



class process_tweets:
    numero_tweets= 0
    df_palabras_topico = pd.DataFrame()
    df_verbos = pd.DataFrame()
    df_lda = pd.DataFrame()
    json_coherencia=''
    json_topwords=''
    json_topbigramas=''
    json_hashtags=''
    palabras_guion = ''
    texto_guion=''
    contexto_guion=''


    def __init__(self):
        self.df = pd.DataFrame()
    
    def getTweetsTema(self,id_tema:int):
        tema = Tema.objects.get(pk=id_tema)
        #tema.pk=id_tema
        self.contexto_guion=tema.contexto
        busquedas = Busqueda.objects.filter(tema=tema)    
        resultado_busqueda= Tweet.objects.filter(busqueda__in=busquedas)
        df = pd.DataFrame(list(resultado_busqueda.values('id_tweet', 'texto', 'texto_limpio','autor','hashtags')))
        df['hashtags']=df['hashtags'].apply(lambda x: " ".join(x.strip("][").replace("'","").split(",")))
        df['hashtags'] = to_lower(df['hashtags'])
        self.df=df

    def getTweets(self,id_busqueda:int):
        try:
            sentiment = sentiment_analysis.SentimentAnalysisSpanish()
            print(id_busqueda)
            busqueda = Busqueda()
            busqueda.pk = id_busqueda
            resultado_busqueda=Tweet.objects.filter(busqueda=busqueda)
            
            self.df = pd.DataFrame(list(resultado_busqueda.values('id_tweet', 'texto', 'autor')))
            df = self.df

            df['texto_limpio'] = to_lower(df['texto'])
            df['texto_limpio'] = clean_text(df['texto_limpio'])
            df['texto_limpio'] = clean_text_spacy(df['texto_limpio'])
            df["sentimiento"] = df['texto_limpio'].apply(sentiment.sentiment)
            self.df=df
        except:
            print("An exception occurred")
            traceback.print_exc()
        print(df['texto_limpio'])            
        return df
    def getwordcloud(self):
        print("get wordcloud sin paramtros")
        return self.getwordcloudP(','.join(list(self.df['texto_limpio'].values)))

    def getwordcloudP(self, long_string):
        wordcloud = WordCloud(background_color="white", max_words=500, contour_width=3, contour_color='steelblue')
        wordcloud.generate(long_string)
        wordcloud.to_image()
        buffer = io.BytesIO()
        wordcloud.to_image().save(buffer, 'png')
        b64 = base64.b64encode(buffer.getvalue())
        b64 = b64.decode('utf-8')
        buffer.close()
        return b64
    
    def ldaModel(self):
        tweets= tokenize(self.df['texto_limpio']).values.tolist() 
        id2word = Dictionary(tweets)
        corpus = [id2word.doc2bow(text) for text in tweets]
        coherencia=[]
        n = range(1,30)
        for i in n:
            lda_model = LdaModel(corpus=corpus,
                    id2word=id2word,
                    num_topics=i,
                    random_state=0,
                    chunksize=100,
                    alpha='auto',
                    per_word_topics=True)
            coherence_model_lda = CoherenceModel(model=lda_model, texts=tweets, dictionary=id2word, coherence='c_v')
            coherence_lda = coherence_model_lda.get_coherence()
            coherencia.append(coherence_lda)
        orden=[b[0]+1 for b in sorted(enumerate(coherencia),key=lambda i:i[1],reverse=True)]
        #b[0] tiene el numero de topicos con el valor de coherencia mas alto para el proceso LDA
      
        self.df_lda['labels']=coherencia
        self.df_lda['num_topicos']=[b[0]+1 for b in enumerate(coherencia)]

        data={}
        data['labels']=[b[0]+1 for b in enumerate(coherencia)]
        data['datasets']=[]
        dataset = {}
        dataset['label']="Coherencia LDA"
        dataset['data']=coherencia
        dataset['borderColor']='rgb(54, 162, 235)'
        dataset['backgroundColor']='rgba(54, 162, 235,0.5)'
        
        data['datasets'].append(dataset)
        self.json_coherencia = json.dumps(data)
        print('json data para grafico {}'.format(self.json_coherencia))


        lda_model = LdaModel(corpus=corpus,
                    id2word=id2word,
                    num_topics=orden[0],
                    random_state=0,
                    chunksize=100,
                    iterations=500,
                    alpha='auto',

                    per_word_topics=True)
        #numero de topicos ideal es orden[0]
        #numero de topicos ideal es el     
        

        #pprint(lda_model.print_topics())
        coherence_model_lda = CoherenceModel(model=lda_model, texts=tweets, dictionary=id2word, coherence='c_v')
        coherence_lda = coherence_model_lda.get_coherence()


        numero_palabras=50 // orden[0]
        palabras_topicos=[]

        for index, topic in lda_model.show_topics(formatted=False, num_words= numero_palabras):
            print('Topic: {} \nWords: {}'.format(index, [w[0] for w in topic]))
            palabras_topicos.append(",".join([w[0] for w in topic]))
        #doc_lda = lda_model[corpus]
        #print(doc_lda)
        palabras2=''
        for idx, x in enumerate(palabras_topicos):
            print(idx, x)
            palabras2+=x
            if idx+1<len(palabras_topicos):
                palabras2+=","
        try:

            print("palabras topicos {}".format(palabras2))
            #tratar de filtrar repetidos
            resultado = list()
            for token in nlp(palabras2):
                #print(token.text)
                if not resultado.__contains__(token.lemma_.split()[0]):
                    resultado.append(token.lemma_.split()[0])
                print("token {} pos_ {} lema {}".format(token.text,token.pos_, token.lemma_))
            print(" ".join(resultado))
            self.palabras_guion=''
            for idx, x in enumerate(resultado):
                print(idx, x)
                self.palabras_guion+=x
                if idx+1<len(resultado):
                    self.palabras_guion+=","
        except:
            print("An exception occurred")
            traceback.print_exc()
       
        print('\nCoherence Score:\n ', coherence_lda)
        print("fin imprime topicos")
        return pyLDAvis.gensim.prepare(lda_model, corpus, id2word).to_json()

    def topWords(self):
        tweets= tokenize(self.df['texto_limpio']).values.tolist()    
        id2word = Dictionary(tweets)
        bow_corpus = [id2word.doc2bow(doc) for doc in tweets]
        total_count = defaultdict(int)
        for word_id, word_count in itertools.chain.from_iterable(bow_corpus):
            total_count[word_id] += word_count

        # Top words
        df1= pd.DataFrame(sorted(total_count.items(), key=lambda x: x[1], reverse=True)[:20])
        df1.columns = ['id_word', 'quantity']
        df1['word']=df1.apply(lambda row: id2word[row.id_word], axis=1)
        print(df1)
        data={}
        data['labels']=list(df1['word'])
        data['datasets']=[]
        dataset = {}
        dataset['label']="Top Palabras"
        dataset['data']=list(df1['quantity'])
        dataset['borderColor']='rgb(54, 162, 235)'
        dataset['backgroundColor']='rgba(54, 162, 235,0.5)'
        
        data['datasets'].append(dataset)
        self.json_topwords = json.dumps(data)
        print("json para topten {}".format(self.json_topwords))


        bigramas= obtener_bigramas(self.df['texto_limpio']) 
        tweets = [d.split() for d in bigramas]

        id2word = Dictionary(tweets)
        bow_corpus = [id2word.doc2bow(doc) for doc in tweets]
        total_count = defaultdict(int)
        for word_id, word_count in itertools.chain.from_iterable(bow_corpus):
            total_count[word_id] += word_count

        # Top bigramas
        df1= pd.DataFrame(sorted(total_count.items(), key=lambda x: x[1], reverse=True)[:20])
        df1.columns = ['id_word', 'quantity']
        df1['word']=df1.apply(lambda row: id2word[row.id_word], axis=1)
        
        data={}
        data['labels']=list(df1['word'])
        data['datasets']=[]
        dataset = {}
        dataset['label']="Top Bigramas"
        dataset['data']=list(df1['quantity'])
        dataset['borderColor']='rgb(54, 162, 235)'
        dataset['backgroundColor']='rgba(54, 162, 235,0.5)'
        
        data['datasets'].append(dataset)
        self.json_topbigramas = json.dumps(data)
        print("json para topten {}".format(self.json_topbigramas))

        #analizar hashtags
        tweets= tokenize(self.df['hashtags']).values.tolist()    
        #tweets = [d.split() for d in bigramas]

        id2word = Dictionary(tweets)
        bow_corpus = [id2word.doc2bow(doc) for doc in tweets]
        total_count = defaultdict(int)
        for word_id, word_count in itertools.chain.from_iterable(bow_corpus):
            total_count[word_id] += word_count

        # Top bigramas
        df1= pd.DataFrame(sorted(total_count.items(), key=lambda x: x[1], reverse=True)[:20])
        df1.columns = ['id_word', 'quantity']
        df1['word']=df1.apply(lambda row: id2word[row.id_word], axis=1)
        
        data={}
        data['labels']=list(df1['word'])
        data['datasets']=[]
        dataset = {}
        dataset['label']="Top Hashtags"
        dataset['data']=list(df1['quantity'])
        dataset['borderColor']='rgb(54, 162, 235)'
        dataset['backgroundColor']='rgba(54, 162, 235,0.5)'
        
        data['datasets'].append(dataset)
       
        self.json_hashtags = json.dumps(data)
        print("json para hashtags {}".format(self.json_hashtags))
        
        



    def json_lda_coherencia(self):
        return self.json_coherencia

    def preprocesar_tweets(self,id_busqueda:int):
        try:
            sentiment = sentiment_analysis.SentimentAnalysisSpanish()
            print(id_busqueda)
            busqueda = Busqueda()
            busqueda.pk = id_busqueda
            resultado_busqueda=Tweet.objects.filter(busqueda=busqueda)
            df = pd.DataFrame(list(resultado_busqueda.values('id_tweet', 'texto')))
            df['texto_limpio'] = to_lower(df['texto'])
            df['texto_limpio'] = clean_text(df['texto_limpio'])
            df['texto_limpio'] = clean_text_spacy(df['texto_limpio'])
            df["sentimiento"] = df['texto_limpio'].apply(sentiment.sentiment)
            for ind in df.index:
                obj = Tweet.objects.get(pk=df['id_tweet'][ind])
                obj.texto_limpio = df['texto_limpio'][ind]
                obj.sentimiento = df['sentimiento'][ind]
                obj.save()
        except:
            print("An exception occurred")
            traceback.print_exc()
    
    def generar_guion(self):
        try:
            api=openai_api()
            #contexto="Debe promover el fortalecimiento de la autoestima, promover la activación de sentimientos y emociones que promueban la empatia.  Debe ser comprendido por niños de 8 años"
            palabras = "ayudar,historia,personal,aportar,trabajo,publicar,tema,normal,trabajar,gracias,denuncia,prueba,forma,sexual,denunciar,foto,llevar,pedir,niño,tema,alguien,entender,niño,caso,hablar,deber,pensar,seguir,situación,acoso,víctima,tipo,decir,casa,familia,esperar,llegar,haber,dejar,gente"
            respuesta=api.generarCapsula(contexto=self.contexto_guion, palabras=self.palabras_guion)
            print(respuesta['choices'][0]['text'])
            return respuesta['choices'][0]['text']
        except:
            print("An exception occurred")
            traceback.print_exc()
            
    