from django.contrib import admin
from registro.models import Empresa, Colector, Plan, Formulario, PermisoFormulario 
from registro.models import Ficha, Entrada, Respuesta, FormularioDiligenciado, Tablet
from registro.models import AsignacionEntrada, ReglaVisibilidad, FormularioAsociado
# Register your models here.

class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nit', 'correo_empresarial', 'telefono','plan' )
    list_filter = ('plan',)
    search_fields = ['nombre', 'nit']
    filter_horizontal = ('colector', 'formulario', 'tablets')

class ColectorAdmin(admin.ModelAdmin):
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

class AsignacionEntradaInline(admin.TabularInline):
    model = AsignacionEntrada
    extra = 1
    

class FichaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', )    
    search_fields = ['nombre', ]
    #filter_horizontal = ('entrada',  )
    inlines = (AsignacionEntradaInline,)

class EntradaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion',  'tipo', 'id', )    
    list_filter = ('tipo',)
    search_fields = ['nombre', 'descripcion' ]
    filter_horizontal = ('respuesta',  )

class FormularioAsociadoAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('form_asociado',)}),
        (None, {'fields': (('seleccionar_existentes', 'crear_nuevo', 'actualizar_existente',  'seleccionar_multiples'),)} ),
        ('Auto Llenar Campos', {
            'classes': ('collapse', ),
            'fields': ('entrada_fuente', 'entrada_destino',)
            }),
        )    
    list_filter = ('form_asociado',)
    search_fields = ['form_asociado', ]

class ReglaVisibilidadAdmin(admin.ModelAdmin):
    list_filter = ['visibilizar__ficha__entrada']
    search_fields = ['valor', ]

class RespuestaAdmin(admin.ModelAdmin):
    list_display = ('valor', 'id', )
    search_fields = ['valor', ]

class FormularioDiligenciadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'empresa',  'gps', 'fecha_creacion' )    
    list_filter = ('empresa',)
    search_fields = ['nombre', 'empresa',  ]

class PermisoFormularioAdmin(admin.ModelAdmin):
    list_display = ('formulario',)    
    list_filter = ('colectores',)
    search_fields = ['formulario', 'colectores',  ]
    filter_horizontal = ('colectores',  )



    

admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Colector, ColectorAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Formulario, FormularioAdmin)
admin.site.register(Ficha, FichaAdmin)
admin.site.register(Entrada, EntradaAdmin)
admin.site.register(ReglaVisibilidad, ReglaVisibilidadAdmin)
admin.site.register(FormularioAsociado, FormularioAsociadoAdmin)
admin.site.register(Respuesta, RespuestaAdmin)
admin.site.register(FormularioDiligenciado, FormularioDiligenciadoAdmin)
admin.site.register(Tablet)
admin.site.register(PermisoFormulario, PermisoFormularioAdmin)
