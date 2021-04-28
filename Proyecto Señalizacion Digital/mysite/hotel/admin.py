from django.contrib import admin
from .models import Planta, Sala, SalaContigua, EstadoActualSala, Hotel
#from .models import Planta
# Register your models here.
#admin.site.register(Question)
#admin.site.register(Choice)
admin.site.register(Planta)
admin.site.register(Sala)
admin.site.register(SalaContigua)
admin.site.register(EstadoActualSala)
admin.site.register(Hotel)