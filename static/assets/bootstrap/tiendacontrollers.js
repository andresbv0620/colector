/**
 * Created by jhon on 24/01/15.
 */
app.controller('startApp', ['$scope', 'defaultService', function ($scope, defaultService) {
 console.log("start");
 //$scope.id_usuario = $("#id_usuario").attr("value");
 $scope.servidor = "http://localhost:8000";
 //$scope.servidor = "http://54.200.219.177:8000";
 //console.log("id usuario:"+$scope.id_usuario);
 $scope.cargar_productos();
 $scope.cargar_productos = function(){
 	console.log("cargando productos");
 }


 

    
}]);

