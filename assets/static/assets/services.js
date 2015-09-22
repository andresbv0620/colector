app.factory('defaultService', function($http){

    return {

        get: function (url, callback, error) {
            $http.get(url).success(callback).error(error);


        },
        

        put: function (url, data, callback, error) {
            $http.put(url, data).success(callback).error(error);

        },

        delete: function (url, callback, error) {
            $http.delete(url).success(callback).error(error);

        },

        post: function (url, data, callback, error) {
            $http.post(url, data).success(callback).error(error);

        }

    }
});

app.factory('ContenidoNotificacionesService', function($http){

    var service = {};

    var data = [
      {'nombre':'Notificacion 1','autor':"jhon", "fecha":"August 12, 2012.", "contenido":"Bacon ipsum dolor sit amet nulla ham qui sint exercitation eiusmod commodo, chuck duis velit. Aute in reprehenderit, dolore aliqua non est magna in labore pig pork biltong. Eiusmod swine spare ribs reprehenderit culpa.", "id_notificacion":0},
      {'nombre':'Notificacion 2','autor':"pedro","fecha":"August 12, 2012.", "contenido":"Bacon ipsum dolor sit amet nulla ham qui sint exercitation eiusmod commodo, chuck duis velit. Aute in reprehenderit, dolore aliqua non est magna in labore pig pork biltong. Eiusmod swine spare ribs reprehenderit culpa.", "id_notificacion":1},
      {'nombre':'Notificacion 3','autor':"jhon", "fecha":"August 12, 2012.", "contenido":"Bacon ipsum dolor sit amet nulla ham qui sint exercitation eiusmod commodo, chuck duis velit. Aute in reprehenderit, dolore aliqua non est magna in labore pig pork biltong. Eiusmod swine spare ribs reprehenderit culpa.", "id_notificacion":2},
      {'nombre':'Notificacion 3','autor':"jhon", "fecha":"August 12, 2012.", "contenido":"Bacon ipsum dolor sit amet nulla ham qui sint exercitation eiusmod commodo, chuck duis velit. Aute in reprehenderit, dolore aliqua non est magna in labore pig pork biltong. Eiusmod swine spare ribs reprehenderit culpa.", "id_notificacion":2}
      ];

    service.getAll = function(){


        return data;
    }

    service.get = function(id){
        for( n in data){
            if(data[n].id == id){
                return data[n];
            }
        }
    }

    service.del = function(id){

        for( n in data){
            if(data[n].id == id){
                //console.log(notificaciones[n]);
                 data.splice(n, 1);
            }
        }
    }


    service.post = function(d){
        data.push(d);

    }


    service.put = function(id, d){
        for( n in data){
            if(data[n].id == id){
                data[n] = d;
            }
        }
    }


    return service;

});
