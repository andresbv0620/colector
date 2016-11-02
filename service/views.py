#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
from django.core.mail import send_mail
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
from bson.objectid import ObjectId
import uuid
import collections
from datetime import datetime
import time
import codecs
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import xlsxwriter

from . import tasks as celery_tasks

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

    def filterColector(self, colector_id):
        colector = Colector.objects.get(usuario = colector_id)
        print 'COLECTOR FILTRADO RESPUESTAS'
        if len(colector.respuesta.all()):
            respuestascolector = []
            for r in colector.respuesta.all():
                respuesta = {}
                respuesta['response_id'] = r.id
                respuesta['value'] = r.valor
                respuestascolector.append(respuesta)
            return respuestascolector




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
                    if not p.formulario.titulo_reporte:
                        formulario['titulo_reporte'] = 0                   
                    else:
                        formulario['titulo_reporte'] = p.formulario.titulo_reporte.id

                    if not p.formulario.titulo_reporte2:
                        formulario['titulo_reporte2'] = 0                   
                    else:
                        formulario['titulo_reporte2'] = p.formulario.titulo_reporte2.id
                        
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
                                        document_filled_forms = database.filled_forms.find({"form_id":str(formasociado.form_asociado.id)});
                                        arrayChecker=[]
                                        for record in document_filled_forms:
                                            if record['form_id']!=str(formasociado.form_asociado.id):
                                                pass
                                            else:
                                                record["rows"]["record_id"]=str(record["rows"]["record_id"])

                                                #La siguiente linea crea el nodo formula para hacer el calculo del valor de cada producto SOLO EN ORDEN VENTA
                                                #Se debe ajustar para que sea dinamico y sea extensible a otras funcionalidades
                                                #Deja estatico el valor del iva en 0,16
                                                
                                                #print record["responses"]
                                                #Se itera sobre la opcion para sacar las variables de cada formula
                                                precioProducto=0
                                                ivaProducto=0
                                                for option_response in record["responses"]:
                                                    if option_response['tipo'] == "3" or option_response['tipo'] == "4" or option_response['tipo'] == "5":
                                                        try:
                                                            response_id=option_response['value']
                                                            respuesta = Respuesta.objects.get(id = int(response_id))
                                                            option_response['value']=respuesta.valor
                                                        except Exception, e:
                                                            option_response['value']="Op_" + option_response['value']
                                                    
                                                    if option_response["label"]=="_PRECIO":
                                                        precioProducto=option_response["value"]
                                                                                                               

                                                    if option_response["label"]=="_IVA":
                                                        ivaProducto=option_response["value"]

                                                #Crea el nodo opciones en base a el registro en mongodb
                                                optionsObject={}                                                                                                                   
                                                optionsObject["formula"]='('+str(precioProducto)+'*<cantidad>)+('+str(precioProducto)+'*<cantidad>*'+str(ivaProducto)+')'

                                                optionsObject['responses'] = record['responses']
                                                optionsObject['Hora Fin'] = record['rows']['Hora Fin']
                                                optionsObject['Hora Inicio'] = record['rows']['Hora Inicio']
                                                optionsObject['record_id'] = record['rows']['record_id']
                                                optionsObject['form_id'] = record['form_id']

                                                entrada['options'].append(optionsObject) #(json.dumps(f,default=json_util.default))


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

                                    ###########CONDICIONAL PARA TQ##################
                                    if e.id == 543:
                                        entrada['responses'] = []
                                        entrada['responses'] = self.filterColector(colector_id)
                                        colector = Colector.objects.get(usuario = colector_id)
                                        formulario['form_description'] = str(colector)
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

#Guarda una estructura simple de las respuestas, colector_id, form_id, rows{} las respuestas no estan referenciadas estan embebidas en rows y se hace referencia al colector id
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
            #response['error'] = True
            response['validation_errors'].append('latitud is blank')

        if not array_validation['longitud'].strip():
            #response['error'] = True
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

    ####EXCLUSIVO PARA TECNOQUIMICAS####
    def tecnoquimica_cols(self, tqformid2, colector_id):
        tqobjs = database.filled_forms.find({"$and":[ {'form_id': tqformid2}, {'colector_id': str(colector_id)}]})
        tqarray = []
        for tqobj in tqobjs:
            for respuesta in tqobj['responses']:
                tqarray.append(respuesta)
        return tqarray
    ####EXCLUSIVO PARA TECNOQUIMICAS####

    def post(self, request):
        resp = {}
        # validando data correcta enviada en body
        try:
            data = json.loads(request.body)
            if 'longitud' not in data:
                data['latitud']='0.0'
                data['longitud']='0.0'
            
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
                rows = {}
                rows['colector_id'] = colector_id
                rows['sincronizado_utc'] = datetime.utcnow()
                #rows['sincronizado'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                rows['Sincronizado'] = datetime.now().strftime("%Y-%m-%d")
                rows['Hora Sincronizado'] = datetime.now().strftime("%H:%M:%S")
                rows['record_id']=str(uuid.uuid4())
                rows['longitud'] = longitud
                rows['latitud'] = latitud
                rows['Hora Inicio'] = horaini
                rows['Hora Fin'] = horafin
                rows['form_id'] = form_id
                formulario = Formulario.objects.get(id = int(form_id))
                rows['form_name'] = formulario.nombre
                rows['form_description'] = formulario.descripcion

                newresponses = []
                for response in responses:
                    if response['value'] == "99270":
                        resp={}
                        # return HttpResponse("colector existe")
                        resp['response_code'] = '202'
                        resp['response_description'] = str('Registro en edicion')
                        resp['body_received'] = str(request.body)
                        resp['body_expected'] = \
                            str('{"colector_id":"", "form_id":" ", "responses":"[]"  }')
                        resp['response_data'] = request.body
                        return HttpResponse(json.dumps(resp),content_type='application/json')

                    input_id=response['input_id']
                    entrada = Entrada.objects.get(id = int(input_id))
                    response['label']=entrada.nombre
                    response['tipo']=entrada.tipo

                ####EXCLUSIVO PARA TECNOQUIMICAS####
                tqformid = '29'
                tqformid2 = '30'
                if form_id == tqformid:
                    aditionalcols = []
                    aditionalcols = self.tecnoquimica_cols(tqformid2, colector_id)
                    rep = User.objects.get(id=int(colector_id))
                    aditionalcols[0]['value'] = str(rep.first_name) +' '+ str(rep.last_name)
                    #aditionalcols.extend(responses)
                    responses.insert(0, aditionalcols[0])
                    responses.insert(0, aditionalcols[1])
                    responses.insert(0, aditionalcols[2])

                ####EXCLUSIVO PARA TECNOQUIMICAS####

                
                colector = \
                    database.filled_forms.find_one({'colector_id': str(colector_id)},
                        {'colector_id': 1})                

                # validando si existe un colector con esta id
                if colector == None:
                    print 'EL COLECTOR NO EXISTE en mongo'
                else:
                    print "El colector existe en mongo"

                data = {}
                data['colector_id'] = colector_id
                data['form_id'] = form_id
                data['rows'] = rows
                data['responses'] = responses
                
                #Se crean los indices para agilizar la consulta
                database.filled_forms.insert(data)
                database.filled_forms.create_index("form_id")
                database.filled_forms.create_index("colector_id")
                database.filled_forms.create_index("rows.record_id")

                #Enviar correo
                # imgurl="https://www.google.com.co/url?sa=t&rct=j&q=&esrc=s&source=web&cd=13&ved=0ahUKEwiDpKa52MnOAhUFXB4KHUTXADAQ8g0ITjAM&url=%2Fimgres%3Fimgurl%3Dhttps%3A%2F%2Fmedia.licdn.com%2Fmedia%2FAAEAAQAAAAAAAAbLAAAAJDUwOGQwN2QyLTA3ZGItNDcwNC1iN2E0LTY3ZTMwNzU4NzFlMQ.png%26imgrefurl%3Dhttps%3A%2F%2Fco.linkedin.com%2Fin%2Fandresbuitragof%26h%3D60%26w%3D60%26tbnid%3DwQK4SDF_D_ZGwM%26tbnh%3D60%26tbnw%3D60%26usg%3D__MLhkybNYaV66vDO9_vYV3iEjml0%3D%26docid%3D3a3EOf0w3y46iM&usg=AFQjCNFVRPhV_yTXa_ayXRanGcemGHBiqw&sig2=FjcBKuVJSLWHhOW5ScVeVQ"
                # imgalt = "alternativa"
                # useremail = "andresbuitragof@gmail.com"

                # subject_email="Nuevo carro publicado"
                # message_email="""
                # Encontramos el siguiente carro %s
                # """ %formulario.descripcion
                # from_email="andres@adiktivo.com"
                # to_email=[useremail,"andresbuitragof@gmail.com"]
                # html_email="""
                # <h1>Buenas noticias</h1>

                # <div class='container'>
                #     <div class='row'>
                #             <div class='col-sm-6 col-md-3 col-lg-3'>
                #                 <div class='thumbnail'>
                #                     <img src='"""+imgurl+"""' alt='"""+imgalt+"""' width='150px'>
                #                     <div class='caption'>
                #                         <h3>$ 0000</h3>
                #                         <p>asdf</p>
                #                     </div>
                #                 </div>
                #             </div>
                #     </div>
                # </div>
                # """
                # send_mail(
                #     subject_email,
                #     message_email,
                #     from_email,
                #     to_email,
                #     html_message=html_email,
                #     fail_silently=False,
                # )

            

                    # return HttpResponse("colector existe")
                resp['response_code'] = '200'
                resp['response_description'] = str('form filled')
                resp['body_received'] = str(request.body)
                resp['record_id'] = rows['record_id']
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
            #activar la siguiente linea para probar local y  a .open() quitar default storage
            #file_path='/home/andres/media/'+name+'.'+extension

            #Agregar default_storage.open para usar django-storages (aws s3) y activar la siguiente linea
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
            #Quitar default_storage para probar local
            csvFile = default_storage.open(file_path)
            #csvFile = open('example.csv')
            csvReader = csv.reader(csvFile, delimiter=';')
            #csvData = list(csvReader)
        except Exception, e:
            return str('No se encuentra el archivo en el servidor'
                    + str(e.args)) + str(input_id)

        records_counter=0
        for row in csvReader:
            print('Row #' + str(csvReader.line_num) + ' ' + str(row))
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
                rows = {}
                rows['colector_id'] = colector_id
                rows['Sincronizado'] = datetime.now().strftime("%Y-%m-%d")
                rows['Hora Sincronizado'] = datetime.now().strftime("%H:%M:%S")
                rows['sincronizado_utc'] = datetime.utcnow()
                rows['record_id']=str(uuid.uuid4())
                rows['Hora Inicio'] = datetime.utcnow()
                rows['Hora Fin'] = datetime.utcnow()
                rows['form_id'] = form_id
                formulario = Formulario.objects.get(id = int(form_id))
                rows['form_name'] = formulario.nombre
                rows['form_description'] = formulario.descripcion

                responsesArray=[]
                for rowvalue in row:
                    index = row.index(rowvalue)
                    inputObject=inputsList[index]
                    inputObject['value'] = rowvalue

                    if element_longitud != None and inputObject['input_id']==element_longitud:
                        rows['longitud'] = rowvalue
                    else:
                        rows['longitud'] = "0.0"

                    if element_latitud != None and inputObject['input_id']==element_latitud:
                        rows['latitud'] = rowvalue
                    else:
                        rows['latitud'] = "0.0"


                colector = database.filled_forms.find_one({'colector_id': str(colector_id)},{'_id': 0})                

                # validando si existe un colector con esta id
                if colector == None:
                    print 'EL COLECTOR NO EXISTE en mongo'
                else:
                    print "El colector existe en mongo"
                
                records_counter+=1
                data = {}
                #####CONDICIONAL PARA TQ PARA REESTABLECER DEJAR SOLO EL ELSE######
                if form_id=='30':
                    data['colector_id'] = row[0]
                else:
                    data['colector_id'] = colector_id
                data['form_id'] = form_id
                data['rows'] = rows
                data['responses'] = inputsList
                
                #Se crean los indices para agilizar la consulta
                database.filled_forms.insert(data)
                database.filled_forms.create_index("form_id")
                database.filled_forms.create_index("colector_id")
                database.filled_forms.create_index("rows.record_id")


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

                #Colocar este condicional para aumentar seguridad, sedebe crear un grupo de administradores
                print user
                if user.groups.filter(name='administrador'):
                    database.filled_forms.remove({'_id': ObjectId(str(record_id))})
                    print 'removed'
                
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

class RegisterUsersCsv(UploadData, View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(RegisterUsersCsv, self).dispatch(*args, **kwargs)

    def insert_file_records(self, file_path, form_id, colector_id, element_longitud, element_latitud):
        try:
            #Quitar default_storage para probar local
            csvFile = default_storage.open(file_path)
            #csvFile = open('example.csv')
            csvReader = csv.reader(csvFile, delimiter=';')
            #csvData = list(csvReader)
        except Exception, e:
            return str('No se encuentra el archivo en el servidor'
                    + str(e.args)) + str(input_id)

        records_counter=0
        for row in csvReader:
            print('Row #' + str(csvReader.line_num) + ' ' + str(row))
            userObject = {}
            userObject['username']=row[0]
            userObject['email']=row[1]
            userObject['password']=row[2]

            user = User.objects.create_user(userObject['username'], userObject['email'], userObject['password'])
            records_counter+=1
            # construyendo json para insertar en mongodb
             
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

#Reporte pagina directamente sobre django usando el paginador de bootstrat table
def FormIdReportPagServerConsulta(id, colector_id, limit, page, lastid, *args, **kwargs):
    if colector_id==None and page==1:
        return database.filled_forms.find({'form_id': str(id)}).limit(limit).sort("_id",-1)
    elif colector_id!=None and page==1:
        return database.filled_forms.find({"$and":[ {'form_id': str(id)}, {'colector_id': str(colector_id)}]}).limit(limit).sort("_id",-1)

    if colector_id==None and page!=1:
        return database.filled_forms.find({'form_id': str(id), '_id':{"$lt": ObjectId(lastid)}}).limit(limit).sort("_id",-1)
    else:
        return database.filled_forms.find({"$and":[ {'form_id': str(id)}, {'colector_id': str(colector_id)}], '_id':{"$lt": ObjectId(lastid)}}).limit(limit).sort("_id",-1)

def FormIdReportPagServer(request, id):
    #Ejecuta esto para obtener los headers o columnas de la tabla, el controller llama este servicio con el parametro getcolumns=true
    getcolumns=request.GET.get('getcolumns')

    if getcolumns=='true':
        colrows = database.filled_forms.find_one({'form_id': str(id)})
        if colrows!=None:
            columns=[]
            for cell in colrows["responses"]:
                column={}
                column['field']=cell['label']
                column['sortable'] = 'true'
                column['title']=cell['label']
                column['filterControl'] = "input"
                if column not in columns:
                    columns.append(column)

            for row in colrows["rows"]:
                column={}
                column['field']=row
                column['sortable'] = 'true'
                column['title']=row
                column['filterControl'] = "input"
                
                if column not in columns:
                    if cell['label'] == 'Sincronizado':
                        column['filterControl'] = "select"
                    else:
                        column['filterControl'] = "select"
                    columns.append(column)

            ########################CONSULTANDO COLECTOR IDS##################3
            form_id = int(id)
            empresas = Formulario.objects.get(id=form_id).empresa_set.all()
            for empresa in empresas:
                empresa = empresa

            #Colocar este condicional para aumentar seguridad, sedebe crear un grupo de administradores
            #if user.groups.filter(name='administrador'):
            colectors = []
            for colectorindjango in empresa.colector.all():
                colectorinmongo = database.filled_forms.find_one({'colector_id': str(colectorindjango.id)}, {'_id': 1})                
                # validando si existe un colector con esta id
                if colectorinmongo != None:
                    colectorObj={}
                    colectorObj['colector_id'] = colectorindjango.id
                    usuario = User.objects.get(id=colectorindjango.id)
                    colectorObj['colector_name'] = usuario.username
                    colectors.append(colectorObj)

            #colectors = [{'colector_id':1,'colector_name':'Andres'},{'colector_id':2,'colector_name':'Migue'}]

            data={
                'columns': columns,
                'colectors':colectors
                }
            return HttpResponse(json.dumps(data, default=json_util.default), content_type='application/json')
        else:
            resp={}
            resp['columns'] = []
            resp['response_code'] = '404'
            resp['response_description'] = 'No hay registros'
            return HttpResponse(json.dumps(resp, default=json_util.default), content_type='application/json')
    #Setting Pagination
    offset=int(request.GET.get('offset', 10))
    limit=int(request.GET.get('limit', 10))
    #sumo divido el offset entre el limit y sumo 1 porque en django se usa el parametro pagina no offset y la paginacion no empieza desde 0, empieza desde 1
    page=(int(request.GET.get('offset', 0)))/limit+1
    #filled_forms = database.filled_forms.find({'form_id': str(id)}, {'_id': 0})
    colector_id=request.GET.get('colector_id')

    lastid=0

    if page == 1:
        filled_forms = FormIdReportPagServerConsulta(id, colector_id, limit, page, lastid)
        request.session['colector_'+str(colector_id)] = filled_forms.count()
    else:
        lastid = str(request.session[str(page-1)])
        filled_forms = FormIdReportPagServerConsulta(id, colector_id, limit, page, lastid)
        #filled_forms = database.filled_forms.find({'form_id': str(id), '_id':{"$lt": ObjectId(lastid)}}).limit(limit).sort("_id",-1)
        #filled_forms = database.filled_forms.find({"$and":[ {'form_id': str(id)}, {'colector_id': str(colector_id)}], '_id':{"$lt": ObjectId(lastid)}}).limit(limit).sort("_id",-1)

    data = {}
    #Si hay registros realizo preparo la respuesta http, iterating on filled_forms
    if filled_forms.count() != 0:
        rows = []#rows array que contiene las filas de la tabla
        #Below f is a document (a record)
        for f in filled_forms:
            f["rows"]["MongoId"]=str(f["_id"])
            #rows.append(f["rows"])#list of records
            mongoid= str(f["_id"])
            request.session[str(page)] = mongoid

            ############ESTO DEMUESTRA QUE SE PUEDE SIMPLIFICAR EL SERVICIO PARA SINCRONIZAR REGISTROS, ESTA CARGA SE PUEDE PASAR AQUI
            # ##LA OTRA FORMA DE HACERLO, ES CONSULTAR DIRECTAMENTE EL NODO ROWS
            row = f["rows"]
            formulario = Formulario.objects.get(id = int(id))
            row['form_name'] = formulario.nombre
            row['form_description'] = formulario.descripcion
            for response in f["responses"]:
                #input_id=response['input_id']
                #entrada = Entrada.objects.get(id = int(input_id))
                #response['label']=entrada.nombre
                #response['tipo']=entrada.tipo
                if response['tipo'] == "1" or response['tipo'] == "2":
                    row[response['label']]=response['value'].upper()

                if response['tipo'] == "3" or response['tipo'] == "4" or response['tipo'] == "5":
                    try:
                        response_id=response['value']
                        respuesta = Respuesta.objects.get(id = int(response_id))
                        row[response['label']]=respuesta.valor
                    except Exception, e:
                        row[response['label']]="Op_" + response['value']

                if response['tipo'] == "7" or response['tipo'] == "8" or response['tipo'] == "9" or response['tipo'] == "10" or response['tipo'] == "11" or response['tipo'] == "12" or response['tipo'] == "13" or response['tipo'] == "15" or response['tipo'] == "17":
                    row[response['label']]=response['value']
                #FOTOS TIENEN UN TAG ADICIONAL A FOTOS Y DOCUMENTOS
                if response['tipo'] == "6":
                    #src='/home/andres/media/'+response['value']
                    #src='https://s3-us-west-2.amazonaws.com/colector.co/media/'+str(response.id)+'/'+response['value']
                    #fileext = response['value'].split("_.",1)[1]
                    fid, tagfoto, tipoarchivo, fechafoto, algo, fileext = response['value'].split('_')

                    src=settings.MEDIA_URL+str(response['input_id'])+'/'+response['value']+fileext
                    static_url=settings.STATIC_URL
                    if response['label'] in row:
                        row[response['label']]=row[response['label']]+'<div style="float:left"><a class="thumb"><img onClick="openMedia()" id="'+src+'" width="50px" height="50px" src="'+static_url+'administrador/admin/dist/img/avatar.png" data-err-src="'+static_url+'administrador/admin/dist/img/avatar.png"/><p>'+tagfoto+'</p></a></div>'
                    else:
                        row[response['label']] = '<div style="float:left"><a class="thumb"><img onClick="openMedia()" id="'+src+'" width="50px" height="50px" src="'+static_url+'administrador/admin/dist/img/avatar.png" data-err-src="'+static_url+'administrador/admin/dist/img/avatar.png"/><p>'+tagfoto+'</p></a></div>'

                if response['tipo']=="14" or response['tipo']=="16":
                    #src='/home/andres/media/'+response['value']
                    #src='https://s3-us-west-2.amazonaws.com/colector.co/media/'+str(entrada.id)+'/'+response['value']
                    #fileext = response['value'].split("_.",1)[1]
                    fid, tipoarchivo, fechafoto, algo, fileext = response['value'].split('_')

                    src=settings.MEDIA_URL+str(response['input_id'])+'/'+response['value']+fileext
                    static_url=settings.STATIC_URL
                    if response['label'] in row:
                        row[response['label']]=row[response['label']]+'<div style="float:left"><a class="thumb"><img onClick="openMedia()" id="'+src+'" width="50px" height="50px" src="'+static_url+'administrador/admin/dist/img/avatar.png" data-err-src="'+static_url+'administrador/admin/dist/img/avatar.png"/></a></div>'
                    else:
                        row[response['label']] = '<div style="float:left"><a class="thumb"><img onClick="openMedia()" id="'+src+'" width="50px" height="50px" src="'+static_url+'administrador/admin/dist/img/avatar.png" data-err-src="'+static_url+'administrador/admin/dist/img/avatar.png"/></a></div>'
                
            rows.append(row)#list of records

    else:
        print 'NO HAY REGISTROS'
        data['response_code'] = '404'
        data['response_description'] = 'No hay registros'
        data['rows'] = []
        data['total'] = 0
        return HttpResponse(json.dumps(data, default=json_util.default), content_type='application/json')

    data={
            "total": request.session['colector_'+str(colector_id)],
            "rows": rows,
        }

    return HttpResponse(json.dumps(data, default=json_util.default), content_type='application/json')

#Permite precargar registros en un formulario con datos desde un archivo plano
def FormExcelReport(request, id):

    filled_forms=database.filled_forms.find({'form_id': str(id)}).sort("_id",-1)

    # Si hay registros realizo preparo la respuesta http, iterating on filled_forms
    if filled_forms.count() != 0:
        # rows = [] # rows array que contiene las filas de la tabla
        # # Below f is a document (a record)
        # for f in filled_forms:
        #     f["rows"]["MongoId"]=str(f["_id"])
        #     # rows.append(f["rows"])#list of records
        #     mongoid = str(f["_id"])
        #
        #     ############ ESTO DEMUESTRA QUE SE PUEDE SIMPLIFICAR EL SERVICIO PARA SINCRONIZAR REGISTROS, ESTA CARGA SE PUEDE PASAR AQUI
        #     # ## LA OTRA FORMA DE HACERLO, ES CONSULTAR DIRECTAMENTE EL NODO ROWS
        #     row = f["rows"]
        #     formulario = Formulario.objects.get(id = int(id))
        #     row['form_name'] = formulario.nombre
        #     row['form_description'] = formulario.descripcion
        #     for response in f["responses"]:
        #         # input_id=response['input_id']
        #         # entrada = Entrada.objects.get(id = int(input_id))
        #         # response['label']=entrada.nombre
        #         # response['tipo']=entrada.tipo
        #         if response['tipo'] == "1" or response['tipo'] == "2":
        #             row[response['label']] = response['value'].upper()
        #
        #         if response['tipo'] == "3" or response['tipo'] == "4" or response['tipo'] == "5":
        #             try:
        #                 response_id=response['value']
        #                 respuesta = Respuesta.objects.get(id = int(response_id))
        #                 row[response['label']]=respuesta.valor
        #             except Exception, e:
        #                 row[response['label']]="Op_" + response['value']
        #
        #         if response['tipo'] == "7" or response['tipo'] == "8" or response['tipo'] == "9" or response['tipo'] == "10" or response['tipo'] == "11" or response['tipo'] == "12" or response['tipo'] == "13" or response['tipo'] == "15" or response['tipo'] == "17":
        #             row[response['label']]=response['value']
        #         # FOTOS TIENEN UN TAG ADICIONAL A FOTOS Y DOCUMENTOS
        #         if response['tipo'] == "6":
        #             # src='/home/andres/media/'+response['value']
        #             # src='https://s3-us-west-2.amazonaws.com/colector.co/media/'+str(response.id)+'/'+response['value']
        #             # fileext = response['value'].split("_.",1)[1]
        #             fid, tagfoto, tipoarchivo, fechafoto, algo, fileext = response['value'].split('_')
        #
        #             src=settings.MEDIA_URL+str(response['input_id'])+'/'+response['value']+fileext
        #             static_url=settings.STATIC_URL
        #             if response['label'] in row:
        #                 row[response['label']]=row[response['label']]+'<div style="float:left"><a class="thumb"><img onClick="openMedia()" id="'+src+'" width="50px" height="50px" src="'+static_url+'administrador/admin/dist/img/avatar.png" data-err-src="'+static_url+'administrador/admin/dist/img/avatar.png"/><p>'+tagfoto+'</p></a></div>'
        #             else:
        #                 row[response['label']] = '<div style="float:left"><a class="thumb"><img onClick="openMedia()" id="'+src+'" width="50px" height="50px" src="'+static_url+'administrador/admin/dist/img/avatar.png" data-err-src="'+static_url+'administrador/admin/dist/img/avatar.png"/><p>'+tagfoto+'</p></a></div>'
        #
        #         if response['tipo'] == "14" or response['tipo'] == "16":
        #             # src='/home/andres/media/'+response['value']
        #             # src='https://s3-us-west-2.amazonaws.com/colector.co/media/'+str(entrada.id)+'/'+response['value']
        #             # fileext = response['value'].split("_.",1)[1]
        #             fid, tipoarchivo, fechafoto, algo, fileext = response['value'].split('_')
        #
        #             src=settings.MEDIA_URL+str(response['input_id'])+'/'+response['value']+fileext
        #             static_url=settings.STATIC_URL
        #             if response['label'] in row:
        #                 row[response['label']]=row[response['label']]+'<div style="float:left"><a class="thumb"><img onClick="openMedia()" id="'+src+'" width="50px" height="50px" src="'+static_url+'administrador/admin/dist/img/avatar.png" data-err-src="'+static_url+'administrador/admin/dist/img/avatar.png"/></a></div>'
        #             else:
        #                 row[response['label']] = '<div style="float:left"><a class="thumb"><img onClick="openMedia()" id="'+src+'" width="50px" height="50px" src="'+static_url+'administrador/admin/dist/img/avatar.png" data-err-src="'+static_url+'administrador/admin/dist/img/avatar.png"/></a></div>'
        #
        #     rows.append(row) # list of records
        celery_proccess = celery_tasks.generate_xls_report.apply_async((id,request.user.email))

        print 'NO HAY REGISTROS'
        data = {}
        data['response_code'] = '200'
        data['response_description'] = 'El reporte se esta procesando cuando este listo enviaremos una url de descarga al correo %s' % request.user.email
        data['rows'] = []
        data['total'] = 0
        return HttpResponse(json.dumps(data, default=json_util.default), content_type='application/json')
    else:
        print 'NO HAY REGISTROS'
        data = {}
        data['response_code'] = '404'
        data['response_description'] = 'No hay registros'
        data['rows'] = []
        data['total'] = 0
        return HttpResponse(json.dumps(data, default=json_util.default), content_type='application/json')

    # Create a workbook and add a worksheet.
    exceltimestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    excelfilename = str(id)+'_'+str(exceltimestamp)+'.xlsx'

    workbook = xlsxwriter.Workbook('reporttq.xlsx')
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})

    # Add a number format for cells with money.
    money = workbook.add_format({'num_format': '$#,##0'})


    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    # Iterate over the data and write it out row by row.
    for record in rows:
        for recordnode in record:
            if recordnode == 'latitud' or recordnode == 'longitud'\
             or recordnode == 'form_id' or recordnode == 'form_description'\
              or recordnode == 'MongoId' or recordnode == 'Hora Inicio' or recordnode == 'Hora Fin'\
               or recordnode == 'record_id' or recordnode == 'sincronizado_utc' or recordnode == 'colector_id':
               continue
            # Adjust the column width.
            worksheet.set_column(col, col, 30)
            if row == 0:
                worksheet.write(row, col, recordnode, bold)
                col += 1
            else:
                worksheet.write(row, col, record[recordnode])
                col += 1
        row+=1
        col=0

    # Write a total using a formula.
    #worksheet.write(row, 0, 'Total')
    #worksheet.write(row, 1, '=SUM(B1:B4)')

    workbook.close()

    celery_tasks.add.apply_async((2, 2))

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
    response.write(excelfilename)
    return response

