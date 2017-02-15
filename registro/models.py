#! -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
# from sortedm2m.fields import SortedManyToManyField
# Create your models here.


class Empresa(models.Model):
    """
    Entidad que agrupa colectorios con formularios y dispositivos
    """
    usuario = models.OneToOneField(User)
    codigo_secreto = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50, blank=True, unique=True)
    industria = models.CharField(max_length=50, blank=True)
    pais = models.CharField(max_length=50, blank=True)
    ciudad = models.CharField(max_length=50, blank=True)
    correo_empresarial = models.TextField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    descripcion = models.TextField(max_length=50, blank=True)
    nit = models.IntegerField(blank=True, null=True)
    correo_facturacion = models.CharField(max_length=50, blank=True, unique=True)
    telefono = models.IntegerField(blank=True, null=True)
    plan = models.ForeignKey('Plan', null=True, blank=True)
    colector = models.ManyToManyField('Colector', blank=True)
    formulario = models.ManyToManyField('Formulario', blank=True)
    tablets = models.ManyToManyField('Tablet', blank=True)

    def __unicode__(self):
        return self.nombre


class Tablet(models.Model):
    """
    Identificador para tabletas
    """
    codigo = models.CharField(max_length=50, blank=True, unique=True)

    def __unicode__(self):
        return self.codigo 


class Colector(models.Model):
    """
    Usuario del sistema que está asociado a una empresa y puede diligenciar formularios
    """
    usuario = models.OneToOneField(User, blank=True)
    respuesta = models.ManyToManyField('Respuesta', blank=True)

    def __unicode__(self):
        return self.usuario.username


class Plan(models.Model):
    """
    Entidad para el manejo de planes de recolección. Actualmente no está en uso
    """
    nombre = models.CharField(max_length=50, blank=True, unique=True)
    almacenamiento = models.CharField(max_length=50, blank=True, unique=True)
    cantidad_colectores = models.IntegerField(blank=True, unique=True)
    valor = models.CharField(max_length=50, blank=True, unique=True)
    activo = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.nombre

SI = 'SI'
NO = 'NO'
IF_CHOICES = (
        (SI, 'SI'),
        (NO, 'NO'),
    )


class Formulario(models.Model):
    """
    Entidad principal de agrupamiento. Una empresa tiene varios formularios
    """
    nombre = models.CharField(max_length=50, blank=True, unique=False)
    descripcion = models.TextField(max_length=100, blank=True)
    ficha = models.ManyToManyField('Ficha', blank=True)
    # precargado = models.CharField(max_length=2, choices=IF_CHOICES, default=NO)
    titulo_reporte = models.ForeignKey(
        'Entrada',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    titulo_reporte2 = models.ForeignKey(
        'Entrada',
        related_name='tituloreporte2',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    
    def __unicode__(self):
        return self.nombre


class PermisoFormulario(models.Model):
    """
    Regla de visibilidad de formularios para colectores. Únicamente los colectores relacionados en esta relación
    con los formularios podrán llenar los formularios
    """
    formulario = models.ForeignKey('Formulario')
    colectores = models.ManyToManyField('Colector')

    def __unicode__(self):
        return self.formulario.nombre


class Ficha(models.Model):
    """
    Entidad de separación de los formularios. Un formulario está compuesto por muchas fichas
    """
    nombre = models.CharField(max_length=50, blank=True, unique=False)
    descripcion = models.TextField(max_length=100, blank=True)
    # entrada = SortedManyToManyField('Entrada')
    # entrada = models.ManyToManyField('Entrada',through='AsignacionEntrada',blank=True)
    entrada = models.ManyToManyField('Entrada', through='AsignacionEntrada', blank=True)
    repetible = models.BooleanField(default=False)

    class Meta:
        ordering = ('id',)
    
    def __unicode__(self):
        return self.nombre

"""
Tipos de preguntas
"""
TEXTO = '1'
PARRAFO = '2'
OPCION = '3'
UNICA = '4'
MULTIPLE = '5'
FOTO = '6'
FECHA = '7'
NUMERO = '8'
SCAN = '9'
DINAMICA = '10'
DINAMICAMULTIPLE = '11'
GPS = '12'
FORMULA = '13'
FIRMA = '14'
DECIMAL = '15'
DOCUMENTO = '16'
TIEMPO = '17'
ENTRADA_CHOICES = (
        (TEXTO, 'TEXTO'),
        (PARRAFO, 'PARRAFO'),
        (OPCION, 'OPCION'),
        (UNICA, 'UNICA'),
        (MULTIPLE, 'MULTIPLE'),
        (FOTO, 'FOTO'),
        (FECHA, 'FECHA'),
        (NUMERO, 'NUMERO'),
        (SCAN, 'SCAN'),
        (DINAMICA, 'DINAMICA UNICA'),
        (DINAMICAMULTIPLE, 'DINAMICA MULTIPLE'),
        (GPS, 'GPS'),
        (FORMULA, 'FORMULA'),
        (FIRMA, 'FIRMA'),
        (DECIMAL, 'DECIMAL'),
        (DOCUMENTO, 'DOCUMENTO'),
        (TIEMPO, 'TIEMPO'),
        
    )


class Entrada(models.Model):
    """
    Entidad central de respuesta. Relaciona un nombre de pregunta con un tipo de pregunta
    """
    tipo = models.CharField(max_length=2, choices=ENTRADA_CHOICES, default=TEXTO)
    nombre = models.CharField(max_length=500, blank=True, unique=False)
    descripcion = models.TextField(max_length=100, blank=True)
    respuesta = models.ManyToManyField('Respuesta', blank=True)

    class Meta:
        ordering = ('id',)
    
    # precargado = models.CharField(max_length=2, choices=REQUIRED_CHOICES, default=NO)

    def __unicode__(self):
        return self.nombre


class AsignacionEntrada(models.Model):
    """
    Relaciona la visibilidad de una entrada dentro de una ficha de un formulario
    """
    ficha = models.ForeignKey(Ficha, on_delete=models.CASCADE)
    entrada = models.ForeignKey(Entrada, on_delete=models.CASCADE)
    orden = models.PositiveIntegerField()
    requerido = models.BooleanField(default=False)
    oculto = models.BooleanField(default=False)
    solo_lectura = models.BooleanField(default=False)
    agregar_nuevo = models.BooleanField(default=False)
    defecto = models.CharField(max_length=50, blank=True, unique=False)
    defecto_previo = models.BooleanField(default=False)
    maximo = models.PositiveIntegerField(blank=True, null=True)
    minimo = models.PositiveIntegerField(blank=True, null=True)
    validacion = models.CharField(max_length=50, blank=True, unique=False)

    regla_visibilidad = models.ForeignKey(
        'ReglaVisibilidad',
        related_name='visibilizar',
        blank=True,
        null=True,
        unique=False
    )

    formulario_asociado = models.ForeignKey(
        'FormularioAsociado',
        related_name='formasociado',
        blank=True,
        null=True,
        unique=False
    )

    class Meta:
        ordering = ('orden',)

    def __unicode__(self):
        return "Asignacion de entrada %s" % unicode(self.entrada) + " a %s" % unicode(self.ficha)

"""
Reglas de visibilidad para las preguntas
"""
Iguala = 'igual_a'
Noiguala = 'no_igual_a'
Contiene = 'contiene'
Empiezacon = 'empieza_con'
Mayorque = 'mayor_que'
Menorque = 'menor_que'
Esvacio = 'es_vacio'
Noesvacio = 'no_es_vacio'
OPERADOR_CHOICES = (
        (Iguala, 'Igual a'),
        (Noiguala, 'No igual a'),
        (Contiene, 'Contiene'),
        (Empiezacon, 'Empieza con'),
        (Mayorque, 'Mayor que'),
        (Menorque, 'Menor que'),
        (Esvacio, 'Es vacio'),
        (Noesvacio, 'No es vacio'),
    )


class ReglaVisibilidad(models.Model):
    """
    Define cuando una encuesta es visible o no
    """
    elemento = models.ForeignKey(Entrada, on_delete=models.CASCADE, blank=False, null=False)
    operador = models.CharField(max_length=50, choices=OPERADOR_CHOICES, blank=False, null=False, unique=False)
    valor = models.CharField(max_length=100, blank=False, null=False, unique=False)

    def __unicode__(self):
        return "%s " % self.elemento+self.operador+" "+self.valor


class FormularioAsociado(models.Model):
    form_asociado = models.ForeignKey(Formulario, on_delete=models.CASCADE, blank=False, null=False)
    seleccionar_existentes = models.BooleanField(default=False)
    crear_nuevo = models.BooleanField(default=False)
    actualizar_existente = models.BooleanField(default=False)
    seleccionar_multiples = models.BooleanField(default=False)
    # entrada_fuente = models.ForeignKey(
    #     Entrada,
    #     related_name='entradafuente',
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     null=True
    # )
    # entrada_destino = models.ForeignKey(
    #     Entrada,
    #     related_name='entradadestino',
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     null=True
    # )

    def __unicode__(self):
        return "%s " % self.form_asociado


class ReglaAutollenado(models.Model):
    asociacion = models.ForeignKey(
        FormularioAsociado,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    entrada_fuente = models.ForeignKey(
        Entrada,
        related_name='entradafuente',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    entrada_destino = models.ForeignKey(
        Entrada,
        related_name='entradadestino',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __unicode__(self):
        return "%s " % self.asociacion


class Respuesta(models.Model):
    valor = models.CharField(max_length=500, blank=True, unique=False)
    # Filtro condicional
    pregunta_id = models.PositiveIntegerField(blank=True, null=True)
    respuesta = models.CharField(max_length=500, blank=True, null=True)
    usuario = models.ForeignKey(User, null=True)

    class Meta:
        ordering = ('id',)

    def __unicode__(self):
        return self.valor


# class FormularioDiligenciado(models.Model):
    # nombre  = modelsself.CharField(max_length=50, blank=True, unique=True)
    # empresa = models.ForeignKey('Empresa', null=True,blank=True)
    # colector = models.ForeignKey('Colector', null=True,blank=True)
    # entrada = models.ForeignKey('Entrada', null=True,blank=True)
    # respuesta = models.ForeignKey('Respuesta', null=True,blank=True)
    # gps  = models.CharField(max_length=50, blank=True, unique=True)
    # fecha_creacion = models.DateTimeField(auto_now=True)

    # def __unicode__(self):
    #     return self.nombre


class FormularioDiligenciado(models.Model):
    nombre = models.CharField(max_length=50, blank=True, unique=True)
    empresa = models.ForeignKey('Empresa', null=True, blank=True)
    colector = models.ForeignKey('Colector', null=True, blank=True)
    entrada = models.ForeignKey('Entrada', null=True, blank=True)
    respuesta = models.ForeignKey('Respuesta', null=True, blank=True)
    gps = models.CharField(max_length=50, blank=True, unique=True)
    fecha_creacion = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.nombre
