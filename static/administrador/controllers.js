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


//////////////Generar Histograma//////////////////////
app.controller('generarHistograma', ['$scope', '$location', '$http', '$uibModal', '$log','$routeParams', 'defaultService', 'globales', function($scope, $location, $http, $uibModal, $log,$routeParams, defaultService, globales) {
    media_url=globales.media_url;
    static_url=globales.static_url;
    
    ///////////////////////////////CARGAR HEADER/////////////////////////////////////////////

    // define the function that does the ajax call
    getheaders = function() {
        return $http.get(globales.static_url + '../service/filled/forms/report/paginate/histograma/' + $routeParams.form_id + '/?getcolumns=true')
            .success(function(data) 
            {
                if (data['response_code']=='404') {
                    $scope.notificacion='NO HAY REGISTROS PARA ESTE FORMULARIO'
                    return;
                }
                $scope.mydata = data;
            });
    }

    // Llamado inicial para carga sin filtros
    getheaders().then(function(data) {
        $scope.colectors=$scope.mydata['colectors']
        console.log($scope.mydata);
        // stuff is now in our scope, I can alert it
        dataurl="/service/filled/forms/report/paginate/histograma/" + $routeParams.form_id + "/";
        setuptable($scope.mydata, dataurl);
    });

    setuptable = function(data, dataurl) {

        $('#table').bootstrapTable('destroy');
        var tablecontent = new Object();
        var columns = new Array();        

        columns=$scope.mydata['columns']

        ////Inicializo los encabezados por defecto de la tabla reporte, Hora inicio, Hora final ////////////


        column = new Object();
        column['field'] = "MongoId";
        column['title'] = "MongoId";
        columns.unshift(column);

        /*column = new Object();
        column['field'] = "No Aplica";
        column['title'] = "No Aplica";
        columns.unshift(column);*/

        column = new Object();
        column['field'] = "Calificacion 5";
        column['title'] = "Calificacion 5";
        column['sortable'] = 'true'
        columns.unshift(column);

        column = new Object();
        column['field'] = "Calificacion 4";
        column['title'] = "Calificacion 4";
        column['sortable'] = 'true'
        columns.unshift(column);

        column = new Object();
        column['field'] = "Calificacion 3";
        column['title'] = "Calificacion 3";
        column['sortable'] = 'true'
        columns.unshift(column);

        column = new Object();
        column['field'] = "Calificacion 2";
        column['title'] = "Calificacion 2";
        column['sortable'] = 'true'
        columns.unshift(column);

        column = new Object();
        column['field'] = "Calificacion 1";
        column['title'] = "Calificacion 1";
        column['sortable'] = 'true'
        columns.unshift(column);

        column = new Object();
        column['field'] = "Pregunta";
        column['title'] = "Pregunta";
        column['filterControl'] = "input"
        column['sortable'] = 'true'
        columns.unshift(column);

        column = new Object();
        column['field'] = "Aspecto";
        column['title'] = "Aspecto";
        column['filterControl'] = "input"
        column['sortable'] = 'true'
        columns.unshift(column);

        column = new Object();
        column['field'] = "state";
        column['checkbox'] = true;
        column['title'] = "state";
        columns.unshift(column);

        /*column = new Object();
        column['field']="action";
        column['title']="Accion";
        column['formatter']="actionFormatter";
        column['events']="actionEvents";
        columns.push(column);*/
        
        tablecontent['url'] = dataurl;

        

        tablecontent['detailFormatter']=function(index, row, element) {
            var html = [];
                $.each(row, function (key, value) {
                    if ((key=='Hora Fin') || (key=='Hora Inicio')) {
                        var d = new Date(0); // The 0 there is the key, which sets the date to the epoch
                        d.setUTCSeconds(value);
                        html.unshift('<p><b>' + key + ':</b> ' + d + '</p>');
                    }else{
                        if ((key=='longitud') || (key=='latitud')) {
                            html.unshift('<p><b>' + key + ':</b> ' + value + '</p>');
                        }else{                    
                            html.push('<p><b>' + key + ':</b> ' + value + '</p>');
                        }                    
                    }

                });
            return html.join('');
        };


        tablecontent['columns'] = columns; 
                
        $('#table').bootstrapTable(tablecontent);   
        
        ///Ocultando columnas
        $('#table').bootstrapTable('hideColumn', 'colector_id');
        $('#table').bootstrapTable('hideColumn', 'latitud');
        $('#table').bootstrapTable('hideColumn', 'longitud');
        $('#table').bootstrapTable('hideColumn', 'MongoId');
        $('#table').bootstrapTable('hideColumn', 'record_id');
        $('#table').bootstrapTable('hideColumn', 'form_name');
        $('#table').bootstrapTable('hideColumn', 'form_description');
        $('#table').bootstrapTable('hideColumn', 'form_id');
        $('#table').bootstrapTable('hideColumn', 'sincronizado_utc');
        $('#table').bootstrapTable('hideColumn', 'Hora Fin');
        $('#table').bootstrapTable('hideColumn', 'Hora Inicio');

    }

    
    /////Filters/////
    $scope.filterResults = function() {

        getheaders().then(function(data) {
            
            colector_id = $scope.selectedColector.colector_id;
            dataurl = "/service/filled/forms/report/paginate/formid/" + $routeParams.form_id + "/?colector_id="+colector_id;
            setuptable($scope.mydata, dataurl);

            $('#table').bootstrapTable('refresh', {});

        });
        $scope.filtered = true;        
    }

    $scope.resetFilter = function() {


        getheaders().then(function(data) {
            colector_id = $scope.selectedColector.colector_id;
            dataurl="/service/filled/forms/report/paginate/formid/" + $routeParams.form_id + "/";
            setuptable($scope.mydata, dataurl);
            $('#table').bootstrapTable('refresh', {});
        });

        $scope.selectedColector = {};
        $scope.filtered = false;
        
    }


    ////ACCIONES SOBRE SELECCIONADOS
    $('#deletebutton').click(function () {
        if (!confirm('Los registros se borraran permanentemente')){
            return;
        }
        var ids = $.map($('#table').bootstrapTable('getSelections'), function (row) {
            colector_id = globales.user_id;
            record_id = row.MongoId;
            defaultService.post(globales.static_url + '../service/form/delete/' + record_id + '/', '{"colector_id":"' + colector_id + '","record_id":"'+record_id+'"}', function(data) {
                $('#table').bootstrapTable('remove', {
                    field: 'MongoId',
                    values: ids
                });
            }, function(error) {
                console.log(error)
            });
            return row.MongoId;
        });
        $('#table').bootstrapTable('remove', {
            field: 'MongoId',
            values: ids
        });
        alert('Registros Eliminados Permanentemente');
    });
    ////ACCIONES SOBRE EL REGISTRO
    window.actionEvents = {
        'click .mapa': function (e, value, row, index) {
            console.log(value, row, index);
            window.location.href="#/reporte/id/"+ $routeParams.form_id +"/"+row['longitud']+"/"+row['latitud'];

            
        },
        'click .edit': function (e, value, row, index) {
            alert('No cuenta con los privilegios para modificar este registro!');
            console.log(value, row, index);
        },
        'click .remove': function (e, value, row, index) {
            if (confirm('El registro se borrara permanentemente')){
                console.log('Registro borrado '+row['MongoId']);
                /////Llamado al servicio de borrado////
                record_id = row['MongoId'];
                colector_id = globales.user_id;
                defaultService.post(globales.static_url + '../service/form/delete/' + record_id + '/', '{"colector_id":"' + colector_id + '","record_id":"'+record_id+'"}', function(data) {
                    $scope.notificacion = "El registro ha sido borrado";

                    var ids = $.map($('#table').bootstrapTable('getSelections'), function (row) {
                        alert('Registro Eliminado Permanentemente');
                        return row.MongoId;
                    });
                    $('#table').bootstrapTable('remove', {
                        field: 'MongoId',
                        values: ids
                    }); 
                }, function(error) {
                    console.log(error)
                });
            }
        }
    };

    //////FUNCION LLAMADA PARA CARGAR LOS DATOS DEL MAPA
    $scope.loadMap = function() {
        pagData = $('#table').bootstrapTable('getData');
        markersArray = new Array();
        for (var i = pagData.length - 1; i >= 0; i--) {
            markers = {};
            markers['longitude'] = pagData[i]["longitud"];
            markers['latitude'] = pagData[i]["latitud"];
            markers['message'] = pagData[i]["latitud"];
            markersArray.push(markers);
            //console.log(markersArray);
        }
        //////////////////////////MAPS REPORT////////////////////////
        $scope.polygons = [
            {
                id: 1,
                path: markersArray,
                stroke: {
                    color: '#6060FB',
                    weight: 3
                },
                editable: false,
                draggable: false,
                geodesic: false,
                visible: true,
                fill: {
                    color: '#000000',
                    opacity: 0.1
                }
            }
        ];
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
    }

    //////FUNCION LLAMADA PARA DESCARGAR EXCEL
    $scope.loadExcel = function() {
        colector_id = globales.user_id;
        defaultService.post(globales.static_url + '../service/filled/forms/report/excel/formid/' + $routeParams.form_id + '/', '{"colector_id":"' + colector_id + '}', function(data) {
            alert(data['response_description']);
            console.log(data);
        }, function(error) {
            console.log(error)
        });
    }



    ///AL HACER EL LLAMADO CON JAVASCRIPT NO ESTA FUNCIONANDO, CUANDO SE LLAMA CON ANGULAR FUNCIONA
    $('#table').on('load-success.bs.table', function (e, number, size) {
        $('#loadmapbutton').click();
    });

}]);
///////////////////////////////////////////////////////


 //////////////Reporte por formid server side pagination////////////////////////
app.controller('serverSidePagController', ['$scope', '$location', '$http', '$uibModal', '$log','$routeParams', 'defaultService', 'globales', function($scope, $location, $http, $uibModal, $log,$routeParams, defaultService, globales) {
    media_url=globales.media_url;
    static_url=globales.static_url;
    
    ///////////////////////////////CARGAR HEADER/////////////////////////////////////////////

    // define the function that does the ajax call
    getheaders = function() {
        return $http.get(globales.static_url + '../service/filled/forms/report/paginate/formid/' + $routeParams.form_id + '/?getcolumns=true')
            .success(function(data) 
            {
                if (data['response_code']=='404') {
                    $scope.notificacion='NO HAY REGISTROS PARA ESTE FORMULARIO'
                    return;
                }
                $scope.mydata = data;
            });
    }

    // Llamado inicial para carga sin filtros
    getheaders().then(function(data) {
        $scope.colectors=$scope.mydata['colectors']
        console.log($scope.mydata);
        // stuff is now in our scope, I can alert it
        dataurl="/service/filled/forms/report/paginate/formid/" + $routeParams.form_id + "/";
        setuptable($scope.mydata, dataurl);
    });

    setuptable = function(data, dataurl) {
        $('#table').bootstrapTable('destroy');
        var tablecontent = new Object();
        var columns = new Array();        

        columns=$scope.mydata['columns']

        ////Inicializo los encabezados por defecto de la tabla reporte, Hora inicio, Hora final ////////////


        column = new Object();
        column['field'] = "MongoId";
        column['title'] = "MongoId";
        columns.unshift(column);

        column = new Object();
        column['field'] = "state";
        column['checkbox'] = true;
        column['title'] = "state";
        columns.unshift(column);

        column = new Object();
        column['field']="action";
        column['title']="Accion";
        column['formatter']="actionFormatter";
        column['events']="actionEvents";
        columns.push(column);
        
        tablecontent['url'] = dataurl;

        

        tablecontent['detailFormatter']=function(index, row, element) {
            var html = [];
                $.each(row, function (key, value) {
                    if ((key=='Hora Fin') || (key=='Hora Inicio')) {
                        var d = new Date(0); // The 0 there is the key, which sets the date to the epoch
                        d.setUTCSeconds(value);
                        html.unshift('<p><b>' + key + ':</b> ' + d + '</p>');
                    }else{
                        if ((key=='longitud') || (key=='latitud')) {
                            html.unshift('<p><b>' + key + ':</b> ' + value + '</p>');
                        }else{                    
                            html.push('<p><b>' + key + ':</b> ' + value + '</p>');
                        }                    
                    }

                });
            return html.join('');
        };


        tablecontent['columns'] = columns; 
                
        $('#table').bootstrapTable(tablecontent);   
        
        ///Ocultando columnas
        $('#table').bootstrapTable('hideColumn', 'colector_id');
        $('#table').bootstrapTable('hideColumn', 'latitud');
        $('#table').bootstrapTable('hideColumn', 'longitud');
        $('#table').bootstrapTable('hideColumn', 'MongoId');
        $('#table').bootstrapTable('hideColumn', 'record_id');
        $('#table').bootstrapTable('hideColumn', 'form_name');
        $('#table').bootstrapTable('hideColumn', 'form_description');
        $('#table').bootstrapTable('hideColumn', 'form_id');
        $('#table').bootstrapTable('hideColumn', 'sincronizado_utc');
        $('#table').bootstrapTable('hideColumn', 'Hora Fin');
        $('#table').bootstrapTable('hideColumn', 'Hora Inicio');

    }

    
    /////Filters/////
    $scope.filterResults = function() {

        getheaders().then(function(data) {
            
            colector_id = $scope.selectedColector.colector_id;
            dataurl = "/service/filled/forms/report/paginate/formid/" + $routeParams.form_id + "/?colector_id="+colector_id;
            setuptable($scope.mydata, dataurl);

            $('#table').bootstrapTable('refresh', {});

        });
        $scope.filtered = true;        
    }

    $scope.resetFilter = function() {


        getheaders().then(function(data) {
            colector_id = $scope.selectedColector.colector_id;
            dataurl="/service/filled/forms/report/paginate/formid/" + $routeParams.form_id + "/";
            setuptable($scope.mydata, dataurl);
            $('#table').bootstrapTable('refresh', {});
        });

        $scope.selectedColector = {};
        $scope.filtered = false;
        
    }


    ////ACCIONES SOBRE SELECCIONADOS
    $('#deletebutton').click(function () {
        if (!confirm('Los registros se borraran permanentemente')){
            return;
        }
        var ids = $.map($('#table').bootstrapTable('getSelections'), function (row) {
            colector_id = globales.user_id;
            record_id = row.MongoId;
            defaultService.post(globales.static_url + '../service/form/delete/' + record_id + '/', '{"colector_id":"' + colector_id + '","record_id":"'+record_id+'"}', function(data) {
                $('#table').bootstrapTable('remove', {
                    field: 'MongoId',
                    values: ids
                });
            }, function(error) {
                console.log(error)
            });
            return row.MongoId;
        });
        $('#table').bootstrapTable('remove', {
            field: 'MongoId',
            values: ids
        });
        alert('Registros Eliminados Permanentemente');
    });
    ////ACCIONES SOBRE EL REGISTRO
    window.actionEvents = {
        'click .mapa': function (e, value, row, index) {
            console.log(value, row, index);
            window.location.href="#/reporte/id/"+ $routeParams.form_id +"/"+row['longitud']+"/"+row['latitud'];

            
        },
        'click .edit': function (e, value, row, index) {
            alert('No cuenta con los privilegios para modificar este registro!');
            console.log(value, row, index);
        },
        'click .remove': function (e, value, row, index) {
            if (confirm('El registro se borrara permanentemente')){
                console.log('Registro borrado '+row['MongoId']);
                /////Llamado al servicio de borrado////
                record_id = row['MongoId'];
                colector_id = globales.user_id;
                defaultService.post(globales.static_url + '../service/form/delete/' + record_id + '/', '{"colector_id":"' + colector_id + '","record_id":"'+record_id+'"}', function(data) {
                    $scope.notificacion = "El registro ha sido borrado";

                    var ids = $.map($('#table').bootstrapTable('getSelections'), function (row) {
                        alert('Registro Eliminado Permanentemente');
                        return row.MongoId;
                    });
                    $('#table').bootstrapTable('remove', {
                        field: 'MongoId',
                        values: ids
                    }); 
                }, function(error) {
                    console.log(error)
                });
            }
        }
    };

    //////FUNCION LLAMADA PARA CARGAR LOS DATOS DEL MAPA
    $scope.loadMap = function() {
        pagData = $('#table').bootstrapTable('getData');
        markersArray = new Array();
        for (var i = pagData.length - 1; i >= 0; i--) {
            markers = {};
            markers['longitude'] = pagData[i]["longitud"];
            markers['latitude'] = pagData[i]["latitud"];
            markers['message'] = pagData[i]["latitud"];
            markersArray.push(markers);
            //console.log(markersArray);
        }
        //////////////////////////MAPS REPORT////////////////////////
        $scope.polygons = [
            {
                id: 1,
                path: markersArray,
                stroke: {
                    color: '#6060FB',
                    weight: 3
                },
                editable: false,
                draggable: false,
                geodesic: false,
                visible: true,
                fill: {
                    color: '#000000',
                    opacity: 0.1
                }
            }
        ];
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
    }

    //////FUNCION LLAMADA PARA DESCARGAR EXCEL
    $scope.loadExcel = function() {
        colector_id = globales.user_id;
        defaultService.post(globales.static_url + '../service/filled/forms/report/excel/formid/' + $routeParams.form_id + '/', '{"colector_id":"' + colector_id + '}', function(data) {
            alert(data['response_description']);
            console.log(data);
        }, function(error) {
            console.log(error)
        });
    }


    //////FUNCION PARA MOSTRAR URL HISTOGRAMAS
    $scope.loadFreq = function() {
        $location.url('/histograma/id/'+ $routeParams.form_id);
    };



    ///AL HACER EL LLAMADO CON JAVASCRIPT NO ESTA FUNCIONANDO, CUANDO SE LLAMA CON ANGULAR FUNCIONA
    $('#table').on('load-success.bs.table', function (e, number, size) {
        $('#loadmapbutton').click();
    });

}]);
///////////////////////////////////////////////////////




//////////////Llenar formulario web///////////////////////
app.controller('llenarFormulario', ['$scope', '$routeParams', 'defaultService', 'globales', function($scope, $routeParams, defaultService, globales) {
    

    
}]);

app.controller('TabController',['$scope', '$routeParams', 'defaultService', 'globales', '$window', function($scope, $routeParams, defaultService, globales, $window) {
    this.loading=true;
    $scope.form_id = $routeParams.form_id;
    
    var tabsdata = this;

    defaultService.post(globales.static_url + '../service/form/single/', '{"form_id":"' + $routeParams.form_id + '"}', function(data) {
        console.log(data['response_data'][0]);
        $scope.formulario = data['response_data'][0];

        tabsdata.tabs=$scope.formulario.sections;
        tabsdata.steps=tabsdata.tabs.length;
        tabsdata.firsttab=tabsdata.tabs[0].section_id;
        tabsdata.lasttab=tabsdata.tabs[tabsdata.tabs.length-1].section_id;
        tabsdata.tab = tabsdata.firsttab;
        tabsdata.btntext = "Comenzar";
        tabsdata.loading = false;


    }, function(error) {
        console.log(error)
    });

    this.setLayout = function(currentTab){
        if (currentTab==this.firsttab) {
            return 'col-md-5';
        }else{
            return 'col-md-8 col-md-offset-2';
        }
    };


    this.setTab = function(newValue){
      this.tab = newValue;
    };


    this.isSet = function(tabName){
      return this.tab === tabName;
    };

    this.backTab = function(currentTab){
        if (currentTab!=this.firsttab) {
            this.tab=currentTab-1;             
        } 
         
    };

    this.nextTab = function(currentTab){
        this.btntext = "Continuar";
        if (currentTab==this.lasttab) {
            this.tab=this.firsttab;
            this.sendForm($scope.formulario)
        }else{ 
            this.tab=currentTab+1;   
        }
    };

    this.sendForm = function(filledform){
        if(this.form.$valid) { 
            // Save to db or whatever.
            
        this.datatoinsert = {
        "colector_id":globales.user_id,
        "form_id":$scope.form_id, 
        "longitud":"-76.5205", 
        "latitud":"3.42158", 
        "horaini":"1461705682", 
        "horafin":"1461705682",
        "responses": []
        }
        this.formresponses = new Array();
        sections = filledform.sections
        for (section in sections) {
            inputs = sections[section].inputs;
            for (input in inputs) {
                if (typeof inputs[input].record["value"] === 'undefined') {
                    this.errortab=sections[section].section_id;
                    inputs[input].record["value"]="vacio";
                }
                this.formresponses.push(inputs[input].record);
            }
        }
        this.datatoinsert.responses = this.formresponses;
        console.log(this.datatoinsert);

        defaultService.post(globales.static_url + '../service/fill/responses/', this.datatoinsert, function(data) {
            console.log(data);

        }, function(error) {
            console.log(error)
        });
            swal("Registro exitoso!", "Haz click en el boton para terminar", "success");
            this.form.$setPristine();
            //$window.location.href = "http://finantic.co/lp/solicitud-realizada/";
            $window.location.href = "#/histograma/id/"+$scope.form_id;
       }else{        

        swal({   
            title: "Oops...",   
            text: "Algunas preguntas no han sido contestadas",   
            type: "warning",   
            showCancelButton: false,   
            confirmButtonColor: "#DD6B55",   
            confirmButtonText: "Aceptar",   
            closeOnConfirm: true }, 
            function(){   
                this.tab=this.errortab;
            });
        
        
       }

    };
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

//////////////Reporte por formid////////////////////////7
app.controller('reporteFormularioId', ['$scope', '$uibModal', '$log','$routeParams', 'defaultService', 'globales', function($scope, $uibModal, $log,$routeParams, defaultService, globales) {
    
    $scope.loading = true;
    $("#table").bootstrapTable("showLoading");
    media_url=globales.media_url;
    static_url=globales.static_url;

    ////////////////////////////////LLAMADO AL SERVICIO QUE DEVUELVE FORMULARIOS DILIGENCIADOS/////////////////////////////////////////////
    defaultService.get(globales.static_url + '../service/filled/forms/report/formid/' + $routeParams.form_id + '/', function(data) {
        console.log("datos recibidos del servidor: ");
        //console.log(data);
        colectorfilledforms = data['data'];
        console.log(colectorfilledforms);

        //$scope.colectorid=colectorfilledforms[0].colector_id;
        //console.log(filledforms);
        tableheader = [];
        columns = new Array();
        data = new Array();
        tablecontent = new Object();
        markersArray = new Array();

        ////Inicializo los encabezados por defecto de la tabla reporte, Hora inicio, Hora final ////////////
        column = new Object();
        column['field'] = "state";
        column['checkbox'] = true;
        column['title'] = "state";
        columns.push(column);

        column = new Object();
        column['field'] = "ID Colector";
        column['sortable'] = true;
        column['visible'] = false;
        column['title'] = "ID Colector";
        columns.push(column);


        column = new Object();
        column['field'] = "Inicio";
        column['sortable'] = true;
        column['title'] = "Inicio";
        columns.push(column);

        column = new Object();
        column['field'] = "Fin";
        column['sortable'] = true;
        column['title'] = "Fin";
        columns.push(column);

        column = new Object();
        column['field'] = "id";
        column['sortable'] = true;
        column['visible'] = false;
        column['title'] = "id";
        columns.push(column);

        column = new Object();
        column['field'] = "sorter";
        column['sortable'] = true;
        column['visible'] = false;
        column['title'] = "sorter";
        columns.push(column);

        ////For que recorre cada documento de colector (cada colector tiene un documento donde se guardan los registros filled_forms)
        markers = {};
        for (colectorDocument in colectorfilledforms) {
            filledforms = colectorfilledforms[colectorDocument].filled_forms;
            colectoridrecord = colectorfilledforms[colectorDocument].colector_id;
            //console.log(colectoridrecord);
            //$scope.filledforms=filledforms;
            //console.log(filledforms);

            //Cada registro o fila en la tabla
            for (form in filledforms) {
                //If que filtra solo el reporte del form_id seleccionado
                if (filledforms[form].form_id == $routeParams.form_id) {
                    $scope.formname=filledforms[form].form_name;

                    ///////////Se asignan las coordenadas GPS del registro/////////////////
                    datacolumns = new Object(); //Objeto que va guardando las respuestas de cada registro
                    //markers objeto usado para el mapa
                    markers = {};
                    markers['longitude'] = filledforms[form].longitud;
                    markers['latitude'] = filledforms[form].latitud;
                    
                    datacolumns["View Map"]="<a href='#/reporte/id/"+ $routeParams.form_id +"/"+markers['longitude']+"/"+markers['latitude']+"'>View Map</a>";

                    responses = filledforms[form].responses;
                    respuestas = new Array();

                    //Cada respuesta o columna en una fila
                    for (response in responses) {
                        inputId = responses[response].input_id;
                        //Se define la primer respuesta como el titulo del pin enel mapa
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

                        //Reporte numero, Se valida si es numero
                        if (inputType == 8) {
                            inputValue=parseFloat(inputValue);
                            if (typeof datacolumns[inputLabel] !== "undefined") {
                                datacolumns[inputLabel] = datacolumns[inputLabel] + ',' + inputValue;
                            } else {
                                datacolumns[inputLabel] = inputValue;
                            }
                        }

                        //Reporte para foto, Se valida si es foto, para convertirla de base64
                        if ((inputType == 6)||(inputType==14)) {
                            src=media_url +inputId+'/'+inputValue+'.jpg';

                            if (typeof datacolumns[inputLabel] !== "undefined") {
                                datacolumns[inputLabel] = datacolumns[inputLabel] + '<a class="thumb"><img onClick="openMedia()" id="'+src+'" width="50px" height="50px" src="'+static_url+'administrador/admin/dist/img/avatar.png" data-err-src="'+static_url+'administrador/admin/dist/img/avatar.png"/></a>';
                            } else {
                                datacolumns[inputLabel] = '<a class="thumb"><img onClick="openMedia()" id="'+src+'" width="50px" height="50px" src="'+static_url+'administrador/admin/dist/img/avatar.png" data-err-src="'+static_url+'administrador/admin/dist/img/avatar.png"/></a>';
                            }
                        } 

                        //Reporte para el resto de tipos de entrada
                        if ((inputType==1)||(inputType==2)||(inputType==3)||(inputType==4)||(inputType==5)||(inputType==7)||(inputType==9)||(inputType==10)||(inputType==11)||(inputType==12)) {
                            if (typeof datacolumns[inputLabel] !== "undefined") {
                                datacolumns[inputLabel] = datacolumns[inputLabel] + ',' + inputValue;
                            } else {
                                datacolumns[inputLabel] = inputValue;
                            }
                        }
                    }//Fin for para mostrar cada respuesta (columna) de una fila

                    /////////////COLUMNAS ADICIONALES en la fila Calculo non monority//////
                    ///////////Se asigna la hora de inicio y fin del registro a las respuestas////////////////
                    datacolumns["ID Colector"] = colectoridrecord;

                    horaini = filledforms[form].horaini;
                    var dini = new Date(0);
                    dini.setUTCSeconds(horaini);
                    datacolumns["Inicio"] = dini;

                    horafin = filledforms[form].horafin;
                    var dfin = new Date(0);
                    dfin.setUTCSeconds(horafin);
                    datacolumns["Fin"] = dfin;

                    datacolumns["id"] = filledforms[form].record_id;
                    datacolumns["sorter"] = horafin;

                    datacolumns["Delete"] = '<a id="delete_row" href="#/reporte/id/'+$routeParams.form_id+'/record/delete/'+filledforms[form].record_id+'">Delete</a>';

                    //Se guardan las respuestas de la fila en el objeto data
                    data.push(datacolumns);
                    markersArray.push(markers);
                }//Fin If que filtra solo el reporte del form_id seleccionado
            }///////////Fin for filas o registros/////////////////////
            //FILAS ADICIONALES, Sumatorias y totales de columnas
            //...............//
        }

        /////ENCABEZADOS ADICIONALES////
        column = new Object();
        column['field'] = "Delete";
        column['sortable'] = true;
        column['title'] = "Delete";
        columns.push(column);
        
        //////////////MAPA EN CADA REGISTRO///////////////////
        column = new Object();
        column['field'] = "View Map";
        column['sortable'] = true;
        column['title'] = "View Map";
        columns.push(column);
        tablecontent['columns'] = columns;
        tablecontent['data'] = data;
        tablecontent['formatLoadingMessage'] = function () {
            return '<img src="http://www.arabianbusiness.com/skins/ab.main/gfx/loading_spinner.gif" />';
        };

        $scope.tableheaders = tableheader;
        $('#table').bootstrapTable(tablecontent);
        
        $("#table").bootstrapTable('hideLoading');

        ///Datos a exportar segun select, basico, seleccionados o todos.

         var $table = $('#table');
            $(function () {
                $('#toolbar').find('select').change(function () {
                    $table.bootstrapTable('refreshOptions', {
                        exportDataType: $(this).val()
                    });
                });

            });


        
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

        ////Cambio el estado del loading para que no se muestre una vez cargado todo success
        $scope.loading = false;

    }, function(error) {
        console.log(error)
    });

}]);
///////////////////////////////////////////////////////


///////////////////Reporte Mapa/////////////////////////////
app.controller('reporteMapa', ['$scope', '$routeParams', 'defaultService', 'globales', function($scope, $routeParams, defaultService, globales) {
    $scope.form_name = $routeParams.form_id;
    longitud = $routeParams.longitud;
    latitud = $routeParams.latitud;
    $scope.loading = true;

    ///////////////////////////////MAPS REPORT////////////////////////
    markersArray = new Array();
    markers = {};
    markers['longitude'] = longitud;
    markers['latitude'] = latitud;
    markersArray.push(markers);

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

    $scope.loading = false;


}]);


//////////////////////////DELETE RECORD////////////////////////////777
app.controller('deleteRecord', ['$scope', '$routeParams', 'defaultService', 'globales','$location', function($scope, $routeParams, defaultService, globales, $location) {
    colector_id = globales.user_id;
    record_id = $routeParams.record_id;
    form_id = $routeParams.form_id;
    $scope.notificacion = "Esta a punto de eliminar un registro";
    $scope.loading = true;
    if(confirm("¿Esta seguro de borrar este registro?")){
        /////Llamado al servicio de borrado////
        defaultService.post(globales.static_url + '../service/form/delete/' + record_id + '/', '{"colector_id":"' + colector_id + '","record_id":"'+record_id+'"}', function(data) {
           $scope.notificacion = "El registro ha sido borrado";
           //$location.path("reporte/id/"+ form_id+"/page/0/limit/10" ).replace();
           $location.path("reporte/id/"+ form_id+"").replace();
        }, function(error) {
            console.log(error)
        });
    }else{
        $location.path("reporte/id/"+ form_id+"" ).replace();
    }
}]);


app.controller('alerta', ['$scope', '$routeParams', 'defaultService', 'globales','$location', function($scope, $routeParams, defaultService, globales, $location) {
    colector_id = globales.user_id;
    record_id = $routeParams.record_id;
    form_id = $routeParams.form_id;
    $scope.notificacion = "Esta a punto de eliminar un registro";
    $scope.loading = true;
    
    this.llamardatos=function(){
        alert("Funciona");
    };

}]);

//////////////Paginacion Controller//////////////////////7
app.controller('FormIdReportPaginate', ['$scope', '$uibModal', '$log','$routeParams', 'defaultService', 'globales', function($scope, $uibModal, $log,$routeParams, defaultService, globales) {
    $scope.loading = true;
    $("#table").bootstrapTable("showLoading");

    ////////////////////////////////LLAMADO AL SERVICIO QUE DEVUELVE FORMULARIOS DILIGENCIADOS/////////////////////////////////////////////
    defaultService.get(globales.static_url + '../service/filled/forms/report/formidpag/' + $routeParams.form_id + '/?page='+ $routeParams.page + '&limit='+ $routeParams.limit + '', function(data) {
        console.log("datos recibidos del servidor: ");
        console.log($routeParams.limit);
        colectorfilledforms = data['data'];
        formrows=data['rows'];
        formcols=data['cols'];
        markers=data['markers'];
        console.log(markers)
        // init paginacion
        $scope.page = $routeParams.page;
        $scope.limit = $routeParams.limit;
        $scope.nextPageNumber = data['nextPageNumber']-1;
        $scope.previousPageNumber = data['previousPageNumber']-1;
        $scope.hasPrevious = data['hasPrevious'];
        $scope.hasNext = data['hasNext'];
        $scope.numPages = data['numPages'];
        $scope.total = data['total'];
        $scope.formId = $routeParams.form_id;

        $scope.pageSizes = [5,10,25,50];
        $scope.reverse = false;
        $scope.filteredItems = formrows;
        $scope.groupedItems = [];
        $scope.itemsPerPage = 0;
        $scope.pagedItems = formrows;
        $scope.currentPage = 0;
        $scope.items = formrows;

        // show items per page
        $scope.perPage = function () {
            $scope.groupToPages();
        };

        // calculate page in place
        $scope.groupToPages = function () {
        $scope.pagedItems = [];

        for (var i = 0; i < $scope.filteredItems.length; i++) {
            if (i % $scope.itemsPerPage === 0) {
                $scope.pagedItems[Math.floor(i / $scope.itemsPerPage)] = [ $scope.filteredItems[i] ];
            } else {
                $scope.pagedItems[Math.floor(i / $scope.itemsPerPage)].push($scope.filteredItems[i]);
            }
            }
        };

        $scope.range = function (start, end) {
        var ret = [];
        if (!end) {
          end = start;
          start = 0;
        }
        for (var i = start; i < end; i++) {
          ret.push(i);
        }
        return ret;
        };

        $scope.prevPage = function () {
        if ($scope.currentPage > 0) {
          $scope.currentPage--;
        }
        };

        $scope.nextPage = function () {
        if ($scope.currentPage < $scope.pagedItems.length - 1) {
          $scope.currentPage++;
        }
        };

        $scope.setPage = function () {
            $scope.currentPage = this.n;
        };
      ////////////////////////////////////////

        ////Inicializo los encabezados por defecto de la tabla reporte, Hora inicio, Hora final ////////////
        column = new Object();
        column['field'] = "state";
        column['checkbox'] = true;
        column['title'] = "state";
        formcols.unshift(column);


        column = new Object();
        column['field'] = "Inicio";
        column['sortable'] = true;
        column['title'] = "Inicio";
        formcols.push(column);

        column = new Object();
        column['field'] = "Fin";
        column['sortable'] = true;
        column['title'] = "Fin";
        formcols.push(column);

        column = new Object();
        column['field'] = "id";
        column['sortable'] = true;
        column['visible'] = false;
        column['title'] = "id";
        formcols.push(column);

        column = new Object();
        column['field'] = "sorter";
        column['sortable'] = true;
        column['visible'] = false;
        column['title'] = "sorter";
        formcols.push(column);

        /////ENCABEZADOS ADICIONALES////
        column = new Object();
        column['field'] = "Delete";
        column['sortable'] = true;
        column['title'] = "Delete";
        formcols.push(column);
        
        //////////////MAPA EN CADA REGISTRO///////////////////
        column = new Object();
        column['field'] = "View Map";
        column['sortable'] = true;
        column['title'] = "View Map";
        formcols.push(column);

        tablecontent={}

        tablecontent['columns'] = formcols;
        tablecontent['data'] = formrows;
        tablecontent['formatLoadingMessage'] = function () {
            return '<img src="http://www.arabianbusiness.com/skins/ab.main/gfx/loading_spinner.gif" />';
        };

        //$scope.tableheaders = tableheader;

        $('#table').bootstrapTable(tablecontent);

        $('#table').on('click-row.bs.table', function (e, row, $element) {
        console.log('Event: click-row.bs.table');
        });
        
        $("#table").bootstrapTable('hideLoading');

        ///Datos a exportar segun select, basico, seleccionados o todos.

         var $table = $('#table');
            $(function () {
                $('#toolbar').find('select').change(function () {
                    $table.bootstrapTable('refreshOptions', {
                        exportDataType: $(this).val()
                    });
                });

            });




            ///////////////////////////////MAPS REPORT////////////////////////
        $scope.map = {
            center: {
                latitude: markers[0]['latitude'],
                longitude: markers[0]['longitude']
            },
            zoom: 12
        };

        $scope.marker = {
            coords: {
                latitude: markers[0]['latitude'],
                longitude: markers[0]['longitude']
            }
        }

        $scope.markerList = markers;
        ////Cambio el estado del loading para que no se muestre una vez cargado todo success
        $scope.loading = false;

    }, function(error) {
        console.log(error)
    });

}]);
///////////////////////////////////////////////////////


app.controller('ModalDemoCtrl', function ($scope, $uibModal, $log) {

  $scope.items = ['item1', 'item2', 'item3'];

  $scope.animationsEnabled = true;

  $scope.open = function (size) {

    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: 'myModalContent.html',
      controller: 'ModalInstanceCtrl',
      size: size,
      resolve: {
        items: function () {
          return $scope.items;
        }
      }
    });

    modalInstance.result.then(function (selectedItem) {
      $scope.selected = selectedItem;
    }, function () {
      $log.info('Modal dismissed at: ' + new Date());
    });
  };

  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };

});

// Please note that $uibModalInstance represents a modal window (instance) dependency.
// It is not the same as the $uibModal service used above.

app.controller('ModalInstanceCtrl', function ($scope, $uibModalInstance, items) {

  $scope.items = items;
  $scope.selected = {
    item: $scope.items[0]
  };

  $scope.ok = function () {
    $uibModalInstance.close($scope.selected.item);
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
});


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


