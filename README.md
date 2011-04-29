Cortex is a Django extension designed to (hopefully) make
realtime Django painless.

The goal is to establish a one-to-one correspondence between
Backbone.js models and Django models and allow changes to be
synced between client and server in realtime.

Everything is a work in progress at the moment.

Directions:
===========

Build your virtualenv:

    $ cd zeromq-chat
    $ virtualenv --no-site-packages env
    $ source env/bin/activate

Install neccesary packages:

    $ pip install -r requirements.txt 

Run:
    
    $ python run.py

Point your browser to localhost:8080

Credits:
========

Capsule

HenrikJoreteg
https://github.com/andyet/Capsule

backbone.js, underscore.js

Jeremy Ashkenas
https://github.com/jashkenas

gevent-socketio

Jeffrey Gellens
https://bitbucket.org/Jeffrey/gevent-socketio


And yes, the name is Firefly reference. Can't stop the signal.
