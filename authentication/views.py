from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import hashlib
from django.contrib.auth import authenticate
from registro.models import Colector, Empresa
from auth_token_middleware.models import Token
# Create your views here.

class ColectorAuth(View):    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ColectorAuth, self).dispatch(*args, **kwargs)

    def post(self, request):
        resp = {}

        # validando data del body
        try:
            data = json.loads(request.body)
            #print data['username']
            #print data['password']
            user = authenticate(username = data['username'], password = data['password'])
            #validando que exista un usuario
            if user is not None:
                try:
                    #validando que exista un colector 
                    colector = Colector.objects.get(usuario = user)
                    resp['response_code'] = '200'
                    resp['response_description'] = str('colector found')
                    resp['response_data'] = str(colector.usuario.username)
                    resp['body_received'] = str(request.body)
                    resp['body_expected'] = str('{"username":" ", "password": " "}')

                    return HttpResponse(json.dumps(resp), content_type= "application/json")

                except Colector.DoesNotExist:

                    resp['response_code'] = '404'
                    resp['response_description'] = str('colector not found')
                    resp['body_received'] = str(request.body)
                    resp['body_expected'] = str('{"username":" ", "password": " "}')

                    return HttpResponse(json.dumps(resp), content_type= "application/json")
            else:
                resp['response_code'] = '404'
                resp['response_description'] = str('incorrect username or password')
                resp['body_received'] = str(request.body)
                resp['body_expected'] = str('{"username":" ", "password": " "}')

                return HttpResponse(json.dumps(resp), content_type= "application/json")


        except  Exception as e:             
            resp['response_code'] = '400'
            resp['response_description'] = str('invalid body request '+ str(e.args))
            resp['body_received'] = str(request.body)
            resp['body_expected'] = str('{"username":" ", "password": " "}')


            return HttpResponse(json.dumps(resp), content_type= "application/json") 


class TokenAuth(View):    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(TokenAuth, self).dispatch(*args, **kwargs)

    def post(self, request):
        resp = {}

        # validando data del body
        try:
            data = json.loads(request.body)
            #print data['username']
            #print data['password'

            try:
                empresa = Empresa.objects.get(nombre = str(data['company_name']) , codigo_secreto = str(data['secret_code']))
                
                resp['response_code'] = '200'
                resp['response_description'] = str('Company found')                    
                resp['body_received'] = str(request.body)
                resp['body_expected'] = str('{"company_name":" ", "secret_code": " "}')

                try:

                    token = Token.objects.get(empresa = empresa )
                    resp['response_data'] = []
                    data = {}
                    data['token'] = str(token.valor)
                    resp['response_data'].append(data)
                except Token.DoesNotExist:
                    resp['response_data'] = "Token no creado"

                return HttpResponse(json.dumps(resp), content_type= "application/json")
                #return HttpResponse("empresa encontrada")

            except Empresa.DoesNotExist:
                resp['response_code'] = '404'
                resp['response_description'] = str('company not found')
                resp['body_received'] = str(request.body)
                resp['body_expected'] =str('{"company_name":" ", "secret_code": " "}')

                return HttpResponse(json.dumps(resp), content_type= "application/json")





            #user = authenticate(username = data['username'], password = data['password'])

            #validando que exista un usuario
            #if user is not None:
                #try:

                    #validando que exista un colector 
                   # empresa = Empresa.objects.get(usuario = user)

                   # print empresa
                    #resp['response_code'] = '200'
                   # resp['response_description'] = str('empresa found')
                    
                    #resp['body_received'] = str(request.body)
                    #resp['body_expected'] = str('{"username":" ", "password": " "}')
                    #buscando token
                    #try:
                        #token = Token.objects.get(empresa = empresa )
                        #resp['response_data'] = []
                        #data = {}
                        #data['token'] = str(token.valor)
                        #resp['response_data'].append(data)
                    #exce#pt Token.DoesNotExist:
                        #resp['response_data'] = "Token no creado"

                    #return HttpResponse(json.dumps(resp), content_type= "application/json")

                #except Empresa.DoesNotExist:

                    #resp['response_code'] = '404'
                   # resp['response_description'] = str('empresa not found')
                    #resp['body_received'] = str(request.body)
                   # resp['body_expected'] = str('{"username":" ", "password": " "}')

                   # return HttpResponse(json.dumps(resp), content_type= "application/json")
            #else:
               # resp['response_code'] = '404'
                #resp['response_description'] = str('incorrect username or password')
               # resp['body_received'] = str(request.body)
                #resp['body_expected'] = str('{"username":" ", "password": " "}')

                #return HttpResponse(json.dumps(resp), content_type= "application/json")


        except  Exception as e:             
            
            resp['response_code'] = '400'
            resp['response_description'] = str('invalid body request '+ str(e.args))
            resp['body_received'] = str(request.body)
            resp['body_expected'] = str('{"company_name":" ", "secret_code": " "}')


            return HttpResponse(json.dumps(resp), content_type= "application/json")
