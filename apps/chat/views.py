import sys, traceback
from django.conf import settings

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

import logging
logger = logging.getLogger(__name__)

from chat.models import AppModel
from cortex import SessionPool, Channel
Sessions = SessionPool();

# Establish a correspondance between the `.type` attribute
# attached to Backbone models and their counterpart in the
# Django ORM.
CapsuleModels = {
    'AppModel': AppModel
}

# The initial `app` model created upon a `session` event call.
app_fixture = {
    'attributes': {
        'toggler': False,
    },
    'id': 1
}

Chatroom = Channel(SessionPool)

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

def handle_event(event, args, socket):
    """
    Process realtime events based on the `event` attribute
    passed.
    """

    if event == 'session':
        # Authorization key
        # (identical to request.session.session_key)
        key = args['cookie']

        socket.send({
          'event': 'initial',
          'app': app_fixture
        });

    elif event == 'sync':

        model = args['model']
        attrs = model['attrs']
        sid   = model['id']
        cid   = model['cid']
        typ   = args['type']

        inst = CapsuleModels[typ].objects.get(id=sid)

        for key, value in attrs.iteritems():
            setattr(inst,key,value)

        inst.save()

    elif event == 'set':

        changes = args['change']
        sid     = args['id']
        typ     = args['type']

        inst = CapsuleModels[typ].objects.get(id=sid)

        for key, value in changes.iteritems():
            setattr(inst,key,value)

        inst.save()

@login_required
def socketio(request):
    socketio = request.environ['socketio']

    while True:
        message = socketio.recv()

        try:
            logger.info('SOCKET CONNECTED: %s' % socketio.session.session_id)
            if len(message) == 1:
                # JSON decoded version of the message
                msg = message[0]
                session = socketio.session

                # If this session is an initial connect then add
                # to the SessionPool instance
                if session.is_new():
                    # Add a key attribute to each new
                    # gevent.socketio.Session object
                    key = request.session.session_key
                    session.key = key
                    Sessions.add(session)

                handle_event(msg['event'], msg, socketio)
            else:
                if not socketio.connected():
                    logger.info('SOCKET DISCONNETED: %s' % socketio.session.session_id)
                    Sessions.remove(socketio.session)
                elif message:
                    # Something strange was set
                    logger.error('Unknown socket message: %s' % message)
                    print message

        except Exception:
            if settings.DEBUG:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback,
                                              limit=2, file=sys.stdout)
            else:
                print 'Error occured while processing Socket.IO event'

    return HttpResponse()
