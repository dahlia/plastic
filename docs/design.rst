Design decisions
================

Compared to "giants"
--------------------

There have been several "giants" in web framework world.  While Plastic inherited
from those frameworks, there are key differences between Plastic and those
frameworks.


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

Persistence agnostic
   The one of main features Django provides is ORM.  However, persistent
   objects can vary in production.  You may want to use SQLAlchemy_
   which is more powerful than Django ORM.  There are some enthusiasts of
   ZODB_ as well.  It's the age of NoSQL.  You may want to use Redis_
   through Sider_ or MongoDB_ using MongoAlchemy_.  Moreover, some applications
   don't have persist model objects *at all*.  Some applications are more
   about *computations* than *data*.

   Plastic is persistence agnostic and you can freely choose what you want to
   use for persistence.

Routing by decorators
   Django's URL router requires the table to be assembled in :file:`urls.py`::

       from django.conf.urls.defaults import patterns, url

       urlpatterns = patterns('',
           url(r'^$', 'myapp.home'),
           url(r'^people$', 'myapp.people'),
           url(r'^people/(?P<person_id>\d+)$', 'myapp.person')
       )

   Plastic uses decorators to route URL patterns to view functions::

       @App.route('/')
       def home(request):
           return '...'

       @App.route('/people')
       def people(request):
           return '...'

       @App.route('/people/<int:person_id>')
       def person(request, person_id):
           return '...'

   You do not need switch between two or more files (:file:`urls.py` and
   :file:`views.py`) to map URL patterns to view functions.

   Moreover, Plastic uses Werkzeug's routing system, so you have not to use
   regular expressions that are hard to read and not so suitable for URL
   patterns to route and can use Werkzeug's small URL pattern language
   that are easy to extend instead.  (Compare ``r'^people/(?P<person_id>\d+)$'``
   to ``'/people/<int:person_id>'`` in the above examples. :-)

.. _Django: https://www.djangoproject.com/
.. _SQLAlchemy: http://www.sqlalchemy.org/
.. _ZODB: http://www.zodb.org/
.. _Redis: http://redis.io/
.. _Sider: http://sider.dahlia.kr/
.. _MongoDB: http://www.mongodb.org/
.. _MongoAlchemy: http://www.mongoalchemy.org/


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

