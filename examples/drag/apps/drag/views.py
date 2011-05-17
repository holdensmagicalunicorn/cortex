from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from drag.models import AppModel
from cortex import SessionPool, Channel, WebsocketHandler
Sessions = SessionPool();

# Establish a correspondance between the `.type` attribute
# attached to Backbone models and their counterpart in the
# Django ORM.
CapsuleModels = {
    'AppModel': AppModel
}

# The initial `app` model created upon a `session` event call.
app = {
    'type': 'AppModel',
    'attributes': {
        'toggler': False,
    },
    'id': 1
}

class Dragger(Channel):

    name = 'dragger'
    users = set([])

    def subscribe(self, user, socket):
        # Add a socket subscription to this channel
        self.add_subscriber(socket)

        # Add a user to users set
        self.users.add(user)

    def unsubscribe(self, user, socket):
        # Remove socket subscription
        self.del_subscriber(socket)

        # Remove the user
        self.users.discard(user.username)

    def message(self, msg, user, socket):
        # Publish the new (x,y) coordinates
        self.send(msg)

# ----------
# HTTP Views
# ----------

@login_required
def home(request, room_name=None, template_name='home.html'):
    context = {'session_key':request.session.session_key}

    return render_to_response(template_name, context,
            context_instance=RequestContext(request))

# List of active users
def users(request):

    users = ''
    for user in Sessions.iter_users():
        user_type, user_obj = user
        users += "(%s,%s)" % (user_type, user_obj.username)

    return HttpResponse(users,mimetype='text')

# ---------------
# Socket Handlers
# ---------------

Room = Dragger(Sessions)

Websocket = WebsocketHandler(pool=Sessions,
                             models=CapsuleModels)
Websocket.app_fixture = app

Websocket.on_connect    = Room.subscribe
Websocket.on_disconnect = Room.unsubscribe
Websocket.on_message    = Room.message

# Hook that is passed to urls.py to handle socketio events
socketio = Websocket.make_handle()
