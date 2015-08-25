from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from registro.models import PermisoFormulario, Colector, Formulario
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

class SingleForm(View):    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(SingleForm, self).dispatch(*args, **kwargs)

    def post(self, request):
    	resp = {}
    	# validando data del body
        try:
        	data = json.loads(request.body)
        	form_id = data['form_id']

        	#validando de que exista el formulario"
        	try:
        		form = Formulario.objects.get(id = int(form_id))
        		
        		formulario = {}
        		formulario['name'] = form.nombre
        		formulario['id'] = form.id
        		formulario['description'] = form.descripcion

        		#validando que el formulario tenga fichas asociadas
        		if len(form.ficha.all()):
        			formulario['sections'] = []
        			for f in form.ficha.all():
        				ficha = {}
        				ficha['name'] = f.nombre
        				ficha['description'] = f.descripcion
        				#validando que la ficha tenga entradas asociadas
        				if len(f.entrada.all()):
        					ficha['entradas'] = []
        					for e in f.entrada.all():
        						entrada = {}
        						entrada['name'] = e.nombre
        						entrada['description'] = e.descripcion
        						entrada['type'] = e.tipo
        						ficha['entradas'].append(entrada)

        						if len(e.respuesta.all()):
        							entrada['responses'] = []
        							for r in e.respuesta.all():	        								
        								respuesta = {}
        								respuesta['value'] = r.valor
        								entrada['responses'].append(respuesta)

        						else:
        							entrada['responses'] = []


        				else:
        					ficha['entradas'] = []



        				formulario['sections'].append(ficha)




        		else:
        			formulario['sections'] = []

        		resp['response_code'] = '200'
        		resp['response_description'] = str('form found')
        		resp['body_received'] = str(request.body)
        		resp['body_expected'] = str('{"form_id":" "}')
        		resp['response_data'] = []
        		resp['response_data'].append(formulario)

        		return HttpResponse(json.dumps(resp), content_type= "application/json")

        	except Formulario.DoesNotExist:
        		resp['response_code'] = '404'
            	resp['response_description'] = str('form not found')
            	resp['body_received'] = str(request.body)
            	resp['body_expected'] = str('{"form_id":" "}')


            	return HttpResponse(json.dumps(resp), content_type= "application/json")


        except  Exception as e:

            resp['response_code'] = '400'
            resp['response_description'] = str('invalid body request '+ str(e.args))
            resp['body_received'] = str(request.body)
            resp['body_expected'] = str('{"form_id":" "}')


            return HttpResponse(json.dumps(resp), content_type= "application/json")


    	return HttpResponse("Single form")
    	