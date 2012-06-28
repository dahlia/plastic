""":mod:`plastic.rendering` --- Content rendering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from werkzeug.exceptions import NotAcceptable

from .message import Request


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
    :param path: a path to template files without suffix
                 to determine template engine
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


def render(request, value, path, values={}, **keywords):
    """Renders the suitable response using content negotiation.
    It's aware of given ``request``'s :mailheader:`Accept` header.

    If there's no matched mimetype to ``request``'s :mailheader:`Accept`
    list, it raises :exc:`~werkzeug.exceptions.NotAcceptable` error.

    If chosen mimetype is associated to serializer (see
    :meth:`BaseApp.add_serializer() <plastic.app.BaseApp.add_serializer>`)
    it passes ``value`` to the serializer and rest of arguments are
    just ignored.

    If chosen mimetype is associated to suffix
    (see :meth:`BaseApp.associate_mimetypes()
    <plastic.app.BaseApp.associate_mimetypes>` method) it appends
    the suffix to the given template ``path`` and then calls
    :func:`render_template()` function with the same arguments
    except ``value``.

    :param request: a request which make it to render
    :type request: :class:`~plastic.message.Request`
    :param value: a value to serialize
    :param path: a path to template files without suffix
                 to determine content type and template engine
    :type path: :class:`basestring`
    :param values: a dictionary of values to pass to template
    :type values: :class:`collections.Mapping`
    :param \*\*keywords: the same to ``values`` except these are passed
                         by keywords
    :returns: a rendered result
    :rtype: :class:`basestring`
    :raises plastic.exceptions.RenderError:
       when there are no matched template files
    :raises werkzeug.exceptions.NotAcceptable:
       when there's no matched mimetype to ``request``'s
       :mailheader:`Accept` list

    """
    if not isinstance(request, Request):
        raise TypeError('request must be an instance of plastic.message.'
                        'Request, not ' + repr(request))
    rendering_mapping = request.app.mimetype_mapping
    mimetype = request.accept_mimetypes.best_match(rendering_mapping)
    if not mimetype:
        raise NotAcceptable()
    rendering_method = rendering_mapping[mimetype]
    if isinstance(rendering_method, basestring):
        template_path = '{0}.{1}'.format(path, rendering_method)
        return render_template(request, template_path, values, **keywords)
    elif callable(rendering_method):
        return rendering_method(request, value)
    raise TypeError('every value of rendering_mapping has to be callable '
                    'or a suffix string; but rendering_mapping[{0!r}] is '
                    '{1!r}'.format(mimetype, rendering_method))

