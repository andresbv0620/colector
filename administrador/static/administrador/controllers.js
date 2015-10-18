/**
 * Created by jhon on 24/01/15.
 */

 /*app.controller("FirstController", ['$scope','$http',function($scope,$http){

    $scope.json=;
    $scope.posts=[];
    $scope.newPost={};
    $http.get("http://jsonplaceholder.typicode.com/posts")
      .success(function(data){
        console.log(data);
        $scope.posts=data;
      })
      .error(function(err){

      });
    $scope.addPost=function(){
      $http.post("http://jsonplaceholder.typicode.com/posts",{
        title:$scope.newPost.title,
        body:$scope.newPost.body,
        userId: 1
      })
      .success(function(data,status,headers,config){
        $scope.posts.push($scope.newPost);
        $scope.newPost={}
        

      })
      .error(function(error,status,headers,config){
        console.log(error);

      });
    }

 }]);*/

app.controller('llenarFormulario',['$scope','$routeParams','defaultService','globales',function($scope,$routeParams,defaultService,globales){
  $scope.form_id=$routeParams.form_id;
  $scope.newFilledForm={}
  defaultService.post(globales.static_url+'../service/form/single/','{"form_id":"'+$routeParams.form_id+'"}', function(data){
     //console.log(d)
     $scope.formulario=data['response_data'][0];
     /*form_name=data['response_data'][0].name;
     form_description=data['response_data'][0].description;
     form_id=data['response_data'][0].id;
     form_sections=data['response_data'][0].sections;*/
  }, function (error){console.log(error)});

  $scope.enviarFormulario=function(){
    formularioObject=$scope.formulario;
    formularioObject.colector_id=globales.user_id;
    formularioObject.form_id=formularioObject.form_id.toString();

    console.log(formularioObject);
    defaultService.post(globales.static_url+'../service/fill/form/',formularioObject, function(data){
      console.log(data);

    }, function (error){console.log(error)});
  }
}]);

app.controller('reporteColector', ['$scope', 'defaultService', 'globales', function ($scope, defaultService, globales) {
   console.log("iniciando controlador");

   
   defaultService.get(globales.static_url+'../service/filled/forms/report/colector/4/', function(data){
           //console.log(d)
           console.log("datos reporte recibidos del servidor: ");

           //console.log(data);
           colectorfilledforms = data['data'];
           $scope.colectorid=colectorfilledforms[0].colector_id;
           filledforms=colectorfilledforms[0].filled_forms;
           $scope.filledforms=filledforms;

                    
           tableheader=[];            
           columns=new Array(); 
           data=new Array();
           tablecontent=new Object();


           for (form in filledforms){
              sections=filledforms[form].sections;
              for (section in sections){
                inputs=sections[section].inputs;
                datacolumns= new Object();  
                for (input in inputs){
                  column=new Object();
                  if(tableheader.indexOf(inputs[input].name)<0){
                    column['field']=inputs[input].name;
                    column['sortable']=true;
                    column['title']=inputs[input].name;
                    columns.push(column);
                    tableheader.push(inputs[input].name);
                  }
                  respuestas=new Array();
                  responses=inputs[input].responses;
                  for (response in responses) {
                    respuestas.push(responses[response].value);
                    datacolumns[inputs[input].name]=responses[response].value;
                  }
                }
              }
              data.push(datacolumns);
            }
            
            tablecontent['columns']=columns;
            tablecontent['data']=data;

            $scope.tableheaders=tableheader;
           $('#table').bootstrapTable(tablecontent);

        }, function (error){console.log(error)});
}]);




app.controller('reporteFormulario', ['$scope', 'defaultService', 'globales', function ($scope, defaultService, globales) {

     


   
   defaultService.get(globales.static_url+'../service/filled/forms/report/formname/formularioBasico/', function(data){
           //console.log(d)
           //console.log("datos recibidos del servidor: ");

           //console.log(data);
           colectorfilledforms = data['data'];
           $scope.colectorid=colectorfilledforms[0].colector_id;
           filledforms=colectorfilledforms[0].filled_forms;
           $scope.filledforms=filledforms;

                    
           tableheader=[];            
           columns=new Array(); 
           data=new Array();
           tablecontent=new Object();


           for (form in filledforms){
              sections=filledforms[form].sections;
              for (section in sections){
                inputs=sections[section].inputs;
                datacolumns= new Object();  
                for (input in inputs){
                  column=new Object();
                  if(tableheader.indexOf(inputs[input].name)<0){
                    column['field']=inputs[input].name;
                    column['sortable']=true;
                    column['title']=inputs[input].name;
                    columns.push(column);
                    tableheader.push(inputs[input].name);
                  }
                  respuestas=new Array();
                  responses=inputs[input].responses;
                  for (response in responses) {
                    respuestas.push(responses[response].value);
                    datacolumns[inputs[input].name]=responses[response].value;
                  }
                }
              }
              data.push(datacolumns);
            }
            
            tablecontent['columns']=columns;
            tablecontent['data']=data;

            $scope.tableheaders=tableheader;
           $('#table').bootstrapTable(tablecontent);

        }, function (error){console.log(error)});
}]);

//////////////////////////////////////////////////////////////

app.controller('startApp', ['$scope', 'defaultService', function ($scope, defaultService) {
 console.log("start"); 
 $scope.version ="1.0";    
}]);


app.controller('perfil', ['$scope', 'defaultService', function ($scope, defaultService) {
 console.log("cargando perfil");
 $scope.cargar_perfil = function(){
 	defaultService.get('/service/perfil/detail/'+$scope.id_usuario+'/',function(d){
           //console.log(d)
           $scope.titular_cuenta = d.Titular_cuenta_bancaria;
           $scope.pais = d.pais;
           $scope.ciudad = d.ciudad;
           $scope.banco = d.banco;
           $scope.numero_cuenta = d.numero_cuenta;
           //alert($scope.titular_cuenta);
        }, function (e){console.log(e)
    });

 }

    $scope.cargar_perfil();

    $scope.modificar_perfil = function(){
    	var data = {
    		"Titular_cuenta_bancaria": $scope.titular_cuenta,
		    "banco": $scope.banco ,
		    "numero_cuenta": $scope.numero_cuenta,
		    "pais": $scope.pais,
		    "ciudad": $scope.ciudad
    	};
    	   
           console.log(data);
           //alert($scope.titular_cuenta);
           defaultService.put('/service/perfil/detail/'+$scope.id_usuario+'/',data,function(d){
           console.log(d)
           $scope.titular_cuenta = d.Titular_cuenta_bancaria;
           $scope.pais = d.pais;
           $scope.ciudad = d.ciudad;
           $scope.banco = d.banco;
           $scope.numero_cuenta = d.numero_cuenta;
           alert("Datos modificados con exito");
        }, function (e){console.log(e)
    });
    	  

    	
    }
    
  

    defaultService.get('/service/tienda/list/',function(d){
           console.log("linea 19 cargando perfil");
           $scope.tiendas = d;
          
        }, function (e){console.log(e)
    });


    $scope.btn_tiendas = function(){
    	console.log("linea 27 btn_tiendas")
    	defaultService.get('/service/perfil/detail/'+$scope.id_usuario+'/',function(data){
					           
					           $scope.tiendas_incluidas = data.tienda;     
					          
					        }, function (e){console.log(e)
					    });
    }



    $scope.incluir_tienda = function(id){
    	//alert(id);
    	var tiendas = [];
    	defaultService.get('/service/perfil/detail/'+$scope.id_usuario+'/',function(d){
           
           tiendas = d.tienda;

           if(tiendas.length == 0){
           	tiendas[0] = id;
           	defaultService.put('/service/perfil/detail/'+$scope.id_usuario+'/', d ,function(data){
					          console.log("linea 48 incluyendo tiendas");      
					           defaultService.get('/service/perfil/detail/'+$scope.id_usuario+'/',function(data){
					           
					           $scope.tiendas_incluidas = data.tienda;     
					          
							        }, function (e){console.log(e)
							    });
					          
					        }, function (e){console.log(e)
					    });

           }
           else{
           		for ( var i in d.tienda){
           	
	           		if( d.tienda[i] != id )  {
	           			tiendas[tiendas.length] = id;
	           			d.tienda = tiendas;
	           			defaultService.put('/service/perfil/detail/'+$scope.id_usuario+'/', d ,function(data){
					           //console.log(data); 
					           defaultService.get('/service/perfil/detail/'+$scope.id_usuario+'/',function(data){
					           	//console.log(data);
					           	$scope.tiendas_incluidas = data.tienda;     
					          
							        }, function (e){console.log(e)
							    });       
					          
					        }, function (e){console.log(e)
					    });

	           		}
	           		else {
	           			console.log("linea 80 esta tienda ya se encuentra incluida");
	           		}
           		}

           }


           

           
           
          
        }, function (e){console.log(e)
    });
    	

    }



    $scope.excluir_tienda = function(id){
    	console.log("linea 101 excluyendo tiendas");
    	defaultService.get('/service/perfil/detail/'+$scope.id_usuario+'/',function(data){
					           	console.log(data);
					           	var tiendas_incluidas = [];  

					           	for(var i in data.tienda) {
					           		if(data.tienda[i] == id){
					           			console.log("linea 110 excluyendo tienda: "+ id)
					           		}
					           		else{
					           			tiendas_incluidas[tiendas_incluidas.length] = data.tienda[i];
					           		}
					           	} 

					           	//console.log(tiendas_incluidas);

					           	data.tienda = tiendas_incluidas;

					           	defaultService.put('/service/perfil/detail/'+$scope.id_usuario+'/', data ,function(d){
							               
							           defaultService.get('/service/perfil/detail/'+$scope.id_usuario+'/',function(data2){
							           //console.log(data2);
							           $scope.tiendas_incluidas = data2.tienda;     
							          
									        }, function (e){console.log(e)
									    });
							          
							        }, function (e){console.log(e)
							    });



					          
							        }, function (e){console.log(e)
							    });
    }



    $scope.generar_links = function(){
    	//alert("generando links");
    	var links = new Array();
    	var tiendas = $scope.tiendas;
    	var tiendas_incluidas = $scope.tiendas_incluidas;

    	console.log(tiendas);
    	console.log(tiendas_incluidas);

    	for (  var i in tiendas){
    		//console.log(tiendas[i].id)
    		for(var j in tiendas_incluidas){
    			if(tiendas_incluidas[j] == tiendas[i].id ){
    				//console.log(tiendas[i]);
    				links.push(tiendas[i]);
    			}
    		}
    	}
    	$scope.links = links;
    	console.log(links);
    }

    $scope.go_tienda = function(){
    	var correo = $("#correo").val();
    	var vendedora = $("#vendedora").val();
    	var tienda = $("#tienda").val();

    	var url = $scope.servidor+'/nuevo/cliente/?correo='+correo+'&vendedora='+vendedora+'&tienda='+tienda;
    	window.location = url;
    	//alert(url);
    }


    $scope.btn_clientes = function(){
    	

    	defaultService.get('/service/cliente/detail/'+$scope.id_usuario+'/',function(data){
							           //console.log(data2);
							           $scope.clientes = data; 
							           console.log($scope.clientes);
							            $('.facturacion').css('display', 'none');
    									$('.tiendas').css('display', 'none');
								    	$('.ventas').css('display', 'none');
								    	$('.clientes').css('display', 'block');    
							          
									        }, function (e){console.log(e)
									    });


    }

}]);