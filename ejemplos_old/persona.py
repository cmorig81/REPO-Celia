class Persona(object):

    def __init__(self, dni:str, nombre:str, apellido:str, fecha_nacimiento:str, direccion:list):
        self.dni=dni
        self.nombre=nombre
        self.apellido=apellido
        self.fecha_nacimiento=fecha_nacimiento
        self.direccion=direccion
    
    def getNombreCompleto(self):
        return self.nombre + ' ' + self.apellido
    
    def getDia(self):
        # dia-mes-año
        if self.fecha_nacimiento.find("-") != -1:
            indice=self.fecha_nacimiento.find("-")
            dia=self.fecha_nacimiento[0:indice]
            return dia
        else:
            print("Formato no válido de fecha")

    def getMes(self):
        indice_1=self.fecha_nacimiento.find("-")
        indice_2=self.fecha_nacimiento.rfind("-")
        mes=self.fecha_nacimiento[indice_1+1:indice_2]
        return mes

    def getAño(self):
        indice=self.fecha_nacimiento.rfind("-")
        año=self.fecha_nacimiento[indice+1:]
        return año

    def setDia(self, dia):
        indice=self.fecha_nacimiento.find("-")
        nueva_fecha=str(dia) + '-' + self.fecha_nacimiento[indice+1:]
        self.fecha_nacimiento=nueva_fecha

persona_1=Persona('123123123P', 'Pepe', 'Perez', '22-11-2000', 'Calle Valladolid')

print(persona_1.getDia())
print(persona_1.getMes())
print(persona_1.getAño())
dia=input("Introduzca un nuevo valor para el campo Día: ")
persona_1.setDia(dia)
print(persona_1.fecha_nacimiento)