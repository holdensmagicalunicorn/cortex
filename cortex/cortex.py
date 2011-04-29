import sys, traceback
from django.conf import settings
from django.utils.importlib import import_module
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, load_backend
from django.http import HttpResponse

import logging
logger = logging.getLogger(__name__)


class SessionPool:

    def __init__(self):
        self._pool = {}
        self.active_clients = []

    def add(self, session):
        """
        Add a Socket.IO session to the pool.
        """
        if session.connected:
            self._pool[session.session_id] = session

    def remove(self, session):
        """
        Remove a Socket.IO session from the pool.
        """
        del self._pool[session.session_id]

    def remove_key(self, session_key):
        """
        Remove a Socket.IO session from the pool by key
        sessio key lookup.
        """
        del self._pool[session_key]

    def __iter__(self):
        """
        Iterate over all Sessions in the pool.
        """
        return iter(self._pool.values())

    def __contains__(self, session):
        """
        Check if a session exists in the pool.
        """
        return session.session_id in self._pool

    def user(self, session):
        """
        Return a touple containing the user account type (User,
        Anonymous, Guest) and a reference of the User object.
        Lookups accounts via the attribute `key` attached to each
        Session object upon connecting.
        """
        return manual_auth(session.key)

    def iter_users(self):
        """
        Iterate over all the User objects for each active
        session, includes Anonymous and Guest accounts.
        """
        return [self.user(session) for session in iter(self)]

    def flush(self, criterion=None):
        """
        Kill sessions filtered by criterion. If no criterion
        is given then kill all sessions
        """

        if criterion:
            for session in iter(self):
                if criterion(session):
                    session.kill()
        else:
            for session in iter(self):
                session.kill()

    @property
    def everyone(self):
        """
        Return a Channel with all users in the pool
        """
        return Everyone(self)

class Channel:
    """
    A subset of a pool with a common message passing schema.
    """

    def __init__(self,pool):
        self._pool = pool
        self._subscribers = []
        #self.messages = []

    def send(self, msg):
        for session in self._subscribers:
            session.put_client_msg(msg)
            #self.message.append(msg)

    def subscribers(self):
        return self._subscribers

    def on_subscribe(self, user):
        pass

    def on_unsubscribe(self, user):
        pass

class Everyone(Channel):
    """
    Channel with the entire pool of sessions. Messages are
    broadcast to all connected users.
    """

    def __init__(self,pool):
        self._pool = pool

    def send(self,msg):
        for subscriber in iter(self._pool):
            subscriber.put_client_msg(msg)

    def subscribers(self):
        return iter(self._pool)

# The initial `app` model created upon a `session` event call.
app_fixture = {
    'attributes': {
        'toggler': False,
    },
    'id': 1
}

class WebsocketHandler:

    def __init__(self, pool=None, models=None):
        self.pool = pool
        self.models = models

    def delegate(self, event, args, socket):
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

            inst = self.models[typ].objects.get(id=sid)

            for key, value in attrs.iteritems():
                setattr(inst,key,value)

            inst.save()

        elif event == 'set':

            changes = args['change']
            sid     = args['id']
            typ     = args['type']

            inst = self.models[typ].objects.get(id=sid)

            for key, value in changes.iteritems():
                setattr(inst,key,value)

            inst.save()


    def make_handle(self):

        def handler(request):
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
                            self.pool.add(session)

                        self.delegate(msg['event'], msg, socketio)
                    else:
                        if not socketio.connected():
                            logger.info('SOCKET DISCONNETED: %s' % socketio.session.session_id)
                            self.pool.remove(socketio.session)
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

        return handler

def manual_auth(session_key):
    """
    Manually lookup user accounts by corresponding their session
    keys.
    """

    engine = import_module(settings.SESSION_ENGINE)
    session = engine.SessionStore(session_key)

    try:
        user_id = session[SESSION_KEY]
        backend_path = session[BACKEND_SESSION_KEY]
        backend = load_backend(backend_path)
        user = backend.get_user(user_id) or AnonymousUser()
    except KeyError:
        user = AnonymousUser()
        return ("Anonymous",user)

    if user.is_authenticated():
        return ("User",user)
    else:
        return ("Guest",user)
