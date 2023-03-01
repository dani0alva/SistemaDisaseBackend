from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Paciente)
admin.site.register(Empresa)
admin.site.register(Diagnostico)
admin.site.register(Usuario)
admin.site.register(Disase)