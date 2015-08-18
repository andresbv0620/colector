from django.db import models
from registro.models import Empresa
import hashlib
# Create your models here.

class Token(models.Model):
	empresa = models.OneToOneField(Empresa )
	valor  = models.CharField(max_length=50 , unique=True, blank= True)

	def save(self, *args, **kwargs):
		
		self.valor = hashlib.md5(self.empresa.nombre).hexdigest()
		super(Token, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.empresa.nombre