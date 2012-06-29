r""":mod:`hgist` --- Gist_ clone, but powered by Mercurial_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This tutorial will tell you how to make a typical web application
using Plastic.  What we will build here is Hgist, a pastebin web
application.  Its key feature is to manage each paste as Mercurial_
repository.  That is, users can pull and push any source code
pasted on Hgist using :program:`hg` command.

As it already comes into your mind, it's a clone of Gist_ except
Hgist is based on Mercurial while Gist is based on Git_.
Those two softwares are both a distributed version control system,
and share basically the same functionalities.

.. _Gist: https://gist.github.com/
.. _Mercurial: http://mercurial.selenic.com/
.. _Git: http://git-scm.org/


What we'll depend on
--------------------

Here we will use several great softwares to develop Hgist:

Mercurial_
   As mentioned above, Mercurial is a distributed version control system.
   It's written in Python, and so you can easily use this as library.
   In other words, you can :keyword:`import` :mod:`mercurial`.

Pygments_
   There are only three real syntax highlighters in the world: Vim, Emacs
   and Pygments.  Pygments is written in Python, and you can use it as
   library as well.

   FYI, GitHub_ and Gist also use Pygments for syntax highlighting.

Lastly, we will use Plastic as web framework.  Because this tutorial
is for that.  ;)

.. _Pygments: http://pygments.org/
.. _GitHub: https://github.com/

"""
