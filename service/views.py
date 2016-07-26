#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
from django.core.files.storage import default_storage
from django.contrib.auth.models import User, Group
from django.core.files.base import ContentFile
from django.core.cache import cache
from django.core.files import File
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.utils.encoding import smart_str, smart_unicode
from django.views.decorators.csrf import csrf_exempt
from registro.models import PermisoFormulario, Colector, Formulario, Entrada, Empresa, Entrada, Respuesta, ReglaVisibilidad, FormularioAsociado, AsignacionEntrada
import json
from bson import json_util
import hashlib
import pymongo
import uuid
import collections
from datetime import datetime
import time
import codecs
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
servidor = pymongo.MongoClient('localhost', 27017)
database = servidor.colector

#Convert cursor of mongo to a dict python
def convert(data):
    if isinstance(data, basestring):
        return smart_str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

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

            # obteniendo formularios con permisos del colector recibido

            permiso_formularios = \
                PermisoFormulario.objects.filter(colectores__usuario__id=colector_id)
            if len(permiso_formularios):
                formularios_array = []
                response_data = {}

                # parseando formularios a json

                for p in permiso_formularios:
                    response_data['form_name'] = p.formulario.nombre
                    response_data['form_id'] = str(p.formulario.id)
                    formularios_array.append(response_data)
                    response_data = {}
                return HttpResponse(json.dumps(formularios_array),
                                    content_type='application/json')
            else:
                resp['response_code'] = '400'
                resp['response_description'] = 'Not available forms'
                resp['body_received'] = str(request.body)
                resp['body_expected'] = str('{"colector_id":" "}')

                return HttpResponse(json.dumps(resp),
                                    content_type='application/json')
        except Exception, e:

            resp['response_code'] = '400'
            resp['response_description'] = str('invalid body request '
                    + str(e.args))
            resp['body_received'] = str(request.body)
            resp['body_expected'] = str('{"colector_id":" "}')

            return HttpResponse(json.dumps(resp),
                                content_type='application/json')

class GetForms(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(GetForms, self).dispatch(*args, **kwargs)

    def post(self, request):
        resp = {}

        # validando data del body
        try:
            data = json.loads(request.body)
            #form_id = data['form_id']
            colector_id = data['colector_id']

            # obteniendo formularios con permisos del colector recibido
            permiso_formularios = \
                PermisoFormulario.objects.filter(colectores__usuario__id=int(colector_id))

            if len(permiso_formularios):
                formularios_array = []
                response_data = {}

                # parseando formularios a json
                resp['response_data'] = []

                #Se genera el listado de formularios con su respectiva informacion
                for p in permiso_formularios:

                    formulario = {}
                    formulario['form_name'] = p.formulario.nombre
                    formulario['form_id'] = p.formulario.id
                    formulario['form_description'] = p.formulario.descripcion
                    formulario['precargado'] = p.formulario.precargado
                    if not p.formulario.titulo_reporte:
                        formulario['titulo_reporte'] = ""                   
                    else:
                        formulario['titulo_reporte'] = p.formulario.titulo_reporte.id
                        
                        


                    # validando que el formulario tenga fichas asociadas
                    if len(p.formulario.ficha.all()):
                        formulario['sections'] = []
                        #Se genera el listado de fichas o secciones
                        for f in p.formulario.ficha.all():
                            ficha = {}
                            ficha['section_id'] = f.id
                            ficha['name'] = f.nombre
                            ficha['description'] = f.descripcion
                            #print f.nombre

                            # validando que la ficha tenga entradas asociadas
                            if len(f.entrada.all()):
                                ficha['inputs'] = []
                                #Se genera la lista de inputs o entradas
                                for e in f.entrada.all().order_by('asignacionentrada'):

                                    entrada = {}
                                    entrada['input_id'] = e.id
                                    entrada['name'] = e.nombre
                                    entrada['description'] = e.descripcion
                                    entrada['type'] = e.tipo
                                    #Datos tabla intermedia de relacion ficha entrada
                                    asignacionentrada = e.asignacionentrada_set.get(ficha=f)
                                    entrada['orden'] = asignacionentrada.orden
                                    entrada['requerido'] = asignacionentrada.requerido
                                    entrada['oculto'] = asignacionentrada.oculto
                                    entrada['solo_lectura'] = asignacionentrada.solo_lectura
                                    entrada['defecto'] = asignacionentrada.defecto
                                    entrada['defecto_previo'] = asignacionentrada.defecto_previo
                                    entrada['maximo'] = asignacionentrada.maximo
                                    entrada['minimo'] = asignacionentrada.minimo
                                    entrada['validacion'] = asignacionentrada.validacion

                                    if (asignacionentrada.regla_visibilidad == None):
                                        entrada['valorvisibility'] =[]
                                    else:
                                        entrada['valorvisibility']=[]
                                        reglavisibilidadobject ={}
                                        reglavisibilidad = ReglaVisibilidad.objects.get(visibilizar=asignacionentrada)
                                        reglavisibilidadobject['elemento'] = reglavisibilidad.elemento.id
                                        reglavisibilidadobject['operador'] = reglavisibilidad.operador
                                        reglavisibilidadobject['valor'] = reglavisibilidad.valor

                                        entrada['valorvisibility'].append(reglavisibilidadobject)


                                    #Se valida si tiene algun formulario asociado para precargar datos
                                    if asignacionentrada.formulario_asociado == None:
                                        entrada['asociate_form']=[]
                                    else:
                                        entrada['asociate_form']=[]
                                        atributos=[]
                                        objetos=[]
                                        registroOpcion={}                                        
                                        asociate_form = {}
                                        formasociado = FormularioAsociado.objects.get(formasociado=asignacionentrada)


                                        asociate_form['name'] = formasociado.form_asociado.nombre
                                        asociate_form['associate_id'] = formasociado.form_asociado.id
                                        asociate_form['description'] = formasociado.form_asociado.descripcion
                                        asociate_form['seleccionar_existentes'] = formasociado.seleccionar_existentes
                                        asociate_form['crear_nuevo'] = formasociado.crear_nuevo
                                        asociate_form['actualizar_existente'] = formasociado.actualizar_existente
                                        asociate_form['seleccionar_multiples'] = formasociado.seleccionar_multiples

                                        asociate_form['autollenar'] = []
                                        if len(asignacionentrada.formulario_asociado.reglaautollenado_set.all()):
                                            
                                            for rautollenar in asignacionentrada.formulario_asociado.reglaautollenado_set.all():
                                                regllenado={}
                                                regllenado['entrada_fuente']=rautollenar.entrada_fuente.id
                                                regllenado['entrada_destino']=rautollenar.entrada_destino.id
                                                asociate_form['autollenar'].append(regllenado)

                                        else:
                                            pass

                                        #asociate_form['entrada_fuente'] = formasociado.entrada_fuente.id
                                        #asociate_form['entrada_destino'] = formasociado.entrada_destino.id


                                        entrada['asociate_form'].append(asociate_form)
                                        entrada['options'] = []
                                        entrada['atributos'] = []
                                        document_filled_forms = database.filled_forms.find({"filled_forms.form_id":str(formasociado.form_asociado.id)},
                                            {"filled_forms.form_description":0,
                                            "filled_forms.form_name":0,
                                            "filled_forms.form_description":0,
                                            "filled_forms.fecha_creacion":0,
                                            "filled_forms.sections.description":0,
                                            "filled_forms.sections.name":0,
                                            "filled_forms.sections.section_id":0,
                                            "filled_forms.sections.inputs.input_id":0,
                                            "filled_forms.sections.inputs.description":0,
                                            "colector_id":0,
                                            "_id":0

                                            });
                                        arrayChecker=[]
                                        for filled in document_filled_forms:
                                            for record in filled["filled_forms"]:
                                                if record['form_id']!=str(formasociado.form_asociado.id):
                                                    pass
                                                else:
                                                    record["record_id"]=str(record["record_id"])

                                                    #La siguiente linea crea el nodo formula para hacer el calculo del valor de cada producto SOLO EN ORDEN VENTA
                                                    #Se debe ajustar para que sea dinamico y sea extensible a otras funcionalidades
                                                    #Deja estatico el valor del iva en 0,16
                                                    
                                                    #print record["responses"]
                                                    #Se itera sobre la opcion para sacar las variables de cada formula
                                                    precioProducto=0
                                                    ivaProducto=0
                                                    for option_response in record["responses"]:
                                                        
                                                        if option_response["label"]=="_PRECIO":
                                                            precioProducto=option_response["value"]
                                                                                                                   

                                                        if option_response["label"]=="_IVA":
                                                            ivaProducto=option_response["value"]
                                                                                                                    

                                                    record["formula"]='('+str(precioProducto)+'*<cantidad>)+('+str(precioProducto)+'*<cantidad>*'+str(ivaProducto)+')'

                                                    

                                                    #Crea el nodo opciones en base a el registro en mongodb
                                                    entrada['options'].append(record) #(json.dumps(f,default=json_util.default))


                                                    #Crear nodo ATRIBUTOS para cargar los campos de formulario anidado en caso de un nuevo registro

                                                    for recordinput in record["responses"]:
                                                        
                                                        if recordinput["input_id"] in arrayChecker:
                                                            pass
                                                        else:
                                                            objeto_atributos={}
                                                            arrayChecker.append(recordinput["input_id"])
                                                            objeto_atributos["label"]=recordinput["label"]
                                                            objeto_atributos["input_id"]=recordinput["input_id"]
                                                            record_entrada = Entrada.objects.get(id = str(recordinput["input_id"]))
                                                            objeto_atributos["type"]=record_entrada.tipo
                                                            
                                                            entrada_anidada = Entrada.objects.get(id=int(objeto_atributos["input_id"]))
                                                            if len(entrada_anidada.respuesta.all()):
                                                                objeto_atributos["responses"]=[]
                                                                for r in entrada_anidada.respuesta.all():
                                                                    respuestaAnidada={}
                                                                    respuestaAnidada['response_id'] = r.id
                                                                    respuestaAnidada['value'] = r.valor
                                                                    objeto_atributos["responses"].append(respuestaAnidada)

                                                            entrada['atributos'].append(objeto_atributos)


                                            form_aux = {}
                                            
                                    ficha['inputs'].append(entrada)

                                    if len(e.respuesta.all()):
                                        entrada['responses'] = []
                                        for r in e.respuesta.all():
                                            respuesta = {}
                                            respuesta['response_id'] = r.id
                                            respuesta['value'] = r.valor
                                            entrada['responses'].append(respuesta)
                                    else:

                                        entrada['responses'] = []
                            else:
                                ficha['inputs'] = []
                            formulario['sections'].append(ficha)
                    else:
                        formulario['sections'] = []

                    resp['response_data'].append(formulario)

                resp['response_code'] = '200'
                resp['response_description'] = str('forms found')
                resp['body_received'] = str(request.body)
                resp['body_expected'] = str('{"colector_id":" "}')
                
                

                return HttpResponse(json.dumps(resp,default=json_util.default),
                                    content_type='application/json')
            else:
                resp['response_code'] = '400'
                resp['response_description'] = 'Not available forms'
                resp['body_received'] = str(request.body)
                resp['body_expected'] = str('{"colector_id":" "}')

                return HttpResponse(json.dumps(resp),
                                    content_type='application/json')
        except Exception, e:
            print e
            resp['response_code'] = '400'
            resp['response_description'] = str('Invalid body request '
                    + str(e.args))
            resp['body_received'] = str(request.body)
            resp['body_expected'] = str('{"colector_id":" "}')

            return HttpResponse(json.dumps(resp),
                                content_type='application/json')

        return HttpResponse('Single form')

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

            # validando de que exista el formulario"

            try:
                form = Formulario.objects.get(id=int(form_id))

                formulario = {}
                formulario['form_name'] = form.nombre
                formulario['form_id'] = form.id
                formulario['form_description'] = form.descripcion

                # validando que el formulario tenga fichas asociadas

                if len(form.ficha.all()):
                    formulario['sections'] = []
                    for f in form.ficha.all():
                        ficha = {}
                        ficha['section_id'] = f.id
                        ficha['name'] = f.nombre
                        ficha['description'] = f.descripcion

                        # validando que la ficha tenga entradas asociadas

                        if len(f.entrada.all()):
                            ficha['inputs'] = []
                            for e in f.entrada.all():

                                entrada = {}
                                entrada['input_id'] = e.id
                                entrada['name'] = e.nombre
                                entrada['description'] = e.descripcion
                                entrada['type'] = e.tipo

                                
                                if e.form_asociado == None:
                                    pass
                                else:
                                    asociate_form = {}
                                    asociate_form['name'] = e.form_asociado.nombre
                                    asociate_form['associate_id'] = e.form_asociado.id
                                    asociate_form['description'] = e.form_asociado.descripcion
                                    entrada['asociate_form'] = asociate_form
                                    entrada['filled_forms'] = []
                                    filled_forms = database.filled_forms.find({"filled_forms.form_id":str(e.form_asociado.id)}, {"filled_forms.$": 1});
                                    for f in filled_forms:
                                        form_aux = {}
                                        print f
                                        
                                        entrada['filled_forms'].append(f) #(json.dumps(f,default=json_util.default))
                                        

                                ficha['inputs'].append(entrada)

                                if len(e.respuesta.all()):
                                    entrada['responses'] = []
                                    for r in e.respuesta.all():
                                        respuesta = {}
                                        respuesta['response_id'] = r.valor
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

                return HttpResponse(json.dumps(resp,default=json_util.default),
                                    content_type='application/json')
            except Formulario.DoesNotExist:

                resp['response_code'] = '404'
            resp['response_description'] = str('form not found')
            resp['body_received'] = str(request.body)
            resp['body_expected'] = str('{"form_id":" "}')

            return HttpResponse(json.dumps(resp),
                                content_type='application/json')
        except Exception, e:
            print e
            resp['response_code'] = '400'
            resp['response_description'] = str('invalid body request '
                    + str(e.args))
            resp['body_received'] = str(request.body)
            resp['body_expected'] = str('{"form_id":" "}')

            return HttpResponse(json.dumps(resp),
                                content_type='application/json')

        return HttpResponse('Single form')

#Guarda una estructura simple de las respuestas, colector_id, form_id, responses[id: , value: ]
class FillResponsesForm(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(FillResponsesForm, self).dispatch(*args, **kwargs)

    # validando la el formato del formulario enviado

    def dataValidator(self, array_validation):

        response = {}
        response['error'] = False
        response['validation_errors'] = []

        # validacion del formulario

        if not array_validation['latitud'].strip():
            response['error'] = True
            response['validation_errors'].append('latitud is blank')

        if not array_validation['longitud'].strip():
            response['error'] = True
            response['validation_errors'].append('longitud is blank')

        if not array_validation['horaini'].strip():
            response['error'] = True
            response['validation_errors'].append('horaini is blank')

        if not array_validation['horafin'].strip():
            response['error'] = True
            response['validation_errors'].append('horafin is blank')



        if not array_validation['colector_id'].strip():
            response['error'] = True
            response['validation_errors'].append('colector_id is blank')

        if not array_validation['form_id'].strip():

            response['error'] = True
            response['validation_errors'].append('form_id is blank')

        if len(array_validation['responses']) == 0:
            response['error'] = True
            response['validation_errors'].append('responses is blank')
        else:

            try:
                for responseItem in array_validation['responses']:
                    try:
                        response_value=responseItem['value']
                        input_id=responseItem['input_id']
                    except Exception, e:
                        response['error'] = True
                        response['validation_errors'].append("any response don't contains value or input_id")
                   
            except Exception, e:
                response['error'] = True
                response['validation_errors'].append("any input don't contains responses")

        return response

    def post(self, request):
        resp = {}
        # validando data correcta enviada en body
        try:
            data = json.loads(request.body)
            longitud = data['longitud']
            latitud = data['latitud']
            horaini = data['horaini']
            horafin = data['horafin']
            colector_id = data['colector_id']
            form_id = data['form_id']
            responses = data['responses']
            

            array_validation = {}
            array_validation['longitud'] = longitud
            array_validation['latitud'] = latitud
            array_validation['horaini'] = horaini
            array_validation['horafin'] = horafin
            array_validation['colector_id'] = colector_id
            array_validation['form_id'] = form_id
            array_validation['responses'] = responses

            data_validator = self.dataValidator(array_validation)

            if data_validator['error'] == True:
                resp['response_code'] = '400'
                resp['validation_errors'] = \
                    data_validator['validation_errors']
                resp['response_description'] = \
                    str('the body data contain validation errors')
                resp['body_received'] = str(request.body)
                resp['body_expected'] = \
                    str('{"colector_id":"", "form_id":" ","responses":" " }')

                return HttpResponse(json.dumps(resp,
                                    default=json_util.default),
                                    content_type='application/json')
            else:
                pass

            # construyendo json para insertar en mongodb

            try:

                form = {}
                form['fecha_creacion'] = datetime.utcnow()
                form['record_id']=str(uuid.uuid4())
                form['longitud'] = longitud
                form['latitud'] = latitud
                form['horaini'] = horaini
                form['horafin'] = horafin
                form['form_id'] = form_id
                formulario = Formulario.objects.get(id = int(form['form_id']))
                form['form_name'] = formulario.nombre
                form['form_description'] = formulario.descripcion

                for response in responses:
                    input_id=response['input_id']
                    entrada = Entrada.objects.get(id = int(input_id))
                    response['label']=entrada.nombre
                    response['tipo']=entrada.tipo
                    if entrada.tipo == "4" or entrada.tipo == "5":
                        try:
                            response_id=response['value']
                            respuesta = Respuesta.objects.get(id = int(response_id))
                            response['value']=respuesta.valor
                        except Exception, e:
                            resp['Warning'] = 'Algunas opciones de respuesta no se almacenaron correctamente: ' + str(response['value'])
                            response['value']="Op_" + str(response['value'])


                form['responses'] = responses

                # return HttpResponse(json.dumps(data))
                colector = \
                    database.filled_forms.find_one({'colector_id': str(colector_id)},
                        {'_id': 0})                

                # validando si existe un colector con esta id
                if colector == None:
                    data = {}
                    data['colector_id'] = colector_id
                    data['filled_forms'] = []
                    data['filled_forms'].append(form)
                    
                    database.filled_forms.insert(data)
                    database.filled_forms.create_index("filled_forms.sections.inputs.responses")

                else:
                    database.filled_forms.update({'colector_id': str(colector_id)},
                            {'$push': {'filled_forms': form}})

                    # return HttpResponse("colector existe")
                resp['response_code'] = '200'
                resp['response_description'] = str('form filled')
                resp['body_received'] = str(request.body)
                resp['record_id'] = form['record_id']
                resp['body_expected'] = \
                    str('{"colector_id":"", "form_id":" ", "responses":"[]"  }'
                        )
                resp['response_data'] = request.body

                return HttpResponse(json.dumps(resp),
                                    content_type='application/json')
            except Exception, e:

                resp['response_code'] = '400'
                resp['response_description'] = \
                    str('Error inserting data in mongodb' + str(e.args))
                resp['body_received'] = str(request.body)
                resp['body_expected'] = \
                    str('{"colector_id":"", "form_id":" ", "responses":"[]"  }'
                        )
                resp['response_data'] = request.body

            return HttpResponse(json.dumps(resp), content_type='application/json')
        except Exception, e:

            resp['response_code'] = '400'
            resp['response_description'] = str('invalid body request '
                    + str(e.args))
            resp['body_received'] = str(request.body)
            resp['body_expected'] = \
                str('{"colector_id":"", "form_id":" ", "responses":"[]" }')

            return HttpResponse(json.dumps(resp),
                                content_type='application/json')

#Guarda una foto a la vez (En base64)
class SaveImg(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(SaveImg, self).dispatch(*args, **kwargs)

    # validando la el formato del formulario enviado

    def dataValidator(self, array_validation):
        response = {}
        response['error'] = False
        response['validation_errors'] = []

        # validacion del formulario

        if not array_validation['fileSend']:
            response['error'] = True
            response['validation_errors'].append('There is no document')

        if not array_validation['extensionFile'].strip():
            response['error'] = True
            response['validation_errors'].append('extension in file is blank')

        if not array_validation['question_id'].strip():
            response['error'] = True
            response['validation_errors'].append('question_id is blank')

        if not array_validation['survey_id'].strip():
            response['error'] = True
            response['validation_errors'].append('survey_id is blank')

        if not array_validation['nameFile'].strip():
            response['error'] = True
            response['validation_errors'].append('name in file is blank')

        if not array_validation['colector_id'].strip():
            response['error'] = True
            response['validation_errors'].append('colector_id in file is blank')

        return response

    def handle_uploaded_file(self, f, name, extension, question_id):
        #file_path='/home/andres/media/'+name+'.'+extension
        #file_path=settings.FILES_ROOT+name+'.'+extension
        file_path=settings.FILES_ROOT+question_id+'/'+name+'.'+extension
        with default_storage.open(file_path, 'wb') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return file_path

    def post(self, request):
        resp={}
        try:
            fileSend = request.FILES['document']
            extensionFile = request.POST['extension']
            question_id = request.POST['question_id']
            survey_id = request.POST['survey_id']
            nameFile = request.POST['name']
            colector_id = request.POST['colector_id']

            array_validation = {}
            array_validation['fileSend'] = fileSend
            array_validation['extensionFile'] = extensionFile
            array_validation['question_id'] = question_id
            array_validation['survey_id'] = survey_id
            array_validation['nameFile'] = nameFile
            array_validation['colector_id'] = colector_id

            data_validator = self.dataValidator(array_validation)

            if data_validator['error'] == True:
                resp['response_code'] = '400'
                resp['validation_errors'] = \
                    data_validator['validation_errors']
                resp['response_description'] = \
                    str('the body data contains validation errors')
                resp['body_received'] = str(request.body)
                resp['form_data_expected'] = \
                    str('{"fileSend":"", "extensionFile":" ","question_id":" ","survey_id":" " ,"nameFile":" ", colector_id  }')

                return HttpResponse(json.dumps(resp,
                                    default=json_util.default),
                                    content_type='application/json')
            else:
                pass

        
            # Todo Validado entonces continuamos
            uploaded_file = self.handle_uploaded_file(fileSend, nameFile.replace('"',''), extensionFile.replace('"',''), question_id)

            resp['response_code'] = '200'
            resp['response_description'] = str('Media Document Saved')
            resp['media_url'] = str(uploaded_file)
            resp['form_data_expected'] = \
                str('{"fileSend":"", "extensionFile":" ","question_id":" ","survey_id":" " ,"nameFile":" ", colector_id  }')

            return HttpResponse(json.dumps(resp),
                        content_type='application/json')

        except Exception, e:
            resp['response_code'] = '400'
            resp['response_description'] = str('invalid body request '
                    + str(e.args))
            resp['form_data_expected'] = \
                str('{"fileSend":"", "extensionFile":" ","question_id":" ","survey_id":" " ,"nameFile":" ", colector_id  }')
            return HttpResponse(json.dumps(resp), content_type='application/json')

#Permite precargar registros en un formulario con datos desde un archivo plano
class UploadData(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UploadData, self).dispatch(*args, **kwargs)

    def dataValidator(self, array_validation):
        response = {}
        response['error'] = False
        response['validation_errors'] = []

        # validacion del formulario

        if not array_validation['fileSend']:
            response['error'] = True
            response['validation_errors'].append('There is no document')

        if not array_validation['extensionFile'].strip():
            response['error'] = True
            response['validation_errors'].append('extension in file is blank')

        if not array_validation['question_id'].strip():
            response['error'] = True
            response['validation_errors'].append('question_id is blank')

        if not array_validation['survey_id'].strip():
            response['error'] = True
            response['validation_errors'].append('survey_id is blank')

        if not array_validation['nameFile'].strip():
            response['error'] = True
            response['validation_errors'].append('name in file is blank')

        if not array_validation['colector_id'].strip():
            response['error'] = True
            response['validation_errors'].append('colector_id in file is blank')

        return response

    def handle_uploaded_file(self, f, name, extension, question_id):
        resp={}
        try:
            #file_path='/home/andres/media/'+name+'.'+extension
            #file_path=settings.FILES_ROOT+name+'.'+extension
            file_path=settings.FILES_ROOT+question_id+'/'+name+'.'+extension
            with default_storage.open(file_path, 'wb') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            resp['path']=file_path
            resp['error'] = False
            return resp
        except Exception, e:            
            resp['error'] = True
            resp['response_description'] = str('No fue posible subir el archivo al servidor ')+str(e)
            return resp

    def insert_file_records(self, file_path, form_id, colector_id, element_longitud, element_latitud):
        try:
            csvFile = default_storage.open(file_path)
            #csvFile = open('example.csv')
            csvReader = csv.reader(csvFile, delimiter=';')
            #csvData = list(csvReader)
        except Exception, e:
            return str('No se encuentra el archivo en el servidor'
                    + str(e.args)) + str(input_id)

        records_counter=0
        for row in csvReader:
            #print('Row #' + str(csvReader.line_num) + ' ' + str(row))
            if csvReader.line_num==1:
                inputsList=[]
                for input_id in row:
                    inputObject = {}
                    try:
                        entrada = Entrada.objects.get(id = int(input_id))
                        inputObject['input_id']=input_id
                        inputObject['label']=entrada.nombre
                        inputObject['tipo']=entrada.tipo
                        inputsList.append(inputObject)
                    except Exception, e:
                        return str('No se encuentra el id de la entrada definida en el encabezado del archivo'
                                + str(e.args)) + str(input_id)  

            # construyendo json para insertar en mongodb
            try:
                form = {}
                form['fecha_creacion'] = datetime.utcnow()
                form['record_id']=str(uuid.uuid4())
                form['horaini'] = datetime.utcnow()
                form['horafin'] = datetime.utcnow()
                form['form_id'] = form_id
                formulario = Formulario.objects.get(id = int(form['form_id']))
                form['form_name'] = formulario.nombre
                form['form_description'] = formulario.descripcion

                responsesArray=[]
                for rowvalue in row:
                    index = row.index(rowvalue)
                    inputObject=inputsList[index]
                    inputObject['value'] = rowvalue

                    if inputObject['input_id']==element_longitud:
                        form['longitud'] = rowvalue

                    if inputObject['input_id']==element_latitud:
                        form['latitud'] = rowvalue

                form['responses'] = inputsList

                colector = database.filled_forms.find_one({'colector_id': str(colector_id)},{'_id': 0})                

                # validando si existe un colector con esta id
                if colector == None:
                    data = {}
                    data['colector_id'] = colector_id
                    data['filled_forms'] = []
                    data['filled_forms'].append(form)
                    
                    database.filled_forms.insert(data)
                    #database.filled_forms.create_index("filled_forms.sections.inputs.responses")
                    records_counter+=1

                else:
                    database.filled_forms.update({'colector_id': str(colector_id)},
                            {'$push': {'filled_forms': form}})
                    records_counter+=1

            except Exception, e:
                return str('Error inserting data in mongodb' + str(e.args))
 
        return str('Los registros del documento csv han sido guardados. Registros totales: ' + str(records_counter))

    def post(self, request):
        resp={}
        try:
            fileSend = request.FILES['document']
            extensionFile = request.POST['extension']
            question_id = request.POST['question_id']
            survey_id = request.POST['survey_id']
            nameFile = request.POST['name']
            colector_id = request.POST['colector_id']
            element_longitud = request.POST['element_longitud']
            element_latitud = request.POST['element_latitud']

            array_validation = {}
            array_validation['fileSend'] = fileSend
            array_validation['extensionFile'] = extensionFile
            array_validation['question_id'] = question_id
            array_validation['survey_id'] = survey_id
            array_validation['nameFile'] = nameFile
            array_validation['colector_id'] = colector_id

            data_validator = self.dataValidator(array_validation)
            

            if data_validator['error'] == True:
                resp['response_code'] = '400'
                resp['validation_errors'] = \
                    data_validator['validation_errors']
                resp['response_description'] = \
                    str('the body data contains validation errors')
                resp['body_received'] = str(request.body)
                resp['form_data_expected'] = \
                    str('{"fileSend":"", "extensionFile":" ","question_id":" ","survey_id":" " ,"nameFile":" ", colector_id  }')

                return HttpResponse(json.dumps(resp,
                                    default=json_util.default),
                                    content_type='application/json')
            else:
                pass

            # Todo Validado entonces continuamos
            uploaded_file = self.handle_uploaded_file(fileSend, nameFile.replace('"',''), extensionFile.replace('"',''), question_id)
            print uploaded_file
            if uploaded_file['error']:
                resp['response_code'] = '403'
                resp['response_description'] = uploaded_file['response_description']
                resp['form_data_expected'] = \
                    str('{"fileSend":"", "extensionFile":" ","question_id":" ","survey_id":" " ,"nameFile":" ", colector_id  }')
                return HttpResponse(json.dumps(resp), content_type='application/json')

            else:
                path_file = uploaded_file['path']
                print path_file


            # Leemos y cargamos en mongo los registros del archivo, pasando el path del archivo guardado uploaded_file
            registered_file = self.insert_file_records(path_file, survey_id, colector_id, element_longitud, element_latitud)

            print registered_file


            resp['response_code'] = '200'
            resp['response_description'] = str(registered_file)
            resp['media_url'] = str(uploaded_file)
            resp['form_data_expected'] = \
                str('{"fileSend":"", "extensionFile":" ","question_id":" ","survey_id":" " ,"nameFile":" ", "colector_id":""  }')

            return HttpResponse(json.dumps(resp),
                        content_type='application/json')

        except Exception, e:
            resp['response_code'] = '403'
            resp['response_description'] = str('invalid body request '
                    + str(e.args))
            resp['form_data_expected'] = \
                str('{"fileSend":"", "extensionFile":" ","question_id":" ","survey_id":" " ,"nameFile":" ", colector_id  }')
            return HttpResponse(json.dumps(resp), content_type='application/json')




#ELIMINA UN REGISTRO
class DeleteResponsesForm(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(DeleteResponsesForm, self).dispatch(*args, **kwargs)

    # validando la el formato del formulario enviado
    def post(self, request):
        resp = {}
        # validando data correcta enviada en body
        try:
            data = json.loads(request.body)
            colector_id = data['colector_id']
            record_id = data['record_id']

            try:
                try:
                    user_id = int(colector_id)
                    user = User.objects.get(id=user_id)
                except  User.DoesNotExist:
                    resp['response_code'] = '400'
                    resp['response_description'] = str('User Does Not Exist' + str(e.args))
                    resp['body_received'] = str(request.body)
                    resp['body_expected'] = str('{"colector_id":"", "record_id":"d"}')
                    resp['response_data'] = request.body
                    return HttpResponse(json.dumps(resp), content_type='application/json')

                if user.groups.filter(name='administrador'):
                    empresa = user.empresa
                    for colectorindjango in empresa.colector.all():
                        print str(colectorindjango.id)
                        colectorinmongo = database.filled_forms.find_one({'colector_id': str(colectorindjango.id)}, {'_id': 0})                
                        # validando si existe un colector con esta id
                        if colectorinmongo == None:
                            pass
                        else:
                            database.filled_forms.update({'colector_id': str(colectorindjango.id)},{'$pull': {'filled_forms':{'record_id':record_id} }})

                        # return HttpResponse("colector existe")

                    resp['response_code'] = '200'
                    resp['response_description'] = str('form filled')
                    resp['body_received'] = str(request.body)
                    resp['body_expected'] = \
                        str('{"colector_id":"", "form_id":" ", "responses":"[]"  }'
                            )
                    resp['response_data'] = request.body

                    return HttpResponse(json.dumps(resp),
                                        content_type='application/json')
            except Exception, e:
                resp['response_code'] = '400'
                resp['response_description'] = \
                    str('Error inserting data in mongodb' + str(e.args))
                resp['body_received'] = str(request.body)
                resp['body_expected'] = \
                    str('{"colector_id":"", "form_id":" ", "responses":"[]"  }'
                        )
                resp['response_data'] = request.body

            return HttpResponse(json.dumps(resp),
                                content_type='application/json')
        except Exception, e:

            resp['response_code'] = '400'
            resp['response_description'] = str('invalid body request '
                    + str(e.args))
            resp['body_received'] = str(request.body)
            resp['body_expected'] = \
                str('{"colector_id":"", "form_id":" ", "responses":"[]" }')

            return HttpResponse(json.dumps(resp),
                                content_type='application/json')

#EDITA UN REGISTRO
class EditResponsesForm(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(DeleteResponsesForm, self).dispatch(*args, **kwargs)

    # validando la el formato del formulario enviado
    def post(self, request):
        resp = {}
        # validando data correcta enviada en body
        try:
            data = json.loads(request.body)
            colector_id = data['colector_id']
            record_id = data['record_id']
            # construyendo json para insertar en mongodb

            try:
                colector = \
                    database.filled_forms.find_one({'colector_id': str(colector_id)},
                        {'_id': 0})                

                # validando si existe un colector con esta id

                if colector == None:
                    pass

                else:

                    database.filled_forms.update({'colector_id': str(colector_id)},
                            {'$pull': {'filled_forms':{'record_id':record_id} }})

                    # return HttpResponse("colector existe")

                resp['response_code'] = '200'
                resp['response_description'] = str('form filled')
                resp['body_received'] = str(request.body)
                resp['body_expected'] = \
                    str('{"colector_id":"", "form_id":" ", "responses":"[]"  }'
                        )
                resp['response_data'] = request.body

                return HttpResponse(json.dumps(resp),
                                    content_type='application/json')
            except Exception, e:
                resp['response_code'] = '400'
                resp['response_description'] = \
                    str('Error inserting data in mongodb' + str(e.args))
                resp['body_received'] = str(request.body)
                resp['body_expected'] = \
                    str('{"colector_id":"", "form_id":" ", "responses":"[]"  }'
                        )
                resp['response_data'] = request.body

            return HttpResponse(json.dumps(resp),
                                content_type='application/json')
        except Exception, e:

            resp['response_code'] = '400'
            resp['response_description'] = str('invalid body request '
                    + str(e.args))
            resp['body_received'] = str(request.body)
            resp['body_expected'] = \
                str('{"colector_id":"", "form_id":" ", "responses":"[]" }')

            return HttpResponse(json.dumps(resp),
                                content_type='application/json')

#Guarda una estructura más compleja de los formularios, NO ESTA EN USO
class FillForm(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(FillForm, self).dispatch(*args, **kwargs)

    # validando la el formato del formulario enviado

    def dataValidator(self, array_validation):

        response = {}
        response['error'] = False
        response['validation_errors'] = []

        # validacion del formulario

        if not array_validation['colector_id'].strip():

            response['error'] = True
            response['validation_errors'].append('colector_id is blank')

        if not array_validation['form_id'].strip():

            response['error'] = True
            response['validation_errors'].append('form_id is blank')

        if not array_validation['form_name'].strip():

            response['error'] = True
            response['validation_errors'].append('form_name is blank')

        if len(array_validation['sections']) == 0:
            response['error'] = True
            response['validation_errors'].append('sections is blank')
        else:

            try:
                for s in array_validation['sections']:
                    inputs = s['inputs']

                    if len(inputs) == 0:
                        response['error'] = True
                        response['validation_errors'
                                 ].append('inputs is blank')
                    else:
                        for i in inputs:

                            try:
                                responses = i['responses']
                            except Exception, e:

                                response['error'] = True
                                response['validation_errors'
                                        ].append("any input don't contains responses"
                                        )
            except Exception, e:

                response['error'] = True
                response['validation_errors'
                         ].append("any section don't contains inputs")

        return response

    def get(self, request, id):
        resp = {}
        colector = \
            database.filled_forms.find_one({'colector_id': str(id)},
                {'_id': 0})

                # validando si existe un colector con esta id

        if colector == None:
            resp['response_code'] = '405'

            # resp['validation_errors'] = data_validator['validation_errors']

            resp['response_description'] = str('Colector not found')
        else:

            resp['response_code'] = '200'
            resp['response_description'] = str('Colector found')
            resp['response_data'] = json.dumps(colector,
                    default=json_util.default)

        return HttpResponse(json.dumps(resp),
                            content_type='application/json')

    def post(self, request):
        resp = {}
        # validando data correcta enviada en body
        try:
            data = json.loads(request.body)
            colector_id = data['colector_id']
            form_id = data['form_id']
            form_name = data['form_name']
            form_description = data['form_description']
            sections = data['sections']

            array_validation = {}
            array_validation['colector_id'] = colector_id
            array_validation['form_id'] = form_id
            array_validation['form_name'] = form_name
            array_validation['sections'] = sections

            data_validator = self.dataValidator(array_validation)

            if data_validator['error'] == True:
                resp['response_code'] = '400'
                resp['validation_errors'] = \
                    data_validator['validation_errors']
                resp['response_description'] = \
                    str('the body data contain validation errors')
                resp['body_received'] = str(request.body)
                resp['body_expected'] = \
                    str('{"colector_id":"", "form_id":" ", "form_name": " ", "form_description": " ", "sections":" " }'
                        )

                return HttpResponse(json.dumps(resp,
                                    default=json_util.default),
                                    content_type='application/json')
            else:
                pass

            # construyendo json para insertar en mongodb

            try:

                form = {}
                form['fecha_creacion'] = datetime.utcnow()
                form['register_id']=uuid.uuid4()
                form['form_id'] = form_id
                form['form_name'] = form_name
                form['form_description'] = form_description
                form['sections'] = sections

                # return HttpResponse(json.dumps(data))

                colector = \
                    database.filled_forms.find_one({'colector_id': str(colector_id)},
                        {'_id': 0})                

                # validando si existe un colector con esta id

                if colector == None:
                    data = {}
                    data['colector_id'] = colector_id
                    data['filled_forms'] = []
                    data['filled_forms'].append(form)
                    
                    database.filled_forms.insert(data)
                    database.filled_forms.create_index("filled_forms.sections.inputs.responses")

                else:

                    database.filled_forms.update({'colector_id': str(colector_id)},
                            {'$push': {'filled_forms': form}})

                    # return HttpResponse("colector existe")

                resp['response_code'] = '200'
                resp['response_description'] = str('form filled')
                resp['body_received'] = str(request.body)
                resp['body_expected'] = \
                    str('{"colector_id":"", "form_id":" ", "form_name": " ", "form_description": " ", "sections":"[]"  }'
                        )
                resp['response_data'] = request.body

                return HttpResponse(json.dumps(resp),
                                    content_type='application/json')
            except Exception, e:

                resp['response_code'] = '400'
                resp['response_description'] = \
                    str('Error inserting data in mongodb' + str(e.args))
                resp['body_received'] = str(request.body)
                resp['body_expected'] = \
                    str('{"colector_id":"", "form_id":" ", "form_name": " ", "form_description": " ", "sections":"[]"  }'
                        )
                resp['response_data'] = request.body

            return HttpResponse(json.dumps(resp),
                                content_type='application/json')
        except Exception, e:

            resp['response_code'] = '400'
            resp['response_description'] = str('invalid body request '
                    + str(e.args))
            resp['body_received'] = str(request.body)
            resp['body_expected'] = \
                str('{"colector_id":"", "form_id":" ", "form_name": " ", "form_description": " ", "sections":"[]" }'
                    )

            return HttpResponse(json.dumps(resp),
                                content_type='application/json')

    #Reporte SIN USO
 
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(FilledFormsReport, self).dispatch(*args, **kwargs)

    def post(self, request):
        resp = {}
        try:
            data = json.loads(request.body)
            colector_id = data['colector_id']
            query = "'colector_id': '2'"
            filled_forms = database.filled_forms.find({}, {'_id': 0})

            forms = []

            for f in filled_forms:
                forms.append(f)
            resp['data'] = forms
            return HttpResponse(json.dumps(resp,
                                default=json_util.default),
                                content_type='application/json')
        except Exception, e:

            resp['response_code'] = '400'
            resp['response_description'] = str('invalid body request '
                    + str(e.args))
            resp['body_received'] = str(request.body)
            resp['body_expected'] = str('{ }')
            return HttpResponse(json.dumps(resp,
                                default=json_util.default),
                                content_type='application/json')

#Reporte Colector_id
def ColectorIdReport(request, id):
    filled_forms = database.filled_forms.find({'colector_id': str(id)},
            {'_id': 0})
    resp = {}

    if filled_forms.count() == 0:
        resp['response_code'] = '404'
        resp['response_description'] = 'colector id not found'
        return HttpResponse(json.dumps(resp,
                            default=json_util.default),
                            content_type='application/json')
    else:

        # print filled_forms.count()

        forms = []
        for f in filled_forms:
            forms.append(f)
        resp['response_code'] = '200'
        resp['response_description'] = 'colector id found'
        resp['data'] = forms
        return HttpResponse(json.dumps(resp,
                            default=json_util.default),
                            content_type='application/json')

#Reporte por nombre formulario, NO ES NECESARIO
def FormNameReport(request, name):
    filled_forms = \
        database.filled_forms.find({'filled_forms.form_name': str(name)},
                                   {'_id': 0})
    resp = {}

    if filled_forms.count() == 0:
        resp['response_code'] = '404'
        resp['response_description'] = 'form name not found'
        return HttpResponse(json.dumps(resp,
                            default=json_util.default),
                            content_type='application/json')
    else:

        # print filled_forms.count()

        forms = []
        for f in filled_forms:
            forms.append(f)
        resp['response_code'] = '200'
        resp['response_description'] = 'form name found'
        resp['data'] = forms
        return HttpResponse(json.dumps(resp,
                            default=json_util.default),
                            content_type='application/json')

#Reporte por form id
def FormIdReport(request, id):
    filled_forms = \
        database.filled_forms.find({'filled_forms.form_id': str(id)},
                                   {'_id': 0})
    resp = {}

    if filled_forms.count() == 0:
        resp['response_code'] = '404'
        resp['response_description'] = 'form id not found'
        return HttpResponse(json.dumps(resp,
                            default=json_util.default),
                            content_type='application/json')
    else:

        # print filled_forms.count()

        forms = []
        for f in filled_forms:
            forms.append(f)

        resp['response_code'] = '200'
        resp['response_description'] = 'form id found'
        resp['data'] = forms
        return HttpResponse(json.dumps(resp,
                            default=json_util.default),
                            content_type='application/json')

#Reporte por form id paginacion
def FormIdReportPag(request, id):
    #Setting Pagination
    #sumo 1 porque en django la paginacion no empieza desde 0, empieza desde 1
    page=int(request.GET.get('page', 1))+1
    limit=int(request.GET.get('limit', 10))
    #Consulta a mongodb
    filled_forms = database.filled_forms.find({'filled_forms.form_id': str(id)}, {'_id': 0})
    resp = {}
    #Si hay registros realizo preparo la respuesta http, iterating on filled_forms
    if filled_forms.count() == 0:
        resp['response_code'] = '404'
        resp['response_description'] = 'form id not found'
        return HttpResponse(json.dumps(resp, default=json_util.default), content_type='application/json')
    else:
        #print "Count ",filled_forms.count()
        forms = []
        #Each colector has a document with its respective forms, the main nodes of a colector document are filled_forms=[] and colector_id
        #Below f is a document (a colector)
        for f in filled_forms:
            #print "Colector Id who contains this formid: ",f["colector_id"]
            #Converts mongo cursor into a python dict
            colectorForms=convert(f["filled_forms"])
            for colectorForm in reversed(colectorForms):
                colectorFormId=colectorForm["form_id"]
                #Filter the forms requested by id
                if colectorFormId == id:
                    #print colectorFormId
                    forms.append(colectorForm)

        forms.sort(key=lambda formu: formu["horafin"], reverse=True)

        #forms contiene todos los  registros del form con el id requerido. A continuacion se hace la paginacion
        paginator = Paginator(forms, limit) # Show limit records per page
        tableheader=[]

        try:
            paginatedForms = paginator.page(page)
            rows=[]
            columns=[]
            markersArray=[]

            #Setting the paggination attributes  
            resp['hasPrevious'] = paginatedForms.has_previous()
            if paginatedForms.has_previous():
                resp['hasPrevious'] = paginatedForms.has_previous()
                resp['previousPageNumber'] = paginatedForms.previous_page_number()

            resp['hasNext'] = paginatedForms.has_next()
            if paginatedForms.has_next():   
                resp['hasNext'] = paginatedForms.has_next()
                resp['nextPageNumber'] = paginatedForms.next_page_number()

            resp['currentPage'] = page
            resp['numPages'] = paginatedForms.paginator.num_pages


            for paginatedForm in paginatedForms:
                #print paginatedForm["form_name"]
                responses=paginatedForm["responses"]
                datarows = {}#Objeto que va guardando las respuestas de cada registro
                #markers objeto usado para el mapa
                markers = {}
                markers['longitude'] = paginatedForm["longitud"]
                markers['latitude'] = paginatedForm["latitud"]
                datarows["id"] = paginatedForm["record_id"]
                datarows["form_id"] = paginatedForm["form_id"]

                for response in responses:
                    inputId = response["input_id"]
                    #print "Input id: ", inputId
                    inputValue = response["value"]
                    inputLabel = response["label"]
                    inputType = response["tipo"]

                    #Se define la primer respuesta como el titulo del pin enel mapa
                    if not markers.has_key('message'):
                        markers['message'] = inputValue

                    #Validamos para generar la fila de encabezados
                    if not inputLabel in tableheader:
                        column = {}
                        column['field'] = inputLabel
                        column['sortable'] = True
                        column['title'] = inputLabel
                        columns.append(column)
                        tableheader.append(inputLabel)
                    
                    #Reporte numero, Se valida si es numero
                    if (inputType == '8'):
                        inputValue=float(inputValue)
                        if datarows.has_key(inputLabel):
                            datarows[inputLabel] = datarows[inputLabel] + ',' + inputValue
                        else:
                            datarows[inputLabel] = inputValue

                    #Reporte para foto, Se valida si es foto, para convertirla de base64
                    if ((inputType == '6')or(inputType=='14')):
                        if datarows.has_key(inputLabel):
                            datarows[inputLabel] = datarows[inputLabel] + '<a class="thumb"><img width="50px" height="50px" src="data:image/png;base64,' + inputValue + '" data-err-src="images/png/avatar.png"/><span><img width="450px" src="data:image/png;base64,' + inputValue + '" data-err-src="images/png/avatar.png"/></span></a>'
                        else:
                            datarows[inputLabel] = '<a class="thumb"><img width="50px" height="50px" src="data:image/png;base64,' + inputValue + '" data-err-src="images/png/avatar.png"/><span><img width="450px" src="data:image/png;base64,' + inputValue + '" data-err-src="images/png/avatar.png"/></span></a>'

                    #Reporte para el resto de tipos de entrada
                    if ((inputType=='1')or(inputType=='2')or(inputType=='3')or(inputType=='4')or(inputType=='5')or(inputType=='7')or(inputType=='9')or(inputType=='10')or(inputType=='11')or(inputType=='12')):
                        if datarows.has_key(inputLabel):
                            datarows[inputLabel] = datarows[inputLabel] + ',' + inputValue
                        else:
                            datarows[inputLabel] = inputValue

                #Fin for para mostrar cada respuesta (columna) de una fila
                #///////////Se asigna la hora de inicio y fin del registro a las respuestas////////////////
                horaini = float(paginatedForm["horaini"])
                datarows["Inicio"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(horaini))

                horafin = float(paginatedForm["horafin"])
                datarows["Fin"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(horafin))

                datarows["id"] = paginatedForm["record_id"]
                datarows["sorter"] = horafin

                datarows["Delete"] = '<a id="delete_row" href="#/reporte/id/'+datarows["form_id"]+'/record/delete/'+paginatedForm["record_id"]+'">Delete</a>'

                #//Se guardan las respuestas de la fila en el objeto data
                rows.append(datarows)
                
                markersArray.append(markers)
                resp['response_code'] = '200'
                resp['response_description'] = 'form id found'
                resp['total'] = len(forms)
                resp['rows'] = rows
                resp['cols'] = columns
                resp['markers'] = markersArray

        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            paginatedForms = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            paginatedForms = paginator.page(paginator.num_pages)

        

        return HttpResponse(json.dumps(resp,
                           default=json_util.default),
                          content_type='application/json')

#Reporte por fecha
def DateReport(
    request,
    id,
    a,
    m,
    d,
    ):

    d = datetime(int(a), int(m), int(d), 0)
    filled_forms = database.filled_forms.find({'colector_id': str(id),
            'filled_forms.fecha_creacion': {'$gte': d}}, {'_id': 0})
    resp = {}

    if filled_forms.count() == 0:
        resp['response_code'] = '404'
        resp['response_description'] = 'date not found'
        return HttpResponse(json.dumps(resp,
                            default=json_util.default),
                            content_type='application/json')
    else:

        # print filled_forms.count()

        forms = []
        for f in filled_forms:
            forms.append(f)
        resp['response_code'] = '200'
        resp['response_description'] = 'date found'
        resp['data'] = forms
        return HttpResponse(json.dumps(resp,
                            default=json_util.default),
                            content_type='application/json')



            