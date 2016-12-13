from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import View
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from registro.models import Colector, Empresa, Formulario
from auth_token_middleware.models import Token
from django.contrib.auth import authenticate

# Create your views here.
@login_required
def index(request):
    empresas = Empresa.objects.filter(usuario=request.user)
    return render(request, 'administrador/index.html',{'user':request.user, 'empresas':empresas})
	#return HttpResponse("interfaz principal de la calculadora")

@login_required
def token(request, empresa_id):
    empresas = Empresa.objects.get(pk=empresa_id)
    token = Token.objects.get(empresa = empresa)
    token = token.valor

    #return render(request, 'administrador/index.html',{'user':request.user, 'empresas':empresas, 'token':token})
    #return HttpResponse("interfaz principal de la calculadora")

def dashboard(request):
    empresas = Empresa.objects.filter(usuario=request.user)
    if len(empresas)==1:
        empresa = Empresa.objects.get(usuario=request.user)
        token = Token.objects.get(empresa = empresa)
        token = token.valor
        

    return render(request, 'administrador/admin/index.html',{'user':request.user, 'empresas':empresas, 'token':token})
    #return HttpResponse(empresas)

def reporte(request):
	user = authenticate(username='finantic', password='finantic')
	if user is not None:
	    # the password verified for the user
	    if user.is_active:
	    	
	    	print("User is valid, active and authenticated")
	    	empresas = Empresa.objects.filter(usuario=user)
	    	token=""
	    	empresa={}
	    	notificacion=""
	    	formularios=[]
	    	if len(empresas)==1:
	    		empresa = Empresa.objects.get(usuario=user)
	    		formularios=empresa.formulario.all();
	    		print empresa
	    		token = Token.objects.get(empresa = empresa)
	    		token = token.valor
	    		print token

    		else:
    			notificacion="No hay empresas registradas a este usuario"
			print "ANTES DEL RETURN"
	    	return render(request,'webforms/maintemplate.html',{
				'user':request.user, 
		        'empresas':empresas, 
		        'token':token, 
		        'notificacion':notificacion,
		        'formularios':formularios
		        })
	    else:
	        print("The password is valid, but the account has been disabled!")
	else:
	    # the authentication system was unable to verify the username and password
	    print("The username and password were incorrect.")


#View de test
@login_required
def testview(request):
    empresas = Empresa.objects.filter(usuario=request.user)
    token=""
    empresa={}
    notificacion=""
    formularios=[]

    if len(empresas)==1:
        empresa = Empresa.objects.get(usuario=request.user)
        formularios=empresa.formulario.all();
        print formularios
        token = Token.objects.get(empresa = empresa)
        token = token.valor
    else:
        notificacion="No hay empresas registradas a este usuario"

    return render(request, 'administrador/admin/index_test.html',{
        'user':request.user, 
        'empresas':empresas, 
        'token':token, 
        'notificacion':notificacion,
        'formularios':formularios
        })
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