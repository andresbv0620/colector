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

//////////////Reporte por formid////////////////////////7
app.controller('reporteFormularioId', ['$scope', '$routeParams', 'defaultService', 'globales', function($scope, $routeParams, defaultService, globales) {
    //////////Se resta para obtener el anterior y en el siguiente llamado se le suma para volver al actual////////////
    formidanterior=$routeParams.form_id-1;
    $scope.loading = true;
    //////////////////////////////ENCABEZADO PARA PASSWORD FORMID-1///////////////////////////////////
    //($routeParams.form_id)-1
    if ($routeParams.form_id==27) {
        defaultService.get(globales.static_url + '../service/filled/forms/report/formid/' + formidanterior + '/', function(data) {
            console.log("datos recibidos del servidor ENCABEZADO: ");
            console.log(data);
            colectorfilledforms = data['data'];

            //$scope.colectorid=colectorfilledforms[0].colector_id;

            //console.log(filledforms);

            tableheader = [];
            columns = new Array();
            data = new Array();
            tablecontent2 = new Object();
            markersArray = new Array();

            ////Inicializo los encabezados por defecto de la tabla reporte, Hora inicio, Hora final ////////////
            /*column = new Object();
            column['field'] = "Start";
            column['sortable'] = true;
            column['title'] = "Start";
            columns.push(column);*/

            column = new Object();
            column['field'] = "Date";
            column['sortable'] = true;
            column['title'] = "Date";
            columns.push(column);

            ////For que recorre cada documento de colector (cada colector tiene un documento donde se guardan los registros filled_forms)
            for (colectorDocument in colectorfilledforms) {
                filledforms = colectorfilledforms[colectorDocument].filled_forms;
                //$scope.filledforms=filledforms;
                //console.log(filledforms);
     
                 //Cada registro o fila en la tabla
                for (form in filledforms) {
                    //If que filtra solo el reporte del form_id seleccionado
                    if (filledforms[form].form_id == formidanterior) {
                        $scope.formnameencabezado=filledforms[form].form_name;

                        ///////////Se asignan las coordenadas GPS del registro/////////////////
                        datacolumns = new Object(); //Objeto que va guardando las respuestas de cada registro
                        //markers objeto usado para el mapa
                        markers = {};
                        markers['longitude'] = filledforms[form].latitud;
                        markers['latitude'] = filledforms[form].longitud;
                        
                        datacolumns["View Map"]="<a href='#/reporte/id/"+ $routeParams.form_id +"/"+markers['longitude']+"/"+markers['latitude']+"'>View Map</a>";

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
                                if (typeof datacolumns[inputLabel] !== "undefined") {
                                    datacolumns[inputLabel] = datacolumns[inputLabel] + '<img width="50px" height="50px" src="data:image/png;base64,' + inputValue + '" data-err-src="images/png/avatar.png"/>';
                                } else {
                                    datacolumns[inputLabel] = '<img width="50px" height="50px" src="data:image/png;base64,' + inputValue + '" data-err-src="images/png/avatar.png"/>';
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

                        horafin = filledforms[form].horafin;
                        var dfin = new Date(0);
                        dfin.setUTCSeconds(horafin);
                        datacolumns["Date"] = dfin;

                        datacolumns["Delete"] = '<a href="#/reporte/id/'+$routeParams.form_id+'/record/delete/'+filledforms[form].record_id+'">Delete</a>';

                        //Se guardan las respuestas de la fila en el objeto data
                        data.push(datacolumns);
                        markersArray.push(markers);
                    }//Fin If que filtra solo el reporte del form_id seleccionado
                }///////////Fin for filas o registros/////////////////////
                //FILAS ADICIONALES, Sumatorias y totales de columnas
            }

            /////ENCABEZADOS ADICIONALES////
            //////////////MAPA EN CADA REGISTRO///////////////////
            column = new Object();
            column['field'] = "Delete";
            column['sortable'] = true;
            column['title'] = "Delete";
            columns.push(column);


            tablecontent2['columns'] = columns;
            tablecontent2['data'] = data;


            //$scope.tableheaders = tableheader;
            $('#table2').bootstrapTable(tablecontent2);

            ////Cambio el estado del loading para que no se muestre una vez cargado todo success
            //$scope.loading = false;

        },
         function(error) {
            console.log(error)
        });
    

       ////////////////////////////////LLAMADO AL SERVICIO QUE DEVUELVE FORMULARIOS DILIGENCIADOS/////////////////////////////////////////////
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

            ////Inicializo los encabezados por defecto de la tabla reporte, Hora inicio, Hora final ////////////
            /*column = new Object();
            column['field'] = "Start";
            column['sortable'] = true;
            column['title'] = "Start";
            columns.push(column);*/

            column = new Object();
            column['field'] = "Date";
            column['sortable'] = true;
            column['title'] = "Date";
            columns.push(column);

            ////For que recorre cada documento de colector (cada colector tiene un documento donde se guardan los registros filled_forms)
            for (colectorDocument in colectorfilledforms) {
                filledforms = colectorfilledforms[colectorDocument].filled_forms;
                //$scope.filledforms=filledforms;
                console.log(filledforms);

                //Inicialiar variables totales
                blackm=0;
                blackf=0;
                hispanicm=0;
                hispanicf=0;
                asianorpacificm=0;
                asianorpacificf=0;
                americanindianm=0;
                americanindianf=0;

                //Totales por level, jorneyman | apprentice,trainee
                blackmj=0;
                blackfj=0;
                hispanicmj=0;
                hispanicfj=0;
                asianorpacificmj=0;
                asianorpacificfj=0;
                americanindianmj=0;
                americanindianfj=0;

                blackmt=0;
                blackft=0;
                hispanicmt=0;
                hispanicft=0;
                asianorpacificmt=0;
                asianorpacificft=0;
                americanindianmt=0;
                americanindianft=0;

                totalmj=0;
                totalfj=0;
                totalmt=0;
                totalft=0;



                //Cada registro o fila en la tabla
                for (form in filledforms) {
                    //If que filtra solo el reporte del form_id seleccionado
                    if (filledforms[form].form_id == $routeParams.form_id) {
                        $scope.formname=filledforms[form].form_name;

                        ///////////Se asignan las coordenadas GPS del registro/////////////////
                        datacolumns = new Object(); //Objeto que va guardando las respuestas de cada registro
                        //markers objeto usado para el mapa
                        markers = {};
                        markers['longitude'] = filledforms[form].latitud;
                        markers['latitude'] = filledforms[form].longitud;
                        
                        datacolumns["View Map"]="<a href='#/reporte/id/"+ $routeParams.form_id +"/"+markers['longitude']+"/"+markers['latitude']+"'>View Map</a>";

                        responses = filledforms[form].responses;
                        respuestas = new Array();

                        //inicializo variables para cada fila
                        totalm=0;
                        totalf=0;
                        minoritym=0;
                        minorityf=0;

                        //Determinar el tipo de fila level=journeyman | trainee
                        levelrow="";

                        //Cada respuesta o columna en una fila
                        for (response in responses) {
                            inputId = responses[response].inputs_id;
                            if (typeof markers['message'] == "undefined") {
                                markers['message'] = responses[response].value;
                            }
                            inputValue = responses[response].value;
                            inputLabel = responses[response].label;
                            inputType = responses[response].tipo;

                            //Determinar el tipo de fila level=journeyman | trainee
                            if (inputLabel=="Level") {
                                levelrow=inputValue;
                            }
                            

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
                                    datacolumns[inputLabel] = '<p class="text-center">'+inputValue+'</p>';
                                    //Calculo reporte para password
                                    //Suma de monorities por fila
                                    if ((inputLabel=="Black M")||(inputLabel=="Hispanic M")||(inputLabel=="Asian or Pacific Islander M")||(inputLabel=="American Indian or Alaskan Native M")){
                                        minoritym=minoritym+inputValue;
                                    }
                                    if ((inputLabel=="Black F")||(inputLabel=="Hispanic F")||(inputLabel=="Asian or Pacific Islander F")||(inputLabel=="American Indian or Alaskan Native F")){
                                        minorityf=minorityf+inputValue;
                                    }


                                    //////////////////////////TOTALES COLUMNAS/////////////////////

                                    if ((inputLabel=="TOTAL EMPLOYEES M")){
                                        totalm=inputValue;
                                        if (levelrow=="Journeyman") {
                                            totalmj=totalmj+inputValue;
                                        }else{
                                            totalmt=totalmt+inputValue;
                                        }
                                    }
                                    if ((inputLabel=="TOTAL EMPLOYEES F")){
                                        totalf=inputValue;
                                        if (levelrow=="Journeyman") {
                                            totalfj=totalfj+inputValue;
                                        }else{
                                            totalft=totalft+inputValue;
                                        }
                                    }

                                    if (inputLabel=="Black M"){
                                        blackm=blackm+inputValue;
                                        if (levelrow=="Journeyman") {
                                            blackmj=blackmj+inputValue;
                                        }else{
                                            blackmt=blackmt+inputValue;
                                        }
                                    }
                                    if(inputLabel=="Hispanic M"){
                                        hispanicm=hispanicm+inputValue;
                                        if (levelrow=="Journeyman") {
                                            hispanicmj=hispanicmj+inputValue;
                                        }else{
                                            hispanicmt=hispanicmt+inputValue;
                                        }

                                    }
                                    if(inputLabel=="Asian or Pacific Islander M"){
                                        asianorpacificm=asianorpacificm+inputValue;
                                        if (levelrow=="Journeyman") {
                                            asianorpacificmj=asianorpacificmj+inputValue;
                                        }else{
                                            asianorpacificmt=asianorpacificmt+inputValue;
                                        }

                                    }
                                    if(inputLabel=="American Indian or Alaskan Native M"){
                                        americanindianm=americanindianm+inputValue;
                                        if (levelrow=="Journeyman") {
                                            americanindianmj=americanindianmj+inputValue;
                                        }else{
                                            americanindianmt=americanindianmt+inputValue;
                                        }
                                    }

                                    if (inputLabel=="Black F"){
                                        blackf=blackf+inputValue;
                                        if (levelrow=="Journeyman") {
                                            blackfj=blackfj+inputValue;
                                        }else{
                                            blackft=blackft+inputValue;
                                        }

                                    }
                                    if(inputLabel=="Hispanic F"){
                                        hispanicf=hispanicf+inputValue;
                                        if (levelrow=="Journeyman") {
                                            hispanicfj=hispanicfj+inputValue;
                                        }else{
                                            hispanicft=hispanicft+inputValue;
                                        }

                                    }
                                    if(inputLabel=="Asian or Pacific Islander F"){
                                        asianorpacificf=asianorpacificf+inputValue;
                                        if (levelrow=="Journeyman") {
                                            asianorpacificfj=asianorpacificfj+inputValue;
                                        }else{
                                            asianorpacificft=asianorpacificft+inputValue;
                                        }

                                    }
                                    if(inputLabel=="American Indian or Alaskan Native F"){
                                        americanindianf=americanindianf+inputValue;
                                        if (levelrow=="Journeyman") {
                                            americanindianfj=americanindianfj+inputValue;
                                        }else{
                                            americanindianft=americanindianft+inputValue;
                                        }


                                    }

                                }
                            }

                            //Reporte para foto, Se valida si es foto, para convertirla de base64
                            if ((inputType == 6)||(inputType==14)) {
                                if (typeof datacolumns[inputLabel] !== "undefined") {
                                    datacolumns[inputLabel] = datacolumns[inputLabel] + '<img width="50px" height="50px" src="data:image/png;base64,' + inputValue + '" data-err-src="images/png/avatar.png"/>';
                                } else {
                                    datacolumns[inputLabel] = '<img width="50px" height="50px" src="data:image/png;base64,' + inputValue + '" data-err-src="images/png/avatar.png"/>';
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
                        datacolumns["Non Minority M"]=totalm-minoritym;
                        datacolumns["Non Minority F"]=totalf-minorityf;


                        datacolumns["Minority %"]=Number((((minoritym+minorityf)/(totalm+totalf))*100).toFixed(1));

                        datacolumns["Female %"]=Number((((totalf)/(totalm+totalf))*100).toFixed(1));
                        datacolumns["Total Minority M"]=minoritym;
                        datacolumns["Total Minority F"]=minorityf;
                        
                        ///////////Se asigna la hora de inicio y fin del registro a las respuestas////////////////
                        /*horaini = filledforms[form].horaini;
                        var dini = new Date(0);
                        dini.setUTCSeconds(horaini);
                        datacolumns["Start"] = dini;*/

                        horafin = filledforms[form].horafin;
                        var dfin = new Date(0);
                        dfin.setUTCSeconds(horafin);
                        datacolumns["Date"] = dfin;

                        datacolumns["Delete"] = '<a href="#/reporte/id/'+$routeParams.form_id+'/record/delete/'+filledforms[form].record_id+'">Delete</a>';

                        //Se guardan las respuestas de la fila en el objeto data
                        data.push(datacolumns);
                        markersArray.push(markers);
                    }//Fin If que filtra solo el reporte del form_id seleccionado
                }///////////Fin for filas o registros/////////////////////
                //FILAS ADICIONALES, Sumatorias y totales de columnas

                //1 Fila adicional J (journeyman)
                datacolumns = new Object(); //Objeto que va guardando las respuestas de cada registro
                datacolumns["Level"] = "<strong>Total Journeyman</strong>";
                datacolumns["Black M"] =blackmj;
                datacolumns["Black F"] =blackfj;
                datacolumns["Hispanic M"] =hispanicmj;
                datacolumns["Hispanic F"] =hispanicfj;
                datacolumns["Asian or Pacific Islander M"] =asianorpacificmj;
                datacolumns["Asian or Pacific Islander F"] =asianorpacificfj;
                datacolumns["American Indian or Alaskan Native M"] =americanindianmj;
                datacolumns["American Indian or Alaskan Native F"] =americanindianfj;
                datacolumns["TOTAL EMPLOYEES M"] =totalmj;
                datacolumns["TOTAL EMPLOYEES F"] =totalfj;
                totalminoritymj=blackmj+hispanicmj+asianorpacificmj+americanindianmj;
                totalminorityfj=blackfj+hispanicfj+asianorpacificfj+americanindianfj;

                datacolumns["Non Minority M"] =totalmj-totalminoritymj;
                datacolumns["Non Minority F"] =totalfj-totalminorityfj;
                
                porminorityj=((totalminoritymj+totalminorityfj)/(totalmj+totalfj))*100;
                datacolumns["Minority %"] =Number((porminorityj).toFixed(1));
                
                porfemalej=(totalfj/(totalmj+totalfj))*100;
                datacolumns["Female %"]=Number((porfemalej).toFixed(1));

                datacolumns["Total Minority M"]=totalminoritymj;
                datacolumns["Total Minority F"]=totalminorityfj;

                //Se guardan las respuestas de la fila en el objeto data
                data.push(datacolumns);

                //2 Fila adicional J (journeyman)
                datacolumns = new Object(); //Objeto que va guardando las respuestas de cada registro
                datacolumns["Level"] = "<strong>Total Apprentice|Trainee</strong>";
                datacolumns["Black M"] =blackmt;
                datacolumns["Black F"] =blackft;
                datacolumns["Hispanic M"] =hispanicmt;
                datacolumns["Hispanic F"] =hispanicft;
                datacolumns["Asian or Pacific Islander M"] =asianorpacificmt;
                datacolumns["Asian or Pacific Islander F"] =asianorpacificft;
                datacolumns["American Indian or Alaskan Native M"] =americanindianmt;
                datacolumns["American Indian or Alaskan Native F"] =americanindianft;
                datacolumns["TOTAL EMPLOYEES M"] =totalmt;
                datacolumns["TOTAL EMPLOYEES F"] =totalft;
                totalminoritymt=blackmt+hispanicmt+asianorpacificmt+americanindianmt;
                totalminorityft=blackft+hispanicft+asianorpacificft+americanindianft;

                datacolumns["Non Minority M"] =totalmt-totalminoritymt;
                datacolumns["Non Minority F"] =totalft-totalminorityft;

                porminorityt=((totalminoritymt+totalminorityft)/(totalmt+totalft))*100;
                datacolumns["Minority %"] =Number((porminorityt).toFixed(1));
                
                porfemalet=(totalft/(totalmt+totalft))*100;
                datacolumns["Female %"]=Number((porfemalet).toFixed(1));
                
                datacolumns["Total Minority M"]=totalminoritymt;
                datacolumns["Total Minority F"]=totalminorityft;

                //Se guardan las respuestas de la fila en el objeto data
                data.push(datacolumns);

                //3 Fila adicional
                datacolumns = new Object(); //Objeto que va guardando las respuestas de cada registro
                datacolumns["Level"] = "<strong>Total Workforce</strong>";
                datacolumns["Black M"] =blackm;
                datacolumns["Black F"] =blackf;
                datacolumns["Hispanic M"] =hispanicm;
                datacolumns["Hispanic F"] =hispanicf;
                datacolumns["Asian or Pacific Islander M"] =asianorpacificm;
                datacolumns["Asian or Pacific Islander F"] =asianorpacificf;
                datacolumns["American Indian or Alaskan Native M"] =americanindianm;
                datacolumns["American Indian or Alaskan Native F"] =americanindianf;
                datacolumns["TOTAL EMPLOYEES M"] =totalmt+totalmj;
                datacolumns["TOTAL EMPLOYEES F"] =totalft+totalfj;
                totalminoritym=blackm+hispanicm+asianorpacificm+americanindianm;
                totalminorityf=blackf+hispanicf+asianorpacificf+americanindianf;

                datacolumns["Non Minority M"] =(totalmt+totalmj)-totalminoritym;
                datacolumns["Non Minority F"] =(totalft+totalfj)-totalminorityf;
                
                
                porminority=((totalminoritym+totalminorityf)/(totalmt+totalmj+totalft+totalfj))*100;
                datacolumns["Minority %"] =Number((porminority).toFixed(1));

                porfemale=((totalft+totalfj)/(totalmt+totalmj+totalft+totalfj))*100;
                datacolumns["Female %"]=Number((porfemale).toFixed(1));
                datacolumns["Total Minority M"]=totalminoritym;
                datacolumns["Total Minority F"]=totalminorityf;
                datacolumns["View Map"]="<strong>Total = "+totalminoritym+totalminorityf+"</strong>";

                //Se guardan las respuestas de la fila en el objeto data
                data.push(datacolumns);

            }


            /////ENCABEZADOS ADICIONALES////


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

            column = new Object();
            column['field'] = "Minority %";
            column['sortable'] = true;
            column['title'] = "Minority %";
            columns.push(column);

            column = new Object();
            column['field'] = "Female %";
            column['sortable'] = true;
            column['title'] = "Female %";
            columns.push(column);

            column = new Object();
            column['field'] = "Total Minority M";
            column['sortable'] = true;
            column['title'] = "Total Minority M";
            columns.push(column);

            column = new Object();
            column['field'] = "Total Minority F";
            column['sortable'] = true;
            column['title'] = "Total Minority F";
            columns.push(column);

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

            ////Cambio el estado del loading para que no se muestre una vez cargado todo success
            $scope.loading = false;

        }, function(error) {
            console.log(error)
        });
    }

    ////////////////////////////////LLAMADO AL SERVICIO QUE DEVUELVE FORMULARIOS DILIGENCIADOS/////////////////////////////////////////////
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

        ////Inicializo los encabezados por defecto de la tabla reporte, Hora inicio, Hora final ////////////
        /*column = new Object();
        column['field'] = "Start";
        column['sortable'] = true;
        column['title'] = "Start";
        columns.push(column);*/

        column = new Object();
        column['field'] = "Date";
        column['sortable'] = true;
        column['title'] = "Date";
        columns.push(column);

        ////For que recorre cada documento de colector (cada colector tiene un documento donde se guardan los registros filled_forms)
        for (colectorDocument in colectorfilledforms) {
            filledforms = colectorfilledforms[colectorDocument].filled_forms;
            //$scope.filledforms=filledforms;
            console.log(filledforms);

            //Cada registro o fila en la tabla
            for (form in filledforms) {
                //If que filtra solo el reporte del form_id seleccionado
                if (filledforms[form].form_id == $routeParams.form_id) {
                    $scope.formname=filledforms[form].form_name;

                    ///////////Se asignan las coordenadas GPS del registro/////////////////
                    datacolumns = new Object(); //Objeto que va guardando las respuestas de cada registro
                    //markers objeto usado para el mapa
                    markers = {};
                    markers['longitude'] = filledforms[form].latitud;
                    markers['latitude'] = filledforms[form].longitud;
                    
                    datacolumns["View Map"]="<a target='_blank' href='#/reporte/id/"+ $routeParams.form_id +"/"+markers['longitude']+"/"+markers['latitude']+"'>View Map</a>";

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
                            if (typeof datacolumns[inputLabel] !== "undefined") {
                                datacolumns[inputLabel] = datacolumns[inputLabel] + '<img width="50px" height="50px" src="data:image/png;base64,' + inputValue + '" data-err-src="images/png/avatar.png"/>';
                            } else {
                                datacolumns[inputLabel] = '<img width="50px" height="50px" src="data:image/png;base64,' + inputValue + '" data-err-src="images/png/avatar.png"/>';
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
                    /*horaini = filledforms[form].horaini;
                    var dini = new Date(0);
                    dini.setUTCSeconds(horaini);
                    datacolumns["Start"] = dini;*/

                    horafin = filledforms[form].horafin;
                    var dfin = new Date(0);
                    dfin.setUTCSeconds(horafin);
                    datacolumns["Date"] = dfin;

                    datacolumns["Delete"] = '<a href="#/reporte/id/'+$routeParams.form_id+'/record/delete/'+filledforms[form].record_id+'">Delete</a>';

                    //Se guardan las respuestas de la fila en el objeto data
                    data.push(datacolumns);
                    markersArray.push(markers);
                }//Fin If que filtra solo el reporte del form_id seleccionado
            }///////////Fin for filas o registros/////////////////////
            //FILAS ADICIONALES, Sumatorias y totales de columnas

            

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

        ////Cambio el estado del loading para que no se muestre una vez cargado todo success
        $scope.loading = false;

    }, function(error) {
        console.log(error)
    });

}]);

///////////////////Reporte Mapa/////////////////////////////
app.controller('reporteMapa', ['$scope', '$routeParams', 'defaultService', 'globales', function($scope, $routeParams, defaultService, globales) {
    $scope.form_name = $routeParams.form_id;
    longitud = $routeParams.longitud;
    latitud = $routeParams.latitud;
    $scope.loading = true;

    ///////////////////////////////MAPS REPORT////////////////////////

        $scope.map = {
            center: {
                latitude: latitud,
                longitude: longitud
            },
            zoom: 12
        };

        $scope.marker = {
            coords: {
                latitude: latitud,
                longitude: longitud
            }
        }
        $scope.markerList = markersArray;

    $scope.loading = false;


}]);


//////////////////////////DELETE RECORD////////////////////////////777

app.controller('deleteRecord', ['$scope', '$routeParams', 'defaultService', 'globales', function($scope, $routeParams, defaultService, globales) {
    colector_id = globales.user_id;
    record_id = $routeParams.record_id;
    $scope.loading = true;
    defaultService.post(globales.static_url + '../service/form/delete/' + record_id + '/', '{"colector_id":"' + colector_id + '","record_id":"'+record_id+'"}', function(data) {
       $scope.notificacion = "The record has been deleted";
    }, function(error) {
        console.log(error)
    });
    //////////Se resta para obtener el anterior y en el siguiente llamado se le suma para volver al actual////////////
    formidanterior=$routeParams.form_id-1;
    $scope.loading = true;

               ////////////////////////////////LLAMADO AL SERVICIO QUE DEVUELVE FORMULARIOS DILIGENCIADOS/////////////////////////////////////////////
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

            ////Inicializo los encabezados por defecto de la tabla reporte, Hora inicio, Hora final ////////////
            /*column = new Object();
            column['field'] = "Start";
            column['sortable'] = true;
            column['title'] = "Start";
            columns.push(column);*/

            column = new Object();
            column['field'] = "Date";
            column['sortable'] = true;
            column['title'] = "Date";
            columns.push(column);

            ////For que recorre cada documento de colector (cada colector tiene un documento donde se guardan los registros filled_forms)
            for (colectorDocument in colectorfilledforms) {
                filledforms = colectorfilledforms[colectorDocument].filled_forms;
                //$scope.filledforms=filledforms;
                console.log(filledforms);

                //Cada registro o fila en la tabla
                for (form in filledforms) {
                    //If que filtra solo el reporte del form_id seleccionado
                    if (filledforms[form].form_id == $routeParams.form_id) {
                        $scope.formname=filledforms[form].form_name;

                        ///////////Se asignan las coordenadas GPS del registro/////////////////
                        datacolumns = new Object(); //Objeto que va guardando las respuestas de cada registro
                        //markers objeto usado para el mapa
                        markers = {};
                        markers['longitude'] = filledforms[form].latitud;
                        markers['latitude'] = filledforms[form].longitud;
                        
                        datacolumns["View Map"]="<a target='_blank' href='#/reporte/id/"+ $routeParams.form_id +"/"+markers['longitude']+"/"+markers['latitude']+"'>View Map</a>";

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
                                if (typeof datacolumns[inputLabel] !== "undefined") {
                                    datacolumns[inputLabel] = datacolumns[inputLabel] + '<img width="50px" height="50px" src="data:image/png;base64,' + inputValue + '" data-err-src="images/png/avatar.png"/>';
                                } else {
                                    datacolumns[inputLabel] = '<img width="50px" height="50px" src="data:image/png;base64,' + inputValue + '" data-err-src="images/png/avatar.png"/>';
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
                        /*horaini = filledforms[form].horaini;
                        var dini = new Date(0);
                        dini.setUTCSeconds(horaini);
                        datacolumns["Start"] = dini;*/

                        horafin = filledforms[form].horafin;
                        var dfin = new Date(0);
                        dfin.setUTCSeconds(horafin);
                        datacolumns["Date"] = dfin;

                        datacolumns["Delete"] = '<a href="#/reporte/id/'+$routeParams.form_id+'/record/delete/'+filledforms[form].record_id+'">Delete</a>';

                        //Se guardan las respuestas de la fila en el objeto data
                        data.push(datacolumns);
                        markersArray.push(markers);
                    }//Fin If que filtra solo el reporte del form_id seleccionado
                }///////////Fin for filas o registros/////////////////////
                //FILAS ADICIONALES, Sumatorias y totales de columnas

                

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

            ////Cambio el estado del loading para que no se muestre una vez cargado todo success
            $scope.loading = false;

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