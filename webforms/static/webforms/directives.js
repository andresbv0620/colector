app.directive("paragraphSesion",['globales', function(globales){
	return{
		restrict:'E',
		templateUrl:globales.static_url+"/webforms/angular_templates/paragraph-sesion.html"
	};
}]);

app.directive("normalSesion",['globales', function(globales){
	return{
		restrict:'E',
		templateUrl:globales.static_url+"/webforms/angular_templates/normal-sesion.html"
	};
}]);

app.directive("groupedSesion",['globales', function(globales){
	return{
		restrict:'E',
		templateUrl:globales.static_url+"/webforms/angular_templates/grouped-sesion.html",
		controller: function(){
			this.groupedInput=[];
			this.focusInput=0;
		    this.isSet = function(selectInput) {
		      return this.groupedInput[selectInput];
		    };
		    this.setInput = function(setInput, active) {
		    	
		      this.groupedInput[setInput]= active;
		      this.focusInput=setInput;
		      return "";
		    };

		    this.isFocus = function(selectInput) {
		      return this.focusInput=== selectInput;
		    };        
      },
      controllerAs:'gInput'
    };
}]);

// Common directive for Focus
app.directive('focus',
	function($timeout) {
		return {
			scope : {
				trigger : '@focus'
			},
			link : function(scope, element) {
				scope.$watch('trigger', function(value) {
					if (value === "true") {
						$timeout(function() {
							element[0].focus();
						});
					}
				});
			}
		};
	}
); 



app.controller('TabController',['$scope', '$routeParams', 'defaultService', 'globales', '$window', function($scope, $routeParams, defaultService, globales, $window) {
    this.loading=true;
    $scope.form_id = $routeParams.form_id;
    $scope.templatesUrl = ''+globales.static_url+'webforms/angular_templates/';
    console.log($scope.templatesUrl);
    
    var tabsdata = this;

    defaultService.post(globales.static_url + '../service/form/single/', '{"form_id":"' + $routeParams.form_id + '"}', function(data) {
        console.log(data['response_data'][0]);
        $scope.formulario = data['response_data'][0];

        tabsdata.tabs=$scope.formulario.sections;
        tabsdata.steps=tabsdata.tabs.length;
        tabsdata.firsttab=tabsdata.tabs[0].section_id;
        tabsdata.lasttab=tabsdata.tabs[tabsdata.tabs.length-1].section_id;
        tabsdata.tab = tabsdata.firsttab;
        tabsdata.btntext = " Iniciar Diagnostico ";
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

    this.step=0;

    this.backTab = function(currentTab, currentStep){
        if (currentTab!=this.firsttab) {
            priorTab = this.tabs[currentStep-1].section_id;
            this.tab=priorTab;
            this.step=currentStep-1;              
        } 
         
    };

    this.nextTab = function(currentTab, currentStep){
        this.btntext = "Continuar";
        if (currentTab==this.lasttab) {
            this.tab=this.firsttab;
            this.sendForm($scope.formulario)
        }else{ 
        	nextTab = this.tabs[currentStep+1].section_id;
            this.tab=nextTab;
            this.step=currentStep+1;   
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
            $window.location.href = "http://finantic.co/dashboard/";
            //$window.location.href = "http://finantic.co/lp/solicitud-realizada/";
            //$window.location.href = "#/histograma/id/"+$scope.form_id;
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

