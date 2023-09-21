import traceback
from django.db import models
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from .twitterapi import BusquedaTwitter
from .util.searchBySelenium import searchBySelenium

# Create your models here.

class Tema(models.Model):
    tema = models.CharField(max_length=200)
    descripcion = models.TextField(null=True)
    fcreacion = models.DateField('Fecha Creación',auto_now_add=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.RESTRICT, blank=True, null=True)
    contexto = models.TextField(max_length=300)
    #busquedas = Busqueda.objects.filter(programme = programme_id)
    def __str__(self):
        return self.tema

class Autor(models.Model):
    id_autor= models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=150)
    nombre_usuario = models.CharField(max_length=150)
    numero_seguidores = models.IntegerField(null=True)
    def __str__(self):
        return self.nombre_usuario



class Tweet(models.Model):
    id_tweet = models.BigIntegerField(primary_key=True)
    texto = models.CharField(max_length=4000)
    texto_limpio = models.CharField(null=True,max_length=4000)
    autor = models.ForeignKey(Autor, on_delete=models.RESTRICT)
    fcreacion = models.DateTimeField('Fecha Creación')
    retweets = models.IntegerField(null=True)
    respuestas = models.IntegerField(null=True)
    megusta = models.IntegerField(null=True)
    citas = models.IntegerField(null=True)
    vistas = models.IntegerField(null=True)
    retweet = models.BooleanField (null=True)
    tweet_url = models.CharField(max_length=600, blank=True, null=True)
    mentions = models.CharField(max_length=600, blank=True, null=True)
    hashtags = models.CharField(max_length=600, blank=True, null=True)
    sentimiento= models.FloatField(null=True)
    respuesta_de = models.ForeignKey('self', on_delete=models.RESTRICT,null=True)
    def __str__(self):
        return self.texto
    
class Busqueda(models.Model):
    query = models.CharField(max_length=300)
    descripcion = models.CharField(max_length=300)
    numero_resultados = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    numero_respuestas = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    fbusqueda = models.DateField('Fecha',auto_now_add=True)
    reciente = models.BooleanField (null=True)
    buscar_respuestas = models.BooleanField (null=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.RESTRICT, blank=True, null=True)
    tema = models.ForeignKey(Tema, on_delete=models.RESTRICT)
    tweets = models.ManyToManyField(Tweet)
    def __str__(self):
        return self.descripcion
    def save(self, *args, **kwargs):
        fuente="selenium"
        try:
            if "api" in fuente:
                b = BusquedaTwitter()
                resultados= b.busqueda(self.query,self.numero_resultados)
                print(resultados)
                print(resultados.meta['result_count'])
                users=[]
                usuarios =  []
                tweets = []
                if resultados.meta['result_count']>0:
                    print(' inicio includes')
                    print(resultados.includes)
                    print(' fin includes')
                    users = resultados.includes["users"]
                    print(users)
                    users = {user["id"]: user for user in users}
                    print(' usuarios')
                    print(users)

                    for resultado in resultados.data:
                        #attachments', 'author_id', 'context_annotations', 'conversation_id', 'created_at', 'data', 'entities', 'geo', 'get', 'id', 'in_reply_to_user_id', 'items', 'keys', 'lang', 'non_public_metrics', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'source', 'text', 'values', 'withheld
                        tweet_nuevo = Tweet()
                        autor = Autor()
                        users[resultado.author_id].username
                        
                        autor.id_autor=resultado.author_id
                        autor.nombre_usuario = users[resultado.author_id].username
                        autor.nombre=users[resultado.author_id].name

                        print(users[resultado.author_id])

                        tweet_nuevo.id_tweet=resultado.id
                        tweet_nuevo.texto=resultado.text
                        tweet_nuevo.fcreacion=resultado.created_at
                        tweet_nuevo.origen=resultado.source
                        print('public_metrics')
                        print(resultado.in_reply_to_user_id)
                        print('organic_metrics')
                        print(resultado.geo)
                        print('promoted_metrics')
                        print(resultado.referenced_tweets)
                        print('keys')
                        print(resultado.items)

                        tweet_nuevo.megusta=resultado.public_metrics['like_count']
                        tweet_nuevo.respuestas=resultado.public_metrics['reply_count']
                        tweet_nuevo.retweets=resultado.public_metrics['retweet_count']
                        tweet_nuevo.citas=resultado.public_metrics['quote_count']
                        tweet_nuevo.vistas=resultado.public_metrics['impression_count']
                        tweet_nuevo.origen = resultado.source
                        tweet_nuevo.autor=autor
                        tweet_nuevo.fcreacion=resultado.created_at
                        tweet_nuevo.busqueda=self

                        print(tweet_nuevo)
                        print('context_annotations')
                        print(resultado.context_annotations)
                        tweets.append(tweet_nuevo)
                        usuarios.append(autor)
                super(Busqueda,self).save(*args,**kwargs)
                for autor in usuarios:
                    try:
                        Autor.objects.get(id_autor=autor.id_autor)
                    except Autor.DoesNotExist:
                        autor.save(True)
                
                for tweet in tweets:
                    try:
                        Tweet.objects.get(id_tweet=tweet.id_tweet)
                    except Tweet.DoesNotExist:
                        tweet.save(True)
            elif "selenium" in fuente:
                cantidad_resultados=0
                c=searchBySelenium(usr="usaurio",pwd="clave")
                resultados = c.searchTweets(self.query,self.numero_resultados,self.reciente)
                users=[]
                usuarios =  []
                tweets = []
                if(resultados and resultados.values()):
                    for resultado in resultados.values():
                        print("REcorriendoo REsultados")
                        cantidad_resultados=cantidad_resultados + 1
                        print(resultado)
                        
                        tweet_nuevo = Tweet()
                        #conversacion = Conversacion()
                        autor = Autor()
                        autor.id_autor = resultado['user_id'] 
                        autor.nombre_usuario = resultado['username']

                        #conversacion.busqueda=self
                        tweet_nuevo.id_tweet = resultado['tweet_id']
                        tweet_nuevo.texto=resultado['content']
                        tweet_nuevo.fcreacion=resultado['posted_time']
                        tweet_nuevo.retweet=resultado['is_retweet']
                        tweet_nuevo.tweet_url=resultado['tweet_url']
                        tweet_nuevo.mentions=resultado['mentions']
                        tweet_nuevo.hashtags=resultado['hashtags']
                        
                        tweet_nuevo.megusta=resultado['likes']
                        tweet_nuevo.respuestas=resultado['replies']
                        tweet_nuevo.retweets=resultado['retweets']
                        tweet_nuevo.autor=autor
                        tweet_nuevo.busqueda=self             
                        tweets.append(tweet_nuevo)
                        usuarios.append(autor)
                        self.numero_resultados=cantidad_resultados
                    print(cantidad_resultados)
                super(Busqueda,self).save(*args,**kwargs)
                for autor in usuarios:
                    try:
                        Autor.objects.get(id_autor=autor.id_autor)
                    except Autor.DoesNotExist:
                        autor.save(True)
                
                for tweet in tweets:
                    try:
                        #buscar en repuestas del tweet
                        Tweet.objects.get(id_tweet=tweet.id_tweet)
                    except Tweet.DoesNotExist:
                        print("Guarda tweet busqueda") 
                        print(tweet.id_tweet)  
                        tweet.save(True)
                    self.tweets.add(tweet)

                #terminado de guardar ahora buscar en cada hilo
                if(self.buscar_respuestas):
                    
                    for tweet in tweets:
                        usuarios2 =  []
                        tweets2 = []
                        resultados_tweet = c.exploreTweet(url=tweet.tweet_url,tweets_count=self.numero_resultados)
                        #print(resultados_tweet)
                        for resultadot in resultados_tweet.values():
                            tweet_nuevo2 = Tweet()
                            
                            autor2 = Autor()
                            autor2.id_autor = resultadot['user_id'] 
                            autor2.nombre_usuario = resultadot['username']

                    #conversacion.busqueda=self
                            if not resultadot['tweet_id'] is None and resultadot['user_id'] == tweet.autor.id_autor:
                                tweet_nuevo2.id_tweet = resultadot['tweet_id']
                                tweet_nuevo2.texto=resultadot['content']
                                tweet_nuevo2.fcreacion=resultadot['posted_time']
                                tweet_nuevo2.retweet=resultadot['is_retweet']
                                tweet_nuevo2.tweet_url=resultadot['tweet_url']
                                tweet_nuevo2.mentions=resultadot['mentions']
                                tweet_nuevo2.hashtags=resultadot['hashtags']
                        
                                tweet_nuevo2.megusta=resultadot['likes']
                                tweet_nuevo2.respuestas=resultadot['replies']
                                tweet_nuevo2.retweets=resultadot['retweets']
                                tweet_nuevo2.autor=autor2
                                tweet_nuevo2.busqueda=self     
                                tweet_nuevo2.respuesta_de=tweet
                                        
                                tweets2.append(tweet_nuevo2)
                            usuarios2.append(autor2)
                        
                    
                            for autor2 in usuarios2:
                                try:
                                    Autor.objects.get(id_autor=autor2.id_autor)
                                except Autor.DoesNotExist:
                                    autor2.save(True)
                            print("Numero de respuestas {}".format(len(tweets2)) )
                            for tweet2 in tweets2:
                                try:
                                    Tweet.objects.get(id_tweet=tweet2.id_tweet)
                                except Tweet.DoesNotExist:
                                    tweet2.save()
                                self.tweets.add(tweet2)
                            print("termina de guardar hilo de tweet {}".format(tweet_nuevo.id_tweet) )
                            #
                #En este punto se va a controlar mensajes con texto largo que no fueron descargador por completo
                #primero de la busqueda realizada buscar los que contengan el texto ... Mostrar más
                resultado_completar= Tweet.objects.filter(busqueda=self).filter(texto__contains='… Mostrar más')
                for res in resultado_completar:
                    resultados_tweetc = c.exploreTweet(url=res.tweet_url,tweets_count=1)
                    print(resultados_tweetc)
                    actualizo=False   
                    tweet2 = list(resultados_tweetc.values())[0]
                    try:
                        if(actualizo==False):
                            print(tweet2)
                            #tweet=Tweet.objects.get(id_tweet=tweet2['tweet_id'])
                            res.texto=tweet2['content']
                            res.save()
                            actualizo=True
                    except Tweet.DoesNotExist:
                        print("No se encuentra tweet con id {}".format(tweet2['tweet_id']))
                c.close_all()
                
        except:
            print("An exception occurred") 
            traceback.print_exc()
            raise ValueError("No se pudo guardar!")


