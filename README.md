Cortex is a Django extension designed to (hopefully) make
realtime Django painless.

The goal is to establish a one-to-one correspondence between
Backbone.js models and Django models and allow changes to be
synced between client and server in realtime.

Most of the ideas are inspired by Now.js ( http://nowjs.com ) but
translated into Pythonic API.

Directions:
===========

Build your virtualenv:

    $ cd cortex
    $ virtualenv --no-site-packages env
    $ source env/bin/activate

Install necessary packages:

    $ pip install -r requirements.txt 

To test one of the example apps follow the directions in 

    examples/drag/README
    examples/chat/README

Use
===

Use pip to Install the `requirements.txt` in your Django project's 
virtualenv then place the directory cortex in your Django project's 
path. Copy all javascript source files from `static/` to your static 
directory.  You can then `import cortex`.

Credits:
========

* Capsule - HenrikJoreteg ( https://github.com/andyet/Capsule )
* backbone, underscore - Jeremy Ashkenas ( https://github.com/jashkenas )
* gevent-socketio - Jeffrey Gelens ( https://bitbucket.org/Jeffrey/gevent-socketio )

Capsule is modified from the original, the server side code is
stripped.

And yes, the name is Firefly reference.
