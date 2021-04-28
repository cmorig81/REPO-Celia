from django.db import models

# Create your models here.

class Hotel(models.Model):
    nombre = models.CharField(max_length=50)
    num_plantas= models.IntegerField(default=0)
    
    def __str__(self):
        return f'Hotel {self.nombre}'

    def serializate(self):
        dic = {}
        dic['nombre'] = self.nombre
        dic['num_plantas'] = self.num_plantas
        
        return dic

# HOTEL
class Planta(models.Model):
    numero = models.IntegerField(default=0)
    hab_desde = models.IntegerField(default=0)
    hab_hasta = models.IntegerField(default=0)
    fk_hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    def __str__(self):
        return f'Planta número: {self.numero} de {self.fk_hotel}'

    def serializate(self):
        dic = {}
        dic['numero'] = self.numero
        dic['hab_desde'] = self.hab_desde
        dic['hab_hasta'] = self.hab_hasta
        dic['fk_hotel'] = self.fk_hotel.id

        return dic

class Sala(models.Model):
    nombre = models.CharField(max_length=200)
    aforo = models.IntegerField(default=0)
    abierto = models.BooleanField(default=False)
    color = models.CharField(max_length=15)
    #--> estado actual (lista)
    fk_planta = models.ForeignKey(Planta, on_delete=models.CASCADE)

    def __str__(self):
        return f'Nombre sala: {self.nombre} de {self.fk_planta}'


    def serializate(self):
        dic = {}
        dic['nombre'] = self.nombre
        dic['aforo'] = self.aforo
        dic['abierto'] = self.abierto
        dic['color'] = self.color
        dic['fk_planta'] = self.fk_planta.id

        return dic
    

class SalaContigua(models.Model):
    fk_sala_orig = models.ForeignKey(Sala, related_name='SalaOrig', on_delete=models.CASCADE)
    fk_sala_contigua = models.ForeignKey(Sala, related_name='SalaContigua', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.fk_sala_contigua.fk_planta.fk_hotel}: La sala: {self.fk_sala_contigua.nombre} es contigua a la sala {self.fk_sala_orig.nombre}'

class EstadoActualSala(models.Model):
    fk_sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    persona = models.IntegerField(default=0)
    
    def __str__(self):
        return f'La sala: {self.fk_sala.nombre} de {self.fk_sala.fk_planta} tiene a la persona {self.persona} <br>'

    def serializate(self):
        dic = {}
        dic['fk_sala'] = self.fk_sala.serializate()
        dic['persona'] = self.persona
        
        return dic

'''
Tabla EstadoActual:
    fk_sala         persona
    -------         -------
    Cafeteria           4
    Cafeteria           9
'''