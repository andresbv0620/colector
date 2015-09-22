from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
	return render(request, 'administrador/index.html')
	#return HttpResponse("interfaz principal de la calculadora")

class DevolverJson(View):


    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(DevolverJson, self).dispatch(*args, **kwargs)

    def get(self, request):

    	personas = []
    	persona1 = {}
    	persona1['nombre'] = "juan"
    	persona1['cedula'] = 9874
    	personas.append(persona1)

    	persona2 = {}
    	persona2['nombre'] = "pedro"
    	persona2['cedula'] = 123456
    	personas.append(persona2)

        resp = {}
        resp['response'] = personas
        return HttpResponse(json.dumps(resp),
                                    content_type='application/json')