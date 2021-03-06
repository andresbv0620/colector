var app = angular.module('app', ['ngRoute','uiGmapgoogle-maps','ui.bootstrap','bsTable']);

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
	.when('/form/:form_id',{
		templateUrl:globales.static_url+"/webforms/angular_templates/fill_form.html"
	})
	.when('/llenar/:form_id',{
		controller:"llenarFormulario",
		templateUrl:globales.static_url+"/administrador/angular_templates/llenar_formulario.html"
	})
	.when('/llenar2/:form_id',{
		controller:"llenarFormulario",
		templateUrl:globales.static_url+"/administrador/angular_templates/llenar_formulario2.html"
	})
	.when('/reporte/id/:form_id',{
		controller:"reporteFormularioId",
		templateUrl:globales.static_url+"/administrador/angular_templates/reporte_formulario.html"
	})
	.when('/reporte/id/:form_id/:longitud/:latitud',{
		controller:"reporteMapa",
		templateUrl:globales.static_url+"/administrador/angular_templates/reporte_mapa.html"
	})
	.when('/reporte/id/:form_id/record/delete/:record_id',{
		controller:"deleteRecord",
		templateUrl:globales.static_url+"/administrador/angular_templates/reporte_formulario.html"
	})
	.when('/reporte/id/:form_id/page/:page/limit/:limit',{
		controller:"FormIdReportPaginate",
		templateUrl:globales.static_url+"/administrador/angular_templates/reporte_formulario_paginate.html"
	})
	.when('/reportepag/id/:form_id',{
		controller:"serverSidePagController",
		templateUrl:globales.static_url+"/administrador/angular_templates/reporte_server_pagination.html"
	})
	.when('/histograma/id/:form_id',{
		controller:"generarHistograma",
		templateUrl:globales.static_url+"/administrador/angular_templates/reporte_server_pagination.html"
	})


}]);



