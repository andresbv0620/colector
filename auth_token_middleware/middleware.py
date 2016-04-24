from django.http import HttpResponse
import json
from auth_token_middleware.models import Token

class AuthToken(object):  
    def process_request(self, request): 
    	service_string = "/service_123456789/" 
    	request_path = str(request.path)
    	resp = {}
    	#validando url solicitada
    	if service_string in request_path:    		
    		
    		#validando recepcion de HTTP_TOKEN
    		try:
    			http_token = request.META['HTTP_TOKEN']

    			
    			#validando que exista el token
    			try:
    				token = Token.objects.get(valor = http_token)
    				#return HttpResponse("token encontrado")
    				return None

    			except Token.DoesNotExist:
    				resp['response_code'] = '400'
                	resp['response_description'] = str('Token not found ')               
                	resp['body_received'] = str(request.body)
                	resp['header_expected'] = str('token')
                	return HttpResponse(json.dumps(resp), content_type= "application/json")

                
    			return HttpResponse(request.META['HTTP_TOKEN'])

    		except Exception as e:
    			resp['response_code'] = '400'
                resp['response_description'] = str('Token not send '+ str(e.args))               
                resp['body_received'] = str(request.body)
                resp['header_expected'] = str('token')
                return HttpResponse(json.dumps(resp), content_type= "application/json")

    	else:
    		pass
    		
        return None 