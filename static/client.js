$(function () {

  // Connected Users
  var Client = Capsule.Model.extend({
  });

  // Collection of Connected Users
  var ClientList = Capsule.Collection.extend({
      model: Client
  });

  var AppModel = Capsule.Model.extend({
    type: 'app',
    initialize: function (spec) {
    }
  });

  var AppView = Capsule.View.extend({
  });


  // init our empty AppModel
  var app = window.app = new AppModel(),
    view = window.view = {},
    server;

  app.type = 'AppModel';

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
      //case 'templates':
        //for (template in data.templates) {
          //ich.addTemplate(template, data.templates[template]);
        //}
        //break;
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
      case 'add':
        Capsule.models[data.collection].add(data.data.attrs);
        break;
      case 'remove':
        changedModel = Capsule.models[data.id];
        if (changedModel && changedModel.collection) {
          changedModel.collection.remove(changedModel);
        }
        break;
    }
  });
});
