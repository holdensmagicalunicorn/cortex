import simplejson as json
from django.db import models
from django.contrib import admin

from django.core import serializers

import django.dispatch
from django.db.models.signals import pre_save
from django.dispatch import receiver

#class Hub(object):
#    """
#    Hub a is namespace of variables and remote/local procedures
#    stored in memory. Completey persistent across the server and
#    the client.
#    """
#    server_func_calls = {}
#    client_func_calls = {}
#
#    def __init__(self):
#        self.func_calls = {
#            'heartbeat': self.heartbeat
#        }
#
#    def rpc(self, func, args):
#        """ Remote procedure call """
#        self.func_calls[func](args)
#
#    def lpc_exec(self, code):
#        """
#        Execute a string on all connected clients
#        """
#
#    def lpc(self, func, args):
#        """
#        Local procedure call
#        """
#
#        socketio.broadcast({
#            'event' : 'rpc' ,
#            'ns'    : ns    ,
#            'func'  : func  ,
#            'args'  : args  ,
#        })
#
#    def heartbeat(self, *args, **kwargs):
#        client = kwargs['client']
#        client.socket.send({
#            event: 'heartbeat',
#        })
#        return True


#class AsyncWorkPool(gevent.Pool):
#    pass
#
#class CallbackDict(dict):
#    callbackdict = {
#        'key': callback
#    }
#
#    def __setitem__(self, key, value):
#        if key in callbackdict:
#            self.callbackdict[key]()
#
#foo = CallbackDict({'a':3})
#f['a'].change = somerpc

#class AsyncWork(object):
#    """
#    Execute a task outside of the main event loop, relay the
#    response back to the client when done.
#    """
#    self.uuid = uuid.uuid4()
#    limit_per_user = 3
#    limit_per_worker = 1

#class Resource(object):
#    """
#    A wrapper for a Model which pushes and pulls changes to
#    clients. Provides a one-to-one correspondance to Backbone
#    models.
#    """
#
#    model = None
#    attrs = None
#    lastupdate = None
#
#    def on(self):
#        pass
#
#    def get(self):
#        pass
#
#    def toJSON(self):
#        pass
#
#    def id(self):
#        pass

#class Channel(object):
#
#    def __init__(self):
#        pass
#
#    def addUser(self):
#        pass
#
#    def removeUser(self):
#        pass
#
#    def stream(self):
#        '''
#        Namespace for all users in this channel
#        '''
#        pass
#
#    def onConnect(self):
#        pass
#
#    def onDisconnect(self):
#        pass

#class Everyone(object):
#
#    def __init__(self):
#        return [client for client in ClientPool.users()]
#
#    def __iter__(self):
#        pass

def lookup_socket_by_ip(ip_addr):
    pass

def lookup_socket_by_user(user):
    pass

def lookup_socket_by_session_id(session_id):
    #socketio.session.session_id
    pass

class Client(object):
    def __init__(self, user, socket):
        self.user = user
        self.socket = socket

# Provide callbacks on the Database (MongoDB?) and push them into
# Backbone models as requested.

#def updateClients():
#    for client in activeClients:
#        """send changes to clients that need them"""
#post_syncdb.connect(updateclients, sender=yourapp.models)

class CapsuleModel(models.Model):

    def xport(self):
        return {
            'id': self.id,
            'attrs': self.json_equivalent()
        }

    def json_equivalent(self):
        dictionary = {}
        for field in self._meta.get_all_field_names():
            if field != 'id':
                val = self.__getattribute__(field)
                if isinstance(val, str) or isinstance(val, int):
                    dictionary[field] = val
        return dictionary

    def mport(self,**args):
        for key, value in args.iteritems():
            self['key'] = value

        self.save()

class AppModel(CapsuleModel):
    toggler = models.BooleanField()

admin.site.register(AppModel)
