from django.shortcuts import render

# Create your views here.
from .forms import InicioSesionForm
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

def InicioSesionView(request):
    form = InicioSesionForm(request.POST or None)
    msg=None
    if request.method == "POST":
        if form.is_valid():
            usuario = form.cleaned_data.get("username")
            clave = form.cleaned_data.get("password")
            user = authenticate(username=usuario, password=clave)
            if user is not None:
                login(request,user)
                return redirect("/")
            else:
                msg = 'Credenciales Incorrectas'
        else:
            msg = 'Revise los datos proporcionados'
    return render(request,"paginas/login.html",{"form": form, "msg": msg})

def finalizarSesion(request):
    logout(request)
    return HttpResponseRedirect( reverse_lazy('autentication:login') )
