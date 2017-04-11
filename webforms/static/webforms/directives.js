app.directive('currencyInput', function($filter, $browser) {
    return {
        require: 'ngModel',
        link: function($scope, $element, $attrs, ngModelCtrl) {
            var listener = function() {
                var value = $element.val().replace(/,/g, '');
                value=parseInt(value);
                $element.val($filter('number')(value));
            }
            
            // This runs when we update the text field
            ngModelCtrl.$parsers.push(function(viewValue) {
                return viewValue.replace(/,/g, '');
            })
            
            // This runs when the model gets updated on the scope directly and keeps our view in sync
            ngModelCtrl.$render = function() {
                $element.val($filter('number')(ngModelCtrl.$viewValue))
            }
            
            $element.bind('change', listener)
            $element.bind('keydown', function(event) {
                var key = event.keyCode
                // If the keys include the CTRL, SHIFT, ALT, or META keys, or the arrow keys, do nothing.
                // This lets us support copy and paste too
                if (key == 91 || (15 < key && key < 19) || (37 <= key && key <= 40)) 
                    return 
                $browser.defer(listener) // Have to do this or changes don't get picked up properly
            })
            
            $element.bind('paste cut', function() {
                $browser.defer(listener)  
            })
        }
        
    }
});

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
		    this.isSet = function(selectInput, requerido) {
                if (requerido===true) {
                    return true
                }
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
        tabsdata.firsttab=parseInt(tabsdata.tabs[0].section_id);
        //tabsdata.firstgroup=parseInt(tabsdata.tabs[0].grupo);
        tabsdata.firstgroup=1;
        tabsdata.lastgroup=1;
        for (sectiontab in tabsdata.tabs) {
            tabgrupo=tabsdata.tabs[sectiontab].grupo;
            if (tabgrupo>tabsdata.lastgroup){
                tabsdata.lastgroup=tabgrupo;
            }
            if (tabgrupo<tabsdata.firstgroup){
                tabsdata.lastgroup=tabgrupo;
            }
        }
        
        tabsdata.lasttab=parseInt(tabsdata.tabs[tabsdata.tabs.length-1].section_id);
        //tabsdata.lastgroup=tabsdata.tabs[tabsdata.tabs.length-1].grupo;
        tabsdata.steps=tabsdata.lastgroup;
        tabsdata.tab = tabsdata.firsttab;
        tabsdata.group = tabsdata.firstgroup;
        tabsdata.btntext = " Iniciar Diagnostico ";
        tabsdata.loading = false;


    }, function(error) {
        console.log(error)
    });

    this.isVisible = function(visibilityRule, formSections){
        if (visibilityRule!="") {
            var elemento=visibilityRule[0].elemento;
            var operador=visibilityRule[0].operador;
            var valor=visibilityRule[0].valor;



            for (section in formSections) {
                sectionInputs = formSections[section].inputs;
                for (sectionInput in sectionInputs) {
                    switch(operador) {
                        case 'igual_a':
                            if (sectionInputs[sectionInput].input_id===elemento && sectionInputs[sectionInput].record.value==valor) {
                                return true;
                            }
                            break;
                        case 'no_igual_a':
                            if (sectionInputs[sectionInput].input_id===elemento && sectionInputs[sectionInput].record.value!=valor) {
                                return true;
                            }
                            break;
                        case 'es_vacio':
                            if (sectionInputs[sectionInput].input_id===elemento && sectionInputs[sectionInput].record.value=='') {
                                return true;
                            }
                            break;
                        case 'no_es_vacio':
                            if (sectionInputs[sectionInput].input_id===elemento && sectionInputs[sectionInput].record.value!='') {
                                return true;
                            }
                            break;
                        case 'mayor_que':
                            if (sectionInputs[sectionInput].input_id===elemento && sectionInputs[sectionInput].record.value>valor) {
                                return true;
                            }
                            break;
                        case 'menor_que':
                            if (sectionInputs[sectionInput].input_id===elemento && sectionInputs[sectionInput].record.value<valor) {
                                return true;
                            }
                            break;
                        default:
                            if (sectionInputs[sectionInput].input_id===elemento && sectionInputs[sectionInput].record.value==valor) {
                                return true;
                            }
                    }
                    

                }
            }
        }else{
            return true
        }
    }

    this.setLayout = function(currentTab){
        if (currentTab==this.firsttab) {
            return 'col-md-5';
        }else{
            return 'col-md-8 col-md-offset-2';
        }
    };


    this.setTab = function(newValue){
      this.group = newValue;
    };


    this.isSet = function(tabId){

        return this.group == tabId;

      
    };

    this.step=0;

    this.backTab = function(currentTab, currentStep){
        currentTab=parseInt(currentTab);

        if (currentTab!=this.firstgroup) {
            this.group=currentTab-1;
             
        } 
         
    };

    this.nextTab = function(currentTab, currentStep){
        currentTab=parseInt(currentTab);
        this.btntext = "Continuar";
        if (currentTab==this.lastgroup) {
            this.group=this.firstgroup;
            
            this.sendForm($scope.formulario)
        }else{
            this.group=currentTab+1;
        }
    };

    this.sendForm = function(filledform){
        if(this.form.$valid) { 
            // Save to db or whatever.
            console.log($scope.formulario);
            
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

        defaultService.post('http://finantic.contraslash.com/diagnostics/receive-response/', this.datatoinsert, function(data) {
            console.log(data);
            $window.location.href = "http://finantic.contraslash.com/diagnostics/" + data + "/"

        }, function(error) {
            console.log(error)
        });
            swal("Registro exitoso!", "Haz click en el boton para terminar", "success");
            this.form.$setPristine();
            //$window.location.href = "http://finantic.contraslash.com/diagnostics/2/";
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


