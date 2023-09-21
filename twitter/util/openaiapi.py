import os
import openai
from decouple import config


  

class openai_api:
  #os.getenv("OPENAI_API_KEY")  
  openai.api_key = '' #introducir OPENAI_API_KEY
  

  def generarCapsula(self, contexto:str, palabras:str ):
    envio="""Crear un guion para un video de una capsula educativa, toma en cuenta el contexto y usa las palabras indicadas 
    contexto: {}
    palabras: {}
    """.format(contexto,palabras)
    print(len(envio))
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=envio,
    temperature=0,
    max_tokens=3000,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
    )
    print(response)
    return response
  