import traceback
from typing import Any, Dict
from django.shortcuts import render,get_object_or_404
# Create your views here.
from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.views.generic import CreateView,ListView, UpdateView, DetailView
from django.views.generic.edit import FormMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .models import Tema, Busqueda, Tweet
from .forms import TemaForm, BusquedaForm
from .util.process_tweets import process_tweets



def error_404(request, exception):
    return render(request,'paginas/page-404.html')

def error_403(request, exception):
    return render(request,'paginas/page-403.html')

def error_500(request):
    return render(request,'paginas/page-403.html')


@login_required(login_url="/login/")
def index(request):
    template = loader.get_template('paginas/index.html')
    context = {
         
    }
    return HttpResponse(template.render(context,request))

def temas(request):
    temas = Tema.objects.order_by('-fcreacion')
    template = loader.get_template('paginas/Temas/temas.html')
    context = {
        'temas': temas 
    }
    salida = ', '.join([t.tema for t in temas])
    return HttpResponse(template.render(context,request))

@login_required(login_url="/login")
def tema(request, id_tema):
    try:
        tema = Tema.objects.get(pk=id_tema)
        form = TemaForm(request.POST or None)
    except Tema.DoesNotExist:
        raise Http404("Tema no existe")
    return render(request, 'paginas/temas/tema.html' , {'tema':tema, 'form':form})


class NuevoTema(CreateView):
    model = Tema
    form_class = TemaForm
    template_name ='paginas/Temas/crear_tema.html'
    success_url = reverse_lazy('twitter:temas')
    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super(NuevoTema, self).form_valid(form)

class NuevaBusqueda(CreateView):
    model = Busqueda
    form_class = BusquedaForm
    template_name ='paginas/Busquedas/crear_busqueda.html'
   
    #def get_initial(self):
    #    print(self.kwargs)
    #    self.tema = get_object_or_404(Tema, id=self.kwargs["id_tema"])
    #    return super.get_initial()
    
    def form_valid(self, form):
        print("Form Valid")
        form.instance.autor = self.request.user
        print("Form user")
        self.tema = get_object_or_404(Tema, id=self.kwargs["id_tema"])
        print(self.tema)
        form.instance.tema = self.tema
        return super(NuevaBusqueda, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        print("Context Data")
        print(**kwargs)
        context = super().get_context_data(**kwargs)
        context['segment'] ='busqueda'
        self.tema = get_object_or_404(Tema, id=self.kwargs["id_tema"])
        context['form'] = BusquedaForm(initial={'tema':self.tema})
        context['id_tema'] = self.kwargs["id_tema"]
        print('return context')
        return context
    
    def get_success_url(self):
        return reverse_lazy('twitter:resultado_busqueda', kwargs={'id_busqueda': self.object.pk})

class ActualizaTema(UpdateView):
    model = Tema
    form_class = TemaForm
    template_name ='paginas/Temas/editar_tema.html'
    success_url = reverse_lazy('twitter:temas')


class ListarTemas(ListView):
    model= Tema
    template_name='paginas/Temas/temas.html'
    context_object_name='temas'
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] ='listar_temas'
        return context

class BusquedasPorTema(ListView):
    paginate_by = 5
    template_name = 'paginas/Busquedas/busquedas_por_tema.html'
    model = Busqueda
    context_object_name='Busquedas'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["tema"]=self.tema
        return context

    def get_queryset(self):
        print(self.kwargs)
        self.tema = get_object_or_404(Tema, id=self.kwargs["id_tema"])
        print(self.tema)
        print(Busqueda.objects.filter(tema=self.tema))
        return Busqueda.objects.filter(tema=self.tema)

class ResultadoBusqueda(ListView):
    paginate_by = 10
    template_name = 'paginas/Resultados/resultados_busqueda.html'
    model = Tweet
    context_object_name='resultados'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["tema"]=self.tema
        context["busqueda"]=self.busqueda
        return context

    def get_queryset(self):
        print("get_queryset==")
        print(self.kwargs)
        print(self.kwargs["id_busqueda"])
        self.busqueda = get_object_or_404(Busqueda, id=self.kwargs["id_busqueda"])
        print(self.busqueda)
        self.tema = self.busqueda.tema
        print(self.tema)
        p = process_tweets()
        print(p.preprocesar_tweets(self.kwargs["id_busqueda"]))
        print("dataframe busquedas")

        #p = process_tweets()
        #print(p.getTweets(self.kwargs["id_busqueda"]))
        return Tweet.objects.filter(busqueda=self.busqueda)

class EDAResultadoBusqueda(ListView):
    paginate_by = 10
    template_name = 'paginas/Resultados/resultados_eda.html'
    model = Tweet
    context_object_name='resultados'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["tema"]=self.tema
        context["busqueda"]=self.busqueda
        context["imgb64"]=self.imgb64
        context["json"]=self.json
        return context

    def get_queryset(self):
        print("get_queryset==")
        print(self.kwargs)
        print(self.kwargs["id_busqueda"])
        self.busqueda = get_object_or_404(Busqueda, id=self.kwargs["id_busqueda"])
        print(self.busqueda)
        self.tema = self.busqueda.tema
        print(self.tema)
        print("dataframe busquedas")

        p = process_tweets()
        print(p.getTweets(self.kwargs["id_busqueda"]))
        print("Genera imagen b64")
        try:
            self.imgb64 = p.getwordcloud()
            self.json = p.ldaModel()
            print(p.topWords())
            #print(self.imgb64)
        except:
            print("An exception occurred")
            traceback.print_exc()

        return Tweet.objects.filter(busqueda=self.busqueda)

class EDAResultadoTema(ListView):
    paginate_by = 10
    template_name = 'paginas/Resultados/tema_eda.html'
    model = Tweet
    context_object_name='resultados'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["tema"]=self.tema
        #context["busqueda"]=self.busqueda
        context["imgb64"]=self.imgb64
        context["json"]=self.json
        context["json_1"]=self.json_1 
        context["json_2"]=self.json_2
        context["json_3"]=self.json_3
        context["json_4"]=self.json_4
        context["texto_guion"]=self.texto_guion

        return context

    def get_queryset(self):
        print(self.kwargs)
        #print(self.kwargs["id_busqueda"])
        self.tema = get_object_or_404(Tema, id=self.kwargs["id_tema"])
        p = process_tweets()
        print(p.getTweetsTema(self.kwargs["id_tema"]))
        print("Genera imagen b64")
        try:
            self.imgb64 = p.getwordcloud()
            self.json = p.ldaModel()
            self.json_1 = p.json_coherencia
            print(p.topWords())
            self.json_2 = p.json_topwords
            self.json_3 = p.json_topbigramas
            self.json_4 = p.json_hashtags
            self.texto_guion=p.generar_guion()
            #print(self.imgb64)
        except:
            print("An exception occurred")
            traceback.print_exc()
        busquedas = Busqueda.objects.filter(tema=self.tema)    
        print("Luego de pasar por busquedas :D ")

        return Tweet.objects.filter(busqueda__in=busquedas)

class DetalleTema(FormMixin,DetailView):
    model = Tema
    template_name='paginas/Temas/detalle_tema.html'
    context_object_name='tema'
    form_class= BusquedaForm

    def get_success_url(self):
        return reverse_lazy('twitter:temas')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] ='detalle_tema'
        context['form'] = BusquedaForm(initial={'tema':self.object})
        return context
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.autor = self.request.user
        form.save()
        return super(DetalleTema, self).form_valid(form)
    
