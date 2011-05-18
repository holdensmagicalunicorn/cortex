(function() {
  var Map, Player;
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  window.map = [[1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]];
  Map = (function() {
    function Map() {}
    Map.prototype.width = 16;
    Map.prototype.height = 16;
    Map.prototype.isPassable = function(i, j) {
      if (map[i] !== void 0 && map[i][j] !== void 0) {
        if (map[i][j] === 1) {
          return true;
        } else {
          return false;
        }
      }
    };
    Map.prototype.drawMap = function() {
      var dirt, img;
      img = new Image();
      img.src = '/static/img/grass.png';
      dirt = new Image();
      dirt.src = '/static/img/dirt.png';
      return dirt.onload = function() {
        var i, j, _ref, _results;
        _results = [];
        for (i = 0, _ref = map.length; (0 <= _ref ? i < _ref : i > _ref); (0 <= _ref ? i += 1 : i -= 1)) {
          _results.push((function() {
            var _ref, _results;
            _results = [];
            for (j = 0, _ref = map[i].length; (0 <= _ref ? j < _ref : j > _ref); (0 <= _ref ? j += 1 : j -= 1)) {
              _results.push(map[i][j] === 1 ? context.drawImage(img, 16 * i, 16 * j) : context.drawImage(dirt, 16 * i, 16 * j));
            }
            return _results;
          })());
        }
        return _results;
      };
    };
    return Map;
  })();
  Player = (function() {
    Player.prototype.position = [0, 0];
    Player.prototype.pos = [0, 0];
    Player.prototype.xsize = 16;
    Player.prototype.ysize = 16;
    Player.prototype.scene = null;
    function Player(sprite, id) {
      this.sprite = sprite;
      this.id = id;
      this.move = __bind(this.move, this);;
    }
    Player.prototype.moveTo = function(x, y) {
      this.position = [x, y];
      this.sprite.position(x, y);
      return console.log('movingto');
    };
    Player.prototype.move = function(dx, dy) {
      var delta, new_i, new_j;
      new_i = this.pos[0] + dx / 16;
      new_j = this.pos[1] + dy / 16;
      if (window.scene.elements.level.isPassable(new_i, new_j)) {
        console.log(new_i, new_j);
        this.position = [this.position[0] + dx, this.position[1] + dy];
        this.sprite.move(dx, dy);
        this.pos = [new_i, new_j];
        delta = [dx, dy];
        return window.socket.send({
          event: 'message',
          message: {
            id: this.id,
            position: this.position
          }
        });
      }
    };
    return Player;
  })();
  $(document).ready(function() {
    var background, input, paint, ticker, toplayer;
    window.session_key = 'u' + Math.floor(Math.random() * 200);
    window.socket = new io.Socket(document.location.hostname);
    window.socket.connect();
    socket.on('connect', function() {
      socket.send({
        event: 'session',
        cookie: window.session_key
      });
      return console.log('connected');
    });
    socket.on('message', function(data) {
      var msg;
      if (data.event === "message") {
        msg = data.message;
        if (msg.id !== window.scene.elements.hero.id) {
          if (window.scene.elements[msg.id]) {
            window.scene.elements[msg.id].moveTo(msg.position[0], msg.position[1]);
            return console.log(data);
          } else {
            return addPlayer(msg.id).move(msg.pos);
          }
        }
      } else {
        return console.log(data);
      }
    });
    window.scene = sjs.Scene({
      w: 640,
      h: 480
    });
    background = scene.Layer('background', {
      useCanvas: true,
      autoClear: false
    });
    toplayer = scene.Layer('toplayer');
    window.sprites = sjs.SpriteList();
    input = scene.Input();
    scene.elements = {};
    scene.loadImages(['/static/img/up.png'], function() {
      var cv, guy, level;
      guy = scene.Sprite('/static/img/up.png', toplayer);
      window.sprites.add(guy);
      scene.elements.hero = new Player(guy, window.session_key);
      level = new Map();
      cv = document.getElementById('sjs0-background');
      window.context = cv.getContext('2d');
      level.drawMap();
      return scene.elements.level = level;
    });
    paint = function() {
      var el, _i, _len, _ref;
      _ref = window.sprites.list;
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        el = _ref[_i];
        el.update();
      }
      if (input.keyboard.right) {
        scene.elements.hero.move(16, 0);
      }
      if (input.keyboard.left) {
        scene.elements.hero.move(-16, 0);
      }
      if (input.keyboard.up) {
        scene.elements.hero.move(0, -16);
      }
      if (input.keyboard.down) {
        return scene.elements.hero.move(0, 16);
      }
    };
    ticker = scene.Ticker(25, paint);
    return ticker.run();
  });
  window.addPlayer = function(id) {
    var guy;
    guy = scene.Sprite('/static/img/up.png', scene.layers.toplayer);
    window.sprites.add(guy);
    window.scene.elements[id] = new Player(guy);
    return window.scene.elements[id];
  };
  window.delPlayer = function(id) {
    var player;
    player = window.scene.elements[id];
    player.sprite.remove();
    window.sprites.remove(player.sprite);
    return delete window.scene.elements[id];
  };
}).call(this);
