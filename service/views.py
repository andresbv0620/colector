from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from registro.models import PermisoFormulario, Colector
import json
import hashlib


# Create your views here.

class AllowedForms(View):    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(AllowedForms, self).dispatch(*args, **kwargs)

    def post(self, request):
    	resp = {}
    	# validando data del body
        try:
            data = json.loads(request.body)
            colector_id = data['colector_id']
            #obteniendo formularios con permisos del colector recibido
            permiso_formularios = PermisoFormulario.objects.filter(colectores__usuario__id = colector_id)
            if len(permiso_formularios):
            	formularios_array = []
            	response_data = {}
            	#parseando formularios a json
            	for p in permiso_formularios:
            		response_data['form_name'] = p.formulario.nombre
            		response_data['form_id'] = str(p.formulario.id)
            		formularios_array.append(response_data)
            		response_data = {}
            	return HttpResponse(json.dumps(formularios_array), content_type= "application/json")
            else:
            	resp['response_code'] = '400'
            	resp['response_description'] = "Not available forms"
            	resp['body_received'] = str(request.body)
            	resp['body_expected'] = str('{"colector_id":" "}')


            	return HttpResponse(json.dumps(resp), content_type= "application/json")

        except  Exception as e:

            resp['response_code'] = '400'
            resp['response_description'] = str('invalid body request '+ str(e.args))
            resp['body_received'] = str(request.body)
            resp['body_expected'] = str('{"colector_id":" "}')


            return HttpResponse(json.dumps(resp), content_type= "application/json")
    	