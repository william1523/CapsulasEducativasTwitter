from django.forms import ModelForm, Textarea, TextInput, NumberInput,HiddenInput,CheckboxInput
from datetime import datetime
from .models import Tema, Busqueda

#formularios para temas
class TemaForm(ModelForm):
    class Meta:
        model = Tema
        fields = ('tema','descripcion','contexto')
        widgets = {
            'tema':TextInput(
            attrs={
                "placeholder": "Tema",
                "class": "form-control"
                }
            ),
            'descripcion':Textarea(
            attrs={
                "placeholder": "Descripción del Tema",
                "class": "form-control",
                'rows': 3
                }
            ),
            'contexto':Textarea(
            attrs={
                "placeholder": "Contexto para cápsula educativa, ejm: debe promover empatía, y ser comprensible para niños de 6 años...",
                "class": "form-control",
                'rows': 3
                }
            )
        }

#formularios para busquedas
#   
class BusquedaForm(ModelForm):
    class Meta:
        model = Busqueda
        fields = ('tema','query','descripcion','numero_resultados','reciente','buscar_respuestas','numero_respuestas')
        widgets = {
            'tema':HiddenInput(
            attrs={
                #"placeholder": "Query USAR OPERADORES DE API TWIITER",
                "class": "form-control"
                }
            ),
            'query':TextInput(
            attrs={
                "placeholder": "Ejm: (#ciberbullying) lang:es -filter:links -filter:replies",
                "class": "form-control form-control-sm"
                }
            ),
            'descripcion':Textarea(
            attrs={
                "placeholder": "Descripción de la busqueda realizada",
                "class": "form-control",
                'rows': 3
                }
            ),
            'numero_resultados':NumberInput(
            attrs={
                "placeholder": "Cantidad de tweets",
                "class": "form-control form-control-sm"
                }
            ),
            'reciente':CheckboxInput(
            attrs={
                
                }
            ),
            'buscar_respuestas':CheckboxInput(
            attrs={
                
                }
            ),
            'numero_respuestas':NumberInput(
            attrs={
                "placeholder": "Cantidad de respuestas por tweet",
                "class": "form-control form-control-sm"
                }
            ),
        }
        labels = {
            # many other fields
			'numero_resultados':'Cantidad de tweets a recuperar',
            'reciente':'Buscar en tweets recientes',
            'query':'Texto de busqueda',
            'descripcion':'Descripción de busqueda a realizar',
            'buscar_respuestas':'Incluir respuestas'
        
        }
        
        
        
         