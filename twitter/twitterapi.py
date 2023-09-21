from tweepy import Client

class BusquedaTwitter:
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAK9DdAEAAAAAJfB1kLLmRKaoPvPoLqX3SZ1Wv8w%3DU4E8mJOTGC3p86OhHInxvkmSb6T2p075fKyfXr7ubQepodUPbP"
    #"AAAAAAAAAAAAAAAAAAAAAK9DdAEAAAAAdK4a1JuLWsy9eWpnqIPOkxTxZHg%3D9uLSVN5MbMfTZjk3SJPnCrest9syAJD5oDBVqMsNFR6xKMS7tZ"
    #"AAAAAAAAAAAAAAAAAAAAAK9DdAEAAAAAJfB1kLLmRKaoPvPoLqX3SZ1Wv8w%3DU4E8mJOTGC3p86OhHInxvkmSb6T2p075fKyfXr7ubQepodUPbP"
    client = Client(bearer_token=bearer_token)
    def busqueda(self,query, resultados):
        #query = '(abusoescolar OR abuso) lang:es '
        response =  self.client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at','public_metrics','conversation_id','possibly_sensitive','lang'], expansions=["attachments.media_keys", "author_id","geo.place_id"], place_fields=["contained_within", "country", "country_code", "full_name", "geo", "id", "name", "place_type"], max_results=resultados)
        imprime = False
        #for tweet in response.data:
        #    if( not imprime):
        #       print('dir tweet')
        #       print(dir(tweet))
        #       print('dir tweet/data')
        #       print(dir(tweet['data']))
        #       imprime = True
        #imprime = False
        #for tweet in response.includes:
        #    if( not imprime):
        #       print('dir include')
        #       print(tweet)
        #       imprime = True


        print(response)
        return response
   