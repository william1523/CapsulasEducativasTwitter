from django import forms
#from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User

class InicioSesionForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
        attrs={
            "placeholder": "Usuario",
            "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
        attrs={
            "placeholder":"contraseñas",
            "class":"form-control "
            }
        )
    )