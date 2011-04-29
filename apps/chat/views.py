from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from chat.models import AppModel
from cortex import SessionPool, Channel, WebsocketHandler
Sessions = SessionPool();

# Establish a correspondance between the `.type` attribute
# attached to Backbone models and their counterpart in the
# Django ORM.
CapsuleModels = {
    'AppModel': AppModel,
}


class Chatroom(Channel):

    def on_subscribe(self, user):
        user_type, user_obj = user
        self.send({
            'add': 'Users',
            'connect': user_obj.username,
        })

# ----------
# HTTP Views
# ----------

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

Websocket = WebsocketHandler(pool=Sessions,
                             models=CapsuleModels)

socketio = Websocket.make_handle()
