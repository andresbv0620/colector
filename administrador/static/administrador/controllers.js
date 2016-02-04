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

//////////////Llenar formulario web///////////////////////
app.controller('llenarFormulario', ['$scope', '$routeParams', 'defaultService', 'globales', function($scope, $routeParams, defaultService, globales) {
    $scope.form_id = $routeParams.form_id;
    $scope.newFilledForm = {}
    defaultService.post(globales.static_url + '../service/form/single/', '{"form_id":"' + $routeParams.form_id + '"}', function(data) {
        //console.log(d)
        $scope.formulario = data['response_data'][0];
        /*form_name=data['response_data'][0].name;
        form_description=data['response_data'][0].description;
        form_id=data['response_data'][0].id;
        form_sections=data['response_data'][0].sections;*/
    }, function(error) {
        console.log(error)
    });

    $scope.enviarFormulario = function() {
        formularioObject = $scope.formulario;
        formularioObject.colector_id = globales.user_id;
        formularioObject.form_id = formularioObject.form_id.toString();

        console.log(formularioObject);
        defaultService.post(globales.static_url + '../service/fill/form/', formularioObject, function(data) {
            console.log(data);

        }, function(error) {
            console.log(error)
        });
    }
}]);
//////////////////Reporte por colector id/////////////////////
app.controller('reporteColector', ['$scope', 'defaultService', 'globales', function($scope, defaultService, globales) {
    console.log("iniciando controlador");


    defaultService.get(globales.static_url + '../service/filled/forms/report/colector/4/', function(data) {
        //console.log(d)
        console.log("datos reporte recibidos del servidor: ");

        //console.log(data);
        colectorfilledforms = data['data'];
        $scope.colectorid = colectorfilledforms[0].colector_id;
        filledforms = colectorfilledforms[0].filled_forms;
        $scope.filledforms = filledforms;


        tableheader = [];
        columns = new Array();
        data = new Array();
        tablecontent = new Object();


        for (form in filledforms) {
            sections = filledforms[form].sections;
            for (section in sections) {
                inputs = sections[section].inputs;
                datacolumns = new Object();
                for (input in inputs) {
                    column = new Object();
                    if (tableheader.indexOf(inputs[input].name) < 0) {
                        column['field'] = inputs[input].name;
                        column['sortable'] = true;
                        column['title'] = inputs[input].name;
                        columns.push(column);
                        tableheader.push(inputs[input].name);
                    }
                    respuestas = new Array();
                    responses = inputs[input].responses;
                    for (response in responses) {
                        respuestas.push(responses[response].value);
                        datacolumns[inputs[input].name] = responses[response].value;
                    }
                }
            }
            data.push(datacolumns);
        }

        tablecontent['columns'] = columns;
        tablecontent['data'] = data;

        $scope.tableheaders = tableheader;
        $('#table').bootstrapTable(tablecontent);

    }, function(error) {
        console.log(error)
    });
}]);
/////Reporte por formname///////////////
app.controller('reporteFormulario', ['$scope', 'defaultService', 'globales', function($scope, defaultService, globales) {

    defaultService.get(globales.static_url + '../service/filled/forms/report/formname/formularioBasico/', function(data) {
        //console.log(d)
        //console.log("datos recibidos del servidor: ");

        //console.log(data);
        colectorfilledforms = data['data'];

        $scope.colectorid = colectorfilledforms[0].colector_id;
        filledforms = colectorfilledforms[0].filled_forms;
        $scope.filledforms = filledforms;
        console.log(filledforms);


        tableheader = [];
        columns = new Array();
        data = new Array();
        tablecontent = new Object();


        for (form in filledforms) {
            sections = filledforms[form].sections;
            for (section in sections) {
                inputs = sections[section].inputs;
                datacolumns = new Object();
                for (input in inputs) {
                    column = new Object();
                    if (tableheader.indexOf(inputs[input].name) < 0) {
                        column['field'] = inputs[input].name;
                        column['sortable'] = true;
                        column['title'] = inputs[input].name;
                        columns.push(column);
                        tableheader.push(inputs[input].name);
                    }
                    respuestas = new Array();
                    responses = inputs[input].responses;
                    for (response in responses) {
                        respuestas.push(responses[response].value);
                        datacolumns[inputs[input].name] = responses[response].value;
                    }
                }
            }
            data.push(datacolumns);
        }

        tablecontent['columns'] = columns;
        tablecontent['data'] = data;

        $scope.tableheaders = tableheader;
        $('#table').bootstrapTable(tablecontent);

    }, function(error) {
        console.log(error)
    });
}]);

app.controller('reporteFormularioId', ['$scope', '$routeParams', 'defaultService', 'globales', function($scope, $routeParams, defaultService, globales) {
    $scope.form_name = $routeParams.form_id;
    defaultService.get(globales.static_url + '../service/filled/forms/report/formid/' + $routeParams.form_id + '/', function(data) {
        console.log("datos recibidos del servidor: ");
        //console.log(data);
        colectorfilledforms = data['data'];

        //$scope.colectorid=colectorfilledforms[0].colector_id;

        //console.log(filledforms);

        tableheader = [];
        columns = new Array();
        data = new Array();
        tablecontent = new Object();
        markersArray = new Array();



        

        for (colectorDocument in colectorfilledforms) {
            filledforms = colectorfilledforms[colectorDocument].filled_forms;
            //$scope.filledforms=filledforms;
            console.log(filledforms);
            blackm=0;
            blackf=0;
            hispanicm=0;
            hispanicf=0;
            asianorpacificm=0;
            asianorpacificf=0;
            americanindianm=0;
            americanindianf=0;

            //Cada registro o fila en la tabla
            for (form in filledforms) {
                //inicializo variables para cada fila
                minoritym=0;
                minorityf=0;
                totalm=0;
                totalf=0;

                if (filledforms[form].form_id == $routeParams.form_id) {

                    ///////////Se asignan las coordenadas GPS del registro/////////////////
                    datacolumns = new Object(); //Objeto que va guardando las respuestas de cada registro
                    //markers objeto usado para el mapa
                    markers = {};
                    markers['longitude'] = filledforms[form].latitud;
                    markers['latitude'] = filledforms[form].longitud;
                    
                    responses = filledforms[form].responses;
                    respuestas = new Array();
                    //Cada respuesta o columna en una fila
                    for (response in responses) {
                        inputId = responses[response].inputs_id;
                        if (typeof markers['message'] == "undefined") {
                            markers['message'] = responses[response].value;
                        }
                        inputValue = responses[response].value;
                        inputLabel = responses[response].label;
                        inputType = responses[response].tipo;
                        //Validamos para generar la fila de encabezados
                        if (tableheader.indexOf(inputLabel) < 0) {
                            column = new Object();
                            column['field'] = inputLabel;
                            column['sortable'] = true;
                            column['title'] = inputLabel;
                            columns.push(column);
                            tableheader.push(inputLabel);
                        }

                        //Se valida si es numero
                        if (inputType == 8) {
                            if (typeof datacolumns[inputLabel] !== "undefined") {
                                datacolumns[inputLabel] = datacolumns[inputLabel] + ',' + inputValue;
                            } else {
                                datacolumns[inputLabel] = inputValue;
                                //Calculo reporte para password
                                //Suma de monorities por fila
                                if ((inputLabel=="Black M")||(inputLabel=="Hispanic M")||(inputLabel=="Asian or Pacific Islander M")||(inputLabel=="American Indian or Alaskan Native M")){
                                    minoritym=minoritym+inputValue;
                                }
                                if ((inputLabel=="Black F")||(inputLabel=="Hispanic F")||(inputLabel=="Asian or Pacific Islander F")||(inputLabel=="American Indian or Alaskan Native F")){
                                    minorityf=minorityf+inputValue;
                                }

                                if ((inputLabel=="TOTAL EMPLOYEES M")){
                                    totalm=inputValue;
                                }
                                if ((inputLabel=="TOTAL EMPLOYEES F")){
                                    totalf=inputValue;
                                }


                                //Sumador de totales de columna
                                blackm=0;
                                blackf=0;
                                hispanicm=0;
                                hispanicf=0;
                                asianorpacificm=0;
                                asianorpacificf=0;
                                americanindianm=0;
                                americanindianf=0;



                            }
                        }

                        //Se valida si es foto, para convertirla de base64
                        if (inputType == 6) {
                            if (typeof datacolumns[inputLabel] !== "undefined") {
                                datacolumns[inputLabel] = datacolumns[inputLabel] + '<br><img width="50px" height="50px" src="data:image/png;base64,' + inputValue + '" data-err-src="images/png/avatar.png"/>';
                            } else {
                                datacolumns[inputLabel] = '<img width="50px" height="50px" src="data:image/png;base64,' + inputValue + '" data-err-src="images/png/avatar.png"/>';
                            }
                        } else {
                            if (typeof datacolumns[inputLabel] !== "undefined") {
                                datacolumns[inputLabel] = datacolumns[inputLabel] + ',' + inputValue;
                            } else {
                                datacolumns[inputLabel] = inputValue;
                            }
                        }
                    }

                    /////////////Calculo non monority//////
                    datacolumns["Non Minority M"]=totalm-minoritym;
                    datacolumns["Non Minority F"]=totalf-minorityf;

                    ///////////Se asigna la hora de inicio y fin del registro a las respuestas////////////////
                    horaini = filledforms[form].horaini;
                    var dini = new Date(0);
                    dini.setUTCSeconds(horaini);
                    datacolumns["Start"] = dini;

                    horafin = filledforms[form].horafin;
                    var dfin = new Date(0);
                    dfin.setUTCSeconds(horafin);
                    datacolumns["Final"] = dfin;

                    //Se guardan las respuestas de la fila en el objeto data
                    data.push(datacolumns);
                    markersArray.push(markers);
                }
            }
        }


        ////Non Minority header calculos
        column = new Object();
        column['field'] = "Non Minority M";
        column['sortable'] = true;
        column['title'] = "Non Minority M";
        columns.push(column);

        column = new Object();
        column['field'] = "Non Minority F";
        column['sortable'] = true;
        column['title'] = "Non Minority F";
        columns.push(column);


        ////Inicializo los encabezados por defecto de la tabla reporte, Hora inicio, Hora final ////////////
        column = new Object();
        column['field'] = "Start";
        column['sortable'] = true;
        column['title'] = "Start";
        columns.push(column);

        column = new Object();
        column['field'] = "Final";
        column['sortable'] = true;
        column['title'] = "Final";
        columns.push(column);

        tablecontent['columns'] = columns;
        tablecontent['data'] = data;

        $scope.tableheaders = tableheader;
        $('#table').bootstrapTable(tablecontent);


        ///////////////////////////////MAPS REPORT////////////////////////

        $scope.map = {
            center: {
                latitude: markers['latitude'],
                longitude: markers['longitude']
            },
            zoom: 12
        };

        $scope.marker = {
            coords: {
                latitude: markers['latitude'],
                longitude: markers['longitude']
            }
        }

        $scope.markerList = markersArray;




    }, function(error) {
        console.log(error)
    });
}]);

//////////////////////////////////////////////////////////////

app.controller('startApp', ['$scope', 'defaultService', function($scope, defaultService) {
    console.log("start");
    $scope.version = "1.0";
}]);


app.controller('perfil', ['$scope', 'defaultService', function($scope, defaultService) {
    console.log("cargando perfil");
    $scope.cargar_perfil = function() {
        defaultService.get('/service/perfil/detail/' + $scope.id_usuario + '/', function(d) {
            //console.log(d)
            $scope.titular_cuenta = d.Titular_cuenta_bancaria;
            $scope.pais = d.pais;
            $scope.ciudad = d.ciudad;
            $scope.banco = d.banco;
            $scope.numero_cuenta = d.numero_cuenta;
            //alert($scope.titular_cuenta);
        }, function(e) {
            console.log(e)
        });

    }

    $scope.cargar_perfil();

    $scope.modificar_perfil = function() {
        var data = {
            "Titular_cuenta_bancaria": $scope.titular_cuenta,
            "banco": $scope.banco,
            "numero_cuenta": $scope.numero_cuenta,
            "pais": $scope.pais,
            "ciudad": $scope.ciudad
        };

        console.log(data);
        //alert($scope.titular_cuenta);
        defaultService.put('/service/perfil/detail/' + $scope.id_usuario + '/', data, function(d) {
            console.log(d)
            $scope.titular_cuenta = d.Titular_cuenta_bancaria;
            $scope.pais = d.pais;
            $scope.ciudad = d.ciudad;
            $scope.banco = d.banco;
            $scope.numero_cuenta = d.numero_cuenta;
            alert("Datos modificados con exito");
        }, function(e) {
            console.log(e)
        });



    }



    defaultService.get('/service/tienda/list/', function(d) {
        console.log("linea 19 cargando perfil");
        $scope.tiendas = d;

    }, function(e) {
        console.log(e)
    });


    $scope.btn_tiendas = function() {
        console.log("linea 27 btn_tiendas")
        defaultService.get('/service/perfil/detail/' + $scope.id_usuario + '/', function(data) {

            $scope.tiendas_incluidas = data.tienda;

        }, function(e) {
            console.log(e)
        });
    }



    $scope.incluir_tienda = function(id) {
        //alert(id);
        var tiendas = [];
        defaultService.get('/service/perfil/detail/' + $scope.id_usuario + '/', function(d) {

            tiendas = d.tienda;

            if (tiendas.length == 0) {
                tiendas[0] = id;
                defaultService.put('/service/perfil/detail/' + $scope.id_usuario + '/', d, function(data) {
                    console.log("linea 48 incluyendo tiendas");
                    defaultService.get('/service/perfil/detail/' + $scope.id_usuario + '/', function(data) {

                        $scope.tiendas_incluidas = data.tienda;

                    }, function(e) {
                        console.log(e)
                    });

                }, function(e) {
                    console.log(e)
                });

            } else {
                for (var i in d.tienda) {

                    if (d.tienda[i] != id) {
                        tiendas[tiendas.length] = id;
                        d.tienda = tiendas;
                        defaultService.put('/service/perfil/detail/' + $scope.id_usuario + '/', d, function(data) {
                            //console.log(data); 
                            defaultService.get('/service/perfil/detail/' + $scope.id_usuario + '/', function(data) {
                                //console.log(data);
                                $scope.tiendas_incluidas = data.tienda;

                            }, function(e) {
                                console.log(e)
                            });

                        }, function(e) {
                            console.log(e)
                        });

                    } else {
                        console.log("linea 80 esta tienda ya se encuentra incluida");
                    }
                }

            }




        }, function(e) {
            console.log(e)
        });


    }



    $scope.excluir_tienda = function(id) {
        console.log("linea 101 excluyendo tiendas");
        defaultService.get('/service/perfil/detail/' + $scope.id_usuario + '/', function(data) {
            console.log(data);
            var tiendas_incluidas = [];

            for (var i in data.tienda) {
                if (data.tienda[i] == id) {
                    console.log("linea 110 excluyendo tienda: " + id)
                } else {
                    tiendas_incluidas[tiendas_incluidas.length] = data.tienda[i];
                }
            }

            //console.log(tiendas_incluidas);

            data.tienda = tiendas_incluidas;

            defaultService.put('/service/perfil/detail/' + $scope.id_usuario + '/', data, function(d) {

                defaultService.get('/service/perfil/detail/' + $scope.id_usuario + '/', function(data2) {
                    //console.log(data2);
                    $scope.tiendas_incluidas = data2.tienda;

                }, function(e) {
                    console.log(e)
                });

            }, function(e) {
                console.log(e)
            });




        }, function(e) {
            console.log(e)
        });
    }



    $scope.generar_links = function() {
        //alert("generando links");
        var links = new Array();
        var tiendas = $scope.tiendas;
        var tiendas_incluidas = $scope.tiendas_incluidas;

        console.log(tiendas);
        console.log(tiendas_incluidas);

        for (var i in tiendas) {
            //console.log(tiendas[i].id)
            for (var j in tiendas_incluidas) {
                if (tiendas_incluidas[j] == tiendas[i].id) {
                    //console.log(tiendas[i]);
                    links.push(tiendas[i]);
                }
            }
        }
        $scope.links = links;
        console.log(links);
    }

    $scope.go_tienda = function() {
        var correo = $("#correo").val();
        var vendedora = $("#vendedora").val();
        var tienda = $("#tienda").val();

        var url = $scope.servidor + '/nuevo/cliente/?correo=' + correo + '&vendedora=' + vendedora + '&tienda=' + tienda;
        window.location = url;
        //alert(url);
    }


    $scope.btn_clientes = function() {


        defaultService.get('/service/cliente/detail/' + $scope.id_usuario + '/', function(data) {
            //console.log(data2);
            $scope.clientes = data;
            console.log($scope.clientes);
            $('.facturacion').css('display', 'none');
            $('.tiendas').css('display', 'none');
            $('.ventas').css('display', 'none');
            $('.clientes').css('display', 'block');

        }, function(e) {
            console.log(e)
        });


    }

}]);