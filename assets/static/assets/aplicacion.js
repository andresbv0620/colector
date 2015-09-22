var app = angular.module('app', []);



app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});


app.config(['$httpProvider', function($httpProvider) {

    $httpProvider.defaults.headers.common['token'] = "d208ffcfcb94431aa49cb47758927ad7";
     delete $httpProvider.defaults.headers.common['X-Requested-With'];
    $httpProvider.defaults.useXDomain = true;

}]);


app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';    
}
]);



