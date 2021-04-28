from django.urls import path

from . import views

urlpatterns = [
    #path('', views.jueves, name='jueves'),
    #path('jueves', views.jueves, name='jueves'),
    path('inicio', views.inicio, name='inicio'),
    path('gestion_Hotel', views.gestion_Hotel, name='gestion_Hotel'),
    #path('datosSala', views.datosSala, name='datosSala'),
    #path('datosSalaCafeteria', views.datosSalaCafeteria, name='datosSalaCafeteria'),
    #path('datosSalaNueva/<str:nombre>', views.datosSalaNueva, name='datosSalaNueva'),
    path('datosHotel', views.datosHotel, name='datosHotel'),
    path('datosSalasHotel', views.datosSalasHotel, name='datosSalasHotel'),
    path('consulta', views.consulta, name='consulta')
]