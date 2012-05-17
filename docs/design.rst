Design decisions
================

Compared to "giants"
--------------------

There have been several "giants" in web framework world.  While Plastic inherits
most of good things from these frameworks, it's also made some key differences
from them.


Compared to Django_
'''''''''''''''''''

Explicit application instance
   Plastic applications have to be a subclass of :class:`~plastic.app.BaseApp`
   and can these make multiple instances of them.  This means each application
   instance's contexts and states are totally isolated from each other even in
   the same process.  It makes applications easy to test.

No monolithic configuration
   Because of *explicit application instance*, each application instance has
   its own different configuration.  So applications can be isolated from
   the environment.  For example, you can make each configuration file for
   development, testing and production environments, and load the suitable
   configuration.

.. _Django: https://www.djangoproject.com/


Compared to Flask_
''''''''''''''''''

Factory by default
   Flask suggests `application factory pattern`__ for larger applications,
   however it's not by default. ::

       app = Flask(__name__)

       @app.route('/')
       def home():
           return 'hello'

       if __name__ == '__main__':
           app.config['FOO'] = 'bar'
           my_superfast_wsgi_server(app)

   The basic usage of Plastic :class:`~plastic.app.BaseApp` is subclassing.
   Routings and registering some hooks are done before application factory
   gets instantiated, and when it's instantiated configuration are applied
   to each instance. ::

       App = BaseApp.clone()

       @App.route('/')
       def home():
           return 'hello'

       if __name__ == '__main__':
           app = App(config={'FOO': 'bar'})
           my_superfast_wsgi_server(app)

   You'll get factories in Plastic by default.

   __ http://flask.pocoo.org/docs/patterns/appfactories/

No context locals
   An interesting feature of Flask is the `context locals`__.  According to
   its design document, Flask chose context locals instead of explicit argument
   passing to make it quick and easy to write a traditional web application.

   Technically it's similar to PHP's superglobals__ except PHP's contexts
   are completely isolated from each other while Flask's context isolation
   sometimes gets broken.

   If Python had `dynamic scoping`__ like Common Lisp or Perl, context locals
   don't get so broken.  Context locals are user-land implementation of
   dynamic scoping in programming languages that have no dynamic scoping.
   It's somewhat like magic, and magic isn't suitable for Python.  :-(

   Like Django and unlike Flask, Plastic takes the request argument as
   the first parameter for every view function.  Everything is explicit.
   No magic.

   If you look for :data:`flask.g`, use :attr:`Request.context
   <plastic.message.Request.context>` attribute which is kept during each
   request context.  :data:`flask.current_app` becomes :attr:`Request.app
   <plastic.message.Request.app>`.

   __ http://flask.pocoo.org/docs/design/#thread-locals
   __ http://php.net/manual/en/language.variables.superglobals.php
   __ http://en.wikipedia.org/wiki/Dynamic_scoping

.. _Flask: http://flask.pocoo.org/

