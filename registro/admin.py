from django.contrib import admin
from registro.models import Empresa, Colector, Plan, Formulario, PermisoFormulario
from registro.models import Ficha, Entrada, Respuesta, FormularioDiligenciado, Tablet
# Register your models here.

class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nit', 'correo_empresarial', 'telefono','plan' )
    list_filter = ('plan',)
    search_fields = ['nombre', 'nit']
    filter_horizontal = ('colector', 'formulario', 'tablets')

class Colectordmin(admin.ModelAdmin):
    list_display = ('get_nombre', 'get_email'  )
    search_fields = ['usuario__username']

    def get_nombre(self, obj):
    	return obj.usuario.username

    def get_email(self, obj):
    	return obj.usuario.email

    get_nombre.short_description = 'usuario'
    get_email.short_description = 'email'
    
class PlanAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'almacenamiento', 'cantidad_colectores', 'valor','activo', 'fecha_creacion', )
	list_filter = ('nombre', 'activo',)
	search_fields = ['nombre', 'fecha_creacion',]
    

class FormularioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', )    
    search_fields = ['nombre', ]
    filter_horizontal = ('ficha',  )

class FichaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', )    
    search_fields = ['nombre', ]
    filter_horizontal = ('entrada',  )

class EntradaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion',  'tipo' )    
    list_filter = ('tipo',)
    search_fields = ['nombre', 'descripcion' ]
    filter_horizontal = ('respuesta',  )

class RespuestaAdmin(admin.ModelAdmin):
    list_display = ('nombre', )
    search_fields = ['nombre', ]

class FormularioDiligenciadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'empresa',  'gps', 'fecha_creacion' )    
    list_filter = ('empresa',)
    search_fields = ['nombre', 'empresa',  ]
    

admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Colector, Colectordmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Formulario, FormularioAdmin)
admin.site.register(Ficha, FichaAdmin)
admin.site.register(Entrada, EntradaAdmin)
admin.site.register(Respuesta, RespuestaAdmin)
admin.site.register(FormularioDiligenciado, FormularioDiligenciadoAdmin)
admin.site.register(Tablet)
admin.site.register(PermisoFormulario)
