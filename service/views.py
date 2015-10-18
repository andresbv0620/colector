#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from registro.models import PermisoFormulario, Colector, Formulario
import json
from bson import json_util
import hashlib
import pymongo
import uuid
from datetime import datetime
servidor = pymongo.MongoClient('localhost', 27017)
database = servidor.colector


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
                PermisoFormulario.objects.filter(colectores__usuario__id=colector_id)
            if len(permiso_formularios):
                formularios_array = []
                response_data = {}

                # parseando formularios a json
                resp['response_data'] = []

                for p in permiso_formularios:

                    formulario = {}
                    formulario['form_name'] = p.formulario.nombre
                    formulario['form_id'] = p.formulario.id
                    formulario['form_description'] = p.formulario.descripcion

                    # validando que el formulario tenga fichas asociadas
                    if len(p.formulario.ficha.all()):
                        formulario['sections'] = []
                        for f in p.formulario.ficha.all():
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
                                        entrada['filled_form_attribute'] = []
                                        filled_forms = database.filled_forms.find({"filled_forms.form_id":str(e.form_asociado.id)},
                                            {"filled_forms.form_description":0,
                                            "filled_forms.form_name":0,
                                            "filled_forms.form_description":0,
                                            "filled_forms.fecha_creacion":0,
                                            "filled_forms.sections.description":0,
                                            "filled_forms.sections.name":0,
                                            "filled_forms.sections.section_id":0,
                                            "filled_forms.sections.inputs.type":0,
                                            "filled_forms.sections.inputs.input_id":0,
                                            "filled_forms.sections.inputs.description":0

                                            });
                                        nested_data={}
                                        #agregar id a response y ya

                                        
                                        
                                        for filled in filled_forms:
                                            print filled
                                            # print filled.sections
                                            # for filled_section in filled.sections:
                                            #     for filled_input in filled_section.inputs:
                                            #         nested_data['label']=filled_input.name
                                            #         for filled_response in filled_input.responses:
                                            #             filled_response['label']=nested_data['label']

                                            form_aux = {}
                                            
                                            
                                            entrada['filled_form_attribute'].append(filled) #(json.dumps(f,default=json_util.default))
                                            

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
            resp['response_description'] = str('invalid body request '
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
            colector_id = data['colector_id']
            form_id = data['form_id']
            responses = data['responses']

            array_validation = {}
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
                resp['response_code'] = '200'
                resp['response_description'] = str('OK')
                resp['body_received'] = str(request.body)
                resp['body_expected'] = \
                    str('{"colector_id":"", "form_id":" ", "responses":"[]"  }'
                        )
                resp['response_data'] = request.body

                return HttpResponse(json.dumps(resp),
                                    content_type='application/json')

            # construyendo json para insertar en mongodb


        except Exception, e:

            resp['response_code'] = '400'
            resp['response_description'] = str('invalid body request '
                    + str(e.args))
            resp['body_received'] = str(request.body)
            resp['body_expected'] = \
                str('{"colector_id":"", "form_id":" ", "responses":"[]" }')

            return HttpResponse(json.dumps(resp),
                                content_type='application/json')

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


class FilledFormsReport(View):

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



            