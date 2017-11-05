urlman
------

.. image:: https://travis-ci.org/andrewgodwin/urlman.svg?branch=master
   :target: https://travis-ci.org/andrewgodwin/urlman
   :alt: Test Status

.. image:: https://codecov.io/gh/andrewgodwin/urlman/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/andrewgodwin/urlman
   :alt: Test Coverage Status

A nicer way to do URLs for Django models.

Replaces things like ``get_absolute_url`` with a ``.urls`` attribute that
can reference other URLs and build sensible trees of things, and can
then be accessed using ``instance.urls.name``.

This is so you can have URLs on your model instances directly (rather than reversing
through the url lookup functions, which is not only slow but often hard to supply
arguments to). You can just throw ``{{ instance.urls.view }}`` into a template to get
a link.

It also lets you use Python string formatting syntax to place arguments into URLs from
the model instance itself or from other URLs in the same set.

Example:

.. code-block:: python

    import urlman

    model Group(models.Model):

    ...

        class urls(urlman.Urls):
            view = "/{self.slug}/"
            users = "{view}users/"
            admin = "{view}admin/"


    def my_view(request):
        group = ...
        return redirect(group.urls.view)

It's suggested that you use "view" as the equivalent name for
``get_absolute_url``, and have a function like this on your model:

.. code-block:: python

    def get_absolute_url(self):
        return self.urls.view

To build a full URL use the ``full`` method like this:

.. code-block:: python

    def my_view(request):
        group = ...
        return redirect(group.urls.admin.full(scheme='https'))

You can implement the `get_scheme(url)` and `get_hostname(url)` methods on your
`Url` class to change your default theme and hostname from the urlman defaults
of `'http'` and `'localhost'`, respectively.
