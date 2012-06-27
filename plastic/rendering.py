""":mod:`plastic.rendering` --- Content rendering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from plastic.message import Request


def render_template(request, path, values={}, **keywords):
    """Helper function that renders a template of the given ``path``
    with ``values`` (and ``keywords``).  It's a shortcut of
    :meth:`BaseApp.render_template() <plastic.app.BaseApp.render_template>`
    method.

    ::

        @App.route('/<int:user_id>')
        def user_profile(request, user_id):
            global users
            user = users[user_id]
            return render_template(request, 'user_profile.html',
                                   user_id=user_id, user=user)

    You have to pass the ``path`` *without specific suffix*.
    The last suffix will be used for determining what template
    engine to use.  For example, if there is :file:`user_profile.html.mako`
    file in the :attr:`template_path` and ``'mako'`` is associated to
    Mako template engine in :attr:`template_engines` mapping,
    the following code will find :file:`user_profile.html.mako`
    (not :file:`user_profile.html`) and render it using Mako::

        render_template(request, 'user_profile.html')

    In other words, you have to append a suffix to determine
    what template engine to use into filenames of templates.

    :param request: a request which make it to render
    :type request: :class:`~plastic.message.Request`
    :param path: a path to template files without specific suffix
    :type path: :class:`basestring`
    :param values: a dictionary of values to pass to template
    :type values: :class:`collections.Mapping`
    :param \*\*keywords: the same to ``values`` except these are passed
                         by keywords
    :returns: a rendered result
    :rtype: :class:`basestring`
    :raises plastic.exceptions.RenderError:
       when there are no matched template files

    .. seealso::

       Method :meth:`BaseApp.render_template() \
       <plastic.app.BaseApp.render_template>`
          Renders the response using registered :attr:`template_engines`.

    """
    if not isinstance(request, Request):
        raise TypeError('request must be an instance of plastic.message.'
                        'Request, not ' + repr(request))
    return request.app.render_template(request, path, values, **keywords)

