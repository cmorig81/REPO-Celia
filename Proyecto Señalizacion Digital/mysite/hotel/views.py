# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from .models import Sala, EstadoActualSala, Planta, SalaContigua, Hotel
from django.db import connection
import random
import time
#from .urls import urlpatterns

from django.contrib.auth import (login as auth_login,  authenticate)
from django.http import HttpResponseRedirect
import threading
import time

def worker_pos():
    """thread worker function"""
    x = 0
    while True:
        x += 1
        print(f'({str(x)}) : sensor working...')
        time.sleep(10)
        activarSensorPositivo('Cafetería', 'Mirador')
        #activarSensorNegativo('Mirador')
        #time.sleep(10)

def worker_neg():
    x=0
    while True:
        x+=1
        time.sleep(10)
        activarSensorNegativo('Mirador')

#threads=[]
t_pos = threading.Thread(target = worker_pos)
#threads.append(t_pos)
t_pos.start()

t_neg = threading.Thread(target = worker_neg)
#threads.append(t_neg)
t_neg.start()

#Función sensor que genera un número aleatorio: el número máximo del randint dependerá del aforo total del hotel
def sensor():
    return random.randint(1,20)

def activarSensorNegativo(nombre_hotel):
    persona=sensor()
    print("Estamos en sensor NEGATIVO y la persona generada es ", persona, "\n")
    obj_hotel=Hotel.objects.get(nombre=nombre_hotel)
    lista_obj_plantas=Planta.objects.filter(fk_hotel=obj_hotel.id)
    lista_obj_salas=Sala.objects.all()

    for planta in lista_obj_plantas:
        for sala in lista_obj_salas:
            if sala.fk_planta_id == planta.id:
                print("SENSOR NEGATIVO: Sala ", sala.nombre)
                #Comprobamos si ahí está la persona y , en caso afirmativo, la descontamos
                obj=EstadoActualSala.objects.filter(fk_sala=sala, persona=persona)
                print(obj)
                if obj:
                    #Descontamos la persona de esa sala , y asumimos que no va a estar esa misma persona en ese mismo
                    #instante en cualquier otra sala
                    obj.delete()
                    break

def activarSensorPositivo(nombre_sala, nombre_hotel):

    persona = sensor()
    print("Se ha generado la persona ", persona)
    obj_hotel=Hotel.objects.get(nombre=nombre_hotel)
    lista_obj_plantas=Planta.objects.filter(fk_hotel=obj_hotel.id)
    
    lista_obj_salas=Sala.objects.filter(nombre=nombre_sala)
    #Buscamos la sala concreta del hotel actual, ya que podría haber dos salas con el mismo nombre en hoteles distintos
    encontrado=False
    for sala in lista_obj_salas:
        for planta in lista_obj_plantas:
            if sala.fk_planta_id==planta.id:
                encontrado=True
                obj_sala=sala
                break

    lista_obj_estadoactualsala = EstadoActualSala.objects.filter(fk_sala=obj_sala.id)

    if len(lista_obj_estadoactualsala) < obj_sala.aforo:
        repetido=False
        for obj in lista_obj_estadoactualsala:
            if obj.persona == persona:
                repetido=True
        if not repetido:
            #obj=EstadoActualSala.objects.create(fk_sala_id=obj_sala.id, persona=persona)
            contar_persona(persona, obj_sala, nombre_hotel)
    return lista_obj_estadoactualsala

def contar_persona(persona, obj_sala, nombre_hotel):
    '''
    Funcion que agrega una persona en la sala actual siempre que esa persona no exista en ninguna otra sala del hotel o bien que , si 
    existe, sea una sala contigua a la sala actual, en cuyo caso se descontará de la otra sala 
    '''
    lista_salas_hotel=[]

    obj_hotel=Hotel.objects.get(nombre=nombre_hotel)
    lista_obj_plantas=Planta.objects.filter(fk_hotel=obj_hotel.id)
    lista_obj_salas=Sala.objects.all()

    for planta in lista_obj_plantas:
        for sala in lista_obj_salas:
            if sala.fk_planta_id==planta.id:
                lista_salas_hotel.append(sala)

    #Ahora recorremos la lista de las salas y vemos si alguna tiene a "persona"
    persona_existente=False
    for sala in lista_salas_hotel:
        print('Recorriendo lista_salas_hotel: ', sala)
        lista_obj_estadoactualsala = EstadoActualSala.objects.filter(fk_sala=sala.id)
        for ocupacion in lista_obj_estadoactualsala:
            if ocupacion.persona == persona:
                persona_existente=True
                #Ver qué sala es
                #Si se trata de la misma sala que la actual, entonces no hacemos nada
                if sala.nombre==obj_sala.nombre:
                    #no hacemos nada
                    print('La persona se encuentra ya en la sala actual , no hacemos nada')
                else:
                    #Si sala y obj_sala son contiguas (hay dos posibles combinaciones)
                    lista_obj_SalaContigua_1 = SalaContigua.objects.filter(fk_sala_orig=sala.id, fk_sala_contigua=obj_sala.id)
                    lista_obj_SalaContigua_2 = SalaContigua.objects.filter(fk_sala_orig=obj_sala.id, fk_sala_contigua=sala.id)
                    print('Lista sala contigua 1 ', lista_obj_SalaContigua_1)
                    print('Lista sala contigua 2 ', lista_obj_SalaContigua_2)
                    
                    if (not lista_obj_SalaContigua_1) and (not lista_obj_SalaContigua_2):
                        #No son salas contiguas, así que no hacemos nada
                        print('No son salas contiguas, no hacemos nada')
                    else:
                        #Son salas contiguas, por tanto, hay que descontar primero la persona de la otra sala y luego añadirla a la sala actual
                        print('Sí son salas contiguas, tenemos que descontar persona de la otra sala')
                        obj=EstadoActualSala.objects.filter(fk_sala=sala.id, persona=persona)
                        obj.delete()
                        obj=EstadoActualSala.objects.create(fk_sala=obj_sala, persona=persona)

    if not persona_existente:
        obj=EstadoActualSala.objects.create(fk_sala=obj_sala, persona=persona)


def datosHotel(request):
    hotel=''
    msg=''
    lista=[]
    dic={}
    lista_hotel=Hotel.objects.all()
    if request.method=='POST':
        msg='Estamos en post'
        print('EN POST')
        #hotel=request.POST['hotel']
        hotel=request.POST['lista_hotel']
        print('El nombre del hotel es ', hotel)
        print(hotel)

        lista=listaSalasHotel(hotel)
        dic=estadoActualSalas(lista)
        datos = {
                'hotel': hotel,
                'msg': msg,
                'lista': lista,
                'dic': dic
            }
        #return render(request, 'hotel/datosSalasHotel.html', datos)
        return datosSalasHotel(request, datos)
        #return HttpResponse(1)
    datos = {
                'hotel': hotel,
                'lista_hotel': lista_hotel,
                'msg': msg
            }
    if request.method=='GET':
        msg='Estamos en get'
        print('EN GET')
        return render(request, 'hotel/datosHotel.html', datos)

def listaSalasHotel(nombre_hotel):
    lista=[]
    obj_hotel=Hotel.objects.get(nombre=nombre_hotel)
    #print(obj_hotel)
    lista_obj_plantas=Planta.objects.filter(fk_hotel=obj_hotel.id)
    lista_obj_salas=Sala.objects.all()
    for sala in lista_obj_salas:
        for planta in lista_obj_plantas:
            if sala.fk_planta_id==planta.id:
                obj_sala=sala
                lista.append(obj_sala)
                #lista_obj_estadoactualsala = EstadoActualSala.objects.filter(fk_sala=obj_sala.id)
    return lista

def listaSalasHotel_serializar(nombre_hotel):
    lista=[]
    obj_hotel=Hotel.objects.get(nombre=nombre_hotel)
    #print(obj_hotel)
    lista_obj_plantas=Planta.objects.filter(fk_hotel=obj_hotel.id)
    lista_obj_salas=Sala.objects.all()
    for sala in lista_obj_salas:
        for planta in lista_obj_plantas:
            if sala.fk_planta_id==planta.id:
                obj_sala=sala
                lista.append(obj_sala.serializate())
                #lista_obj_estadoactualsala = EstadoActualSala.objects.filter(fk_sala=obj_sala.id)
    return lista




def estadoActualSalas(lista):
    dic={}
    for obj_sala in lista:
        dic[obj_sala.nombre] = EstadoActualSala.objects.filter(fk_sala=obj_sala.id)
    #print(dic)

    return dic

def estadoActualSalas_serializar(lista):
    dic={}
    for obj_sala in lista:
        dic[obj_sala.nombre] = EstadoActualSala.objects.filter(fk_sala=obj_sala.id)
        lista = []
        for i in dic[obj_sala.nombre]:
            lista.append(i.serializate())
        dic[obj_sala.nombre] = lista
    #print(dic)
    
    return dic

import json
from django.http import JsonResponse

def consulta(request):
    lista=listaSalasHotel('Mirador')
    dic=estadoActualSalas_serializar(lista)
    lista2=listaSalasHotel_serializar('Mirador')
    datos = {
        'estadoActualSalas':dic,
        'listaSalasHotel':lista2
    }
    print(datos)
    json_obj = json.dumps(datos)
    
    #return JsonResponse(json_obj)
    return HttpResponse(json_obj, content_type='application/json')


def datosSalasHotel(request, datos):
    return render(request, 'hotel/datosSalasHotel.html', datos)



def inicio(request):
    if request.method=='POST':
        pass
    if request.method=='GET':
        pass
    msg='Señalizacion Digital'
    datos = {
                'msg': msg
            }
    return render(request, 'hotel/inicio.html', datos)

  
def gestion_Hotel(request):
    msg='Hola que tal'
    lista_hotel=Hotel.objects.all()
    datos = {
            'msg': msg,
            'lista_hotel': lista_hotel
            }
    #if request.method='POST':
    #    pass
    
    return render(request, 'hotel/gestion_Hotel.html', datos)    
    