from django.conf import settings
from django.utils.importlib import import_module
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, load_backend
from collections import deque

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

    def on_subscribe(self):
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
