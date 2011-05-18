window.map = [
    [1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    [1,0,0,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    [1,0,0,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    [1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    [1,0,0,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    [1,0,0,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    [1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    [1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    [1,1,1,1,1,1,0,1,1,1,1,1,0,1,0,0,0,0,1,1,1,1,1,1,1]
    [1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,0,0,1,1,1,1,1,1]
    [1,1,1,1,1,1,0,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,1,1,1]
    [1,1,1,1,1,1,0,1,1,1,1,0,1,0,0,1,1,1,0,1,1,1,1,1,1]
    [1,1,1,1,1,1,0,1,1,1,1,0,1,0,0,1,1,0,0,1,1,1,1,1,1]
    [1,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,1,1]
    [1,1,1,1,1,1,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1]
    [1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    [1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    [1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    [1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    [1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]


class Map

    width: 16
    height: 16

    isPassable: (i,j) ->
        if map[i] != undefined && map[i][j] != undefined
            # Grass
            if map[i][j] == 1
                return true
            # Rock
            else
                return false

    drawMap: () ->

        img = new Image()
        img.src = '/static/img/grass.png'

        dirt = new Image()
        dirt.src = '/static/img/dirt.png'

        dirt.onload = () ->

            for i in [0...map.length]
                for j in [0...map[i].length]
                    if map[i][j] == 1
                        context.drawImage(img,16*i,16*j)
                    else
                        context.drawImage(dirt,16*i,16*j)

class Player

    # Spatial coordinates on screen
    position: [0,0]

    # Arary indexes for map
    pos: [0,0]

    xsize: 16
    ysize: 16
    scene: null

    constructor: (@sprite,@id) ->

    moveTo: (x,y) ->
        @position = [x,y]
        @sprite.position(x,y)
        console.log('movingto')

    move: (dx,dy) =>
        new_i = @pos[0]+dx/16
        new_j = @pos[1]+dy/16

        if window.scene.elements.level.isPassable(new_i,new_j)
            console.log(new_i,new_j)
            @position = [@position[0]+dx,@position[1]+dy]
            @sprite.move(dx,dy)
            @pos = [new_i,new_j]
            delta = [dx,dy]

            window.socket.send
                event: 'message',
                message: {
                    @id,
                    @position
                }

$(document).ready ()->

    # Session Information / Handlers
    window.session_key = 'u' + Math.floor(Math.random()*200)
    window.socket = new io.Socket( document.location.hostname )
    window.socket.connect()

    socket.on 'connect', () ->
        socket.send
            event: 'session',
            cookie: window.session_key

        console.log('connected')

    socket.on 'message', (data) ->
        if data.event == "message"
            msg = data.message
            if msg.id != window.scene.elements.hero.id
                if window.scene.elements[msg.id]
                    window.scene.elements[msg.id].moveTo(msg.position[0],msg.position[1])
                    console.log data
                else
                    addPlayer(msg.id).move(msg.pos)
        else
            console.log data

    window.scene = sjs.Scene({w:640, h:480})
    background = scene.Layer 'background',
        useCanvas:true,
        autoClear: false

    toplayer = scene.Layer 'toplayer'
    window.sprites = sjs.SpriteList()

    input = scene.Input()
    scene.elements = {}

    scene.loadImages ['/static/img/up.png'], () ->
        guy = scene.Sprite('/static/img/up.png',toplayer)

        window.sprites.add(guy)
        scene.elements.hero = new Player(guy, window.session_key)

        level = new Map()
        cv = document.getElementById('sjs0-background')
        window.context = cv.getContext('2d')
        level.drawMap()
        scene.elements.level = level

    # Main Event Loop
    paint = () ->
        for el in window.sprites.list
            el.update()

        if input.keyboard.right
            scene.elements.hero.move(16,0)

        if input.keyboard.left
            scene.elements.hero.move(-16,0)

        if input.keyboard.up
            scene.elements.hero.move(0,-16)

        if input.keyboard.down
            scene.elements.hero.move(0,16)
    
    ticker = scene.Ticker(25, paint)
    ticker.run()

window.addPlayer = (id) ->
    guy = scene.Sprite('/static/img/up.png',scene.layers.toplayer)
    window.sprites.add(guy)
    window.scene.elements[id] = new Player(guy)
    return window.scene.elements[id]

window.delPlayer = (id) ->
    player = window.scene.elements[id]
    player.sprite.remove()
    window.sprites.remove(player.sprite)
    delete window.scene.elements[id]
