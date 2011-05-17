$(function () {

  var AppModel = Capsule.Model.extend({

    type: 'AppModel',
    users: {},

    initialize: function (spec) {
    },

    userlist: function(user) {
        $("#users").text(user);
    },

  });

  var AppView = Capsule.View.extend({
  });

  // init our empty AppModel
  var app = window.app = new AppModel(),
      view = window.view = {};

  // init our socket
  window.socket = new io.Socket( document.location.hostname );

  socket.on('connect', function() {
    socket.send({
        event: 'session',
        cookie: window.session_key
    });
    console.log('connected');
  });

  window.socket.connect();

  socket.on('message', function (data) {
    var changedModel, template;

    console.log('RECD:', data);

    switch (data.event) {
      case 'initial':
        //import app state
        app.mport(data.app);
        app.register();

        //init our root view
        view = window.view = new AppView({
         el: $('body'),
         model: app
        });

        view.render();
        break;
      case 'change':
        changedModel = Capsule.models[data.id];
        if (changedModel) {
          changedModel.set(data.data);
        } else {
          console.error('model not found for change event', data);
        }
        break;

      case 'call':
        var model = Capsule.models[data.id];
        if(model) {
            var procedure = model[data.procedure];
            procedure.call(model, data.args);
        } else {
          console.error('model not found for procedure call', data);
        }
        break;

    }
  });
});
