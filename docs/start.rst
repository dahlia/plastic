Getting started
===============

Hello world
-----------

The following small code shows you how to print "hello world" using Plastic
web framework::

    from plastic.app import BaseApp

    App = BaseApp.clone()

    @App.route('/')
    def hello(request):
        return 'Hello, world!'

    if __name__ == '__main__':
        App().run()

Save the script (say it's :file:`hello.py`) and execute it:

.. sourcecode:: console

   $ python hello.py
    * Running on http://127.0.0.1:5555/
    * Restarting with reloader

Then open http://127.0.0.1:5555/ in your favorite web browser.  The page
says you "Hello, world!":

.. image:: _images/hello_world.png
   :alt: Hello world


How it was going on?
--------------------

In the above example, we created our application class named :class:`App`::

    App = BaseApp.clone()

Yes, it's a class and also a subtype of :class:`plastic.app.BaseApp`.
It can do several things e.g. routing, service.  Indeed it's a shorthand
of the following "ordinary" inheritance code::

    class App(BaseApp):
        pass

And then we defined a web page named :func:`hello()`::

    @App.route('/')
    def hello(request):
        return 'Hello, world!'

We call these functions *view functions* (as like in Django or Flask).
View functions can be routed using :meth:`BaseApp.route()
<plastic.app.BaseApp.route>` decorator, which is a convenient form of
:meth:`BaseApp.add_rule() <plastic.app.BaseApp.add_rule>` method::

    from werkzerug.routing import Rule

    def hello(request):
        return 'Hello, world'
    App.add_rule(Rule('/'), hello)

A view function has to take an argument at least, for getting a request.
In a request object there are many information about a request e.g.
HTTP method, HTTP headers, WSGI environment values.

It has to return a response.  If it's simply a string, it will be a content
of a response that :mailheader:`Content-Type` is :mimetype:`text/plain`.
It also can return an instance of :class:`plastic.message.Response`.

Lastly, the following line makes an app to be served::

    if __name__ == '__main__':
        App().run()

The first :keyword:`if` statement is a common idiom of Python to determine
whether the file is directly executed by :program:`python` as a script or
imported by other module or script as a module.  If it's imported by
others as :mod:`hello` module, the code in the :keyword:`if` statement
will be ignored.  If it's exeucted by :program:`python` as a script
(e.g. ``python hello.py``), the code below will be also executed.

The :meth:`~plastic.app.BaseApp.run()` method serves the app, so the above
two lines mean: "run the web server if the file isn't imported by others but
executed as a script."  It's not a class method but an instance method,
so it should be instantiated first: ``App()``.
