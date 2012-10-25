Plastic
=======

.. image:: https://secure.travis-ci.org/dahlia/plastic.png?branch=master
   :alt: Build Status
   :target: http://travis-ci.org/dahlia/plastic

Plastic is a Python web framework built on top of Werkzeug_.

.. code-block:: python

   from plastic.app import BaseApp

   App = BaseApp.clone()

   @App.route('/')
   def hello(request):
       return 'Hello, world!'

   if __name__ == '__main__':
       app = App()
       app.run()

Run:

.. code-block:: console

   $ python hello.py
    * Running on http://127.0.0.1:5555/
    * Restarting with reloader

.. _Werkzeug: http://werkzeug.pocoo.org/
