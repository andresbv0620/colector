from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Empresa(models.Model):
	usuario  = models.OneToOneField(User)
	codigo_secreto =  models.CharField(max_length=50)
	nombre = models.CharField(max_length=50, blank = True , unique=True)
	industria = models.CharField(max_length=50, blank = True )
	pais = models.CharField(max_length=50, blank = True )
	ciudad = models.CharField(max_length=50, blank = True )
	correo_empresarial = models.TextField(max_length=50, blank = True )
	email = models.CharField(max_length=50, blank = True )
	descripcion = models.TextField(max_length=50, blank = True )
	nit = models.IntegerField(  blank = True, null = True)
	correo_facturacion = models.CharField(max_length=50, blank = True , unique=True)
	telefono = models.IntegerField(  blank = True, null = True)
	plan = models.ForeignKey('Plan', null = True,  blank = True)
	colector = models.ManyToManyField('Colector',  blank = True)
	formulario = models.ManyToManyField('Formulario',  blank = True)
	tablets = models.ManyToManyField('Tablet',  blank = True)

		
	
	def __unicode__(self):
		return self.nombre

class Tablet(models.Model):
	codigo = models.CharField(max_length=50, blank = True , unique=True)

	def __unicode__(self):
		return self.codigo 


class Colector(models.Model):
	usuario  = models.OneToOneField(User, blank = True)

	def __unicode__(self):
		return self.usuario.username

class Plan(models.Model):
	nombre  = models.CharField(max_length=50, blank = True , unique=True)
	almacenamiento  = models.CharField(max_length=50, blank = True , unique=True)
	cantidad_colectores  = models.IntegerField(blank = True , unique=True)
	valor  = models.CharField(max_length=50, blank = True , unique=True) 
	activo = models.BooleanField(default = False)
	fecha_creacion = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.nombre


class Formulario(models.Model):
	nombre  = models.CharField(max_length=50, blank = True , unique=True)
	descripcion = models.TextField(max_length=50, blank = True )
	ficha = models.ManyToManyField('Ficha',  blank = True)
	
	def __unicode__(self):
		return self.nombre

class PermisoFormulario(models.Model):
	formulario = models.ForeignKey('Formulario')
	colectores = models.ManyToManyField('Colector')

	def __unicode__(self):
		return self.formulario.nombre


class Ficha(models.Model):
	nombre  = models.CharField(max_length=50, blank = True , unique=True)
	descripcion = models.TextField(max_length=50, blank = True )
	entrada = models.ManyToManyField('Entrada',  blank = True)
	def __unicode__(self):
		return self.nombre

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
GPS='12'
FORMULA='13'
FIRMA='14'
DECIMAL='15'
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
        
    )

SI = 'SI'
NO = 'NO'
REQUIRED_CHOICES = (
        (SI, 'SI'),
        (NO, 'NO'),
    )

class Entrada(models.Model):
	tipo = models.CharField(max_length=2, choices=ENTRADA_CHOICES, default=TEXTO)
	nombre  = models.CharField(max_length=50, blank = True , unique=True)
	descripcion = models.TextField(max_length=50, blank = True )
	respuesta = models.ManyToManyField('Respuesta',  blank = True)
	form_asociado = models.ForeignKey('Formulario', blank = True, null = True)
	requerido = models.CharField(max_length=2, choices=REQUIRED_CHOICES, default=SI)
	defecto  = models.CharField(max_length=50, blank = True , unique=False)
	maximo	= models.CharField(max_length=50, blank = True , unique=False)
	minimo = models.CharField(max_length=50, blank = True , unique=False)
	def __unicode__(self):
		return self.nombre

class Respuesta(models.Model):
	valor  = models.CharField(max_length=50, blank = True , unique=True)

	def __unicode__(self):
		return self.valor

#class FormularioDiligenciado(models.Model):
	#nombre  = models.CharField(max_length=50, blank = True , unique=True)
	#empresa = models.ForeignKey('Empresa', null = True,  blank = True)
	#colector = models.ForeignKey('Colector', null = True,  blank = True)
	#entrada = models.ForeignKey('Entrada', null = True,  blank = True)
	#respuesta = models.ForeignKey('Respuesta', null = True,  blank = True)
	#gps  = models.CharField(max_length=50, blank = True , unique=True)
	#fecha_creacion = models.DateTimeField(auto_now=True)

	#def __unicode__(self):
	#	return self.nombre


class FormularioDiligenciado(models.Model):
	nombre  = models.CharField(max_length=50, blank = True , unique=True)
	empresa = models.ForeignKey('Empresa', null = True,  blank = True)
	colector = models.ForeignKey('Colector', null = True,  blank = True)
	entrada = models.ForeignKey('Entrada', null = True,  blank = True)
	respuesta = models.ForeignKey('Respuesta', null = True,  blank = True)
	gps  = models.CharField(max_length=50, blank = True , unique=True)
	fecha_creacion = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.nombre


