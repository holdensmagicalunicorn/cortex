Chatroom Example
================

This is a vanilla single channel chatroom. It uses the Django
user system for chat handles.

Directions:
===========

Using the virtualenv via ../../requirement.txt launch.

    $ python manage.py syncdb

Create your admin account. And run the server

    $ python run.py

Login at http://localhost:8080/users/login

Test the chat room at http://localhost:8080

Notes
=====

For a more scalable solution with ZeroMQ backend see:

    https://github.com/sdiehl/zeromq-chat
