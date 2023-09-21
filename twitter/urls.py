from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from .views import tema,index, NuevoTema, ListarTemas, ActualizaTema, DetalleTema, BusquedasPorTema,NuevaBusqueda,ResultadoBusqueda,EDAResultadoBusqueda, EDAResultadoTema


app_name = 'twitter'
urlpatterns = [
    #path('', login_required(index ), name='index'),
    #path('listar_temas/', login_required( ListarTemas.as_view() ),name='temas'),
    path('', login_required( ListarTemas.as_view() ),name='temas'),
    path('tema/nuevo/',login_required(NuevoTema.as_view()),name='crear_tema'),
    path('editar_tema/<int:pk>/',login_required(ActualizaTema.as_view()),name='editar_tema'),

    path('detalle_tema/<int:pk>/',login_required(DetalleTema.as_view()),name='detalle_tema'),
    path("busquedas/<int:id_tema>/", BusquedasPorTema.as_view(),name='busqueda_por_tema'),
    path('nueva_busqueda/<int:id_tema>/',NuevaBusqueda.as_view(),name='crear_busqueda'),
    path("resultados/<int:id_busqueda>/", ResultadoBusqueda.as_view(),name='resultado_busqueda'),
    path("resultadosEDA/<int:id_busqueda>/", EDAResultadoBusqueda.as_view(),name='resultado_eda'),
    path("temaEDA/<int:id_tema>/", EDAResultadoTema.as_view(),name='tema_eda'),
    #path("logout/", login_required( LogoutView.as_view() ), name="logout"),
]