var app = angular.module('app', ['ngRoute','uiGmapgoogle-maps']);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});


app.config(['$httpProvider','globales', function($httpProvider, globales) {
	

    $httpProvider.defaults.headers.common['token'] = globales.auth_token;
     delete $httpProvider.defaults.headers.common['X-Requested-With'];
    $httpProvider.defaults.useXDomain = true;

}]);


app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';    
}
]);

app.config(['$routeProvider','globales', function($routeProvider, globales) {
	$routeProvider
	.when('/reporte/',{
		controller:"reporteFormulario",
		templateUrl:globales.static_url+"/administrador/angular_templates/reporte_formulario.html"
	})
	.when('/llenar/:form_id',{
		controller:"llenarFormulario",
		templateUrl:globales.static_url+"/administrador/angular_templates/llenar_formulario.html"
	})
	.when('/reporte/id/:form_id',{
		controller:"reporteFormularioId",
		templateUrl:globales.static_url+"/administrador/angular_templates/reporte_formulario.html"
	})
	.when('/reporte/id/:form_id/:longitud/:latitud',{
		controller:"reporteMapa",
		templateUrl:globales.static_url+"/administrador/angular_templates/reporte_formulario.html"
	})
	.when('/reporte/id/:form_id/record/delete/:record_id',{
		controller:"deleteRecord",
		templateUrl:globales.static_url+"/administrador/angular_templates/reporte_formulario.html"
	})


}]);



