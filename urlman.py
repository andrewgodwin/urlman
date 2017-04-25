import string

try:
    from urlparse import urlunparse
except ImportError:  # pragma: no cover
    from urllib.parse import urlunparse

__version__ = '1.1.0'


def with_metaclass(meta, *bases):
    """
    Create a base class with a metaclass.

    For Python 2.x and 3.x compatibility.
    """
    # This requires a bit of explanation: the basic idea is to make a dummy
    # metaclass for one level of class instantiation that replaces itself with
    # the actual metaclass.
    class metaclass(meta):

        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)
    return type.__new__(metaclass, 'temporary_class', (), {})


class UrlsMetaclass(type):
    """
    Metaclass which makes attribute access instantiate the class with
    the instance.
    """
    def __new__(self, name, bases, attrs):
        # Collect patterns off of the attrs
        attrs["urls"] = {}
        for name, item in list(attrs.items()):
            if (name not in ["urls", "get_url", "get_example_url"] and
                    not name.startswith("__")):
                attrs["urls"][name] = item
                del attrs[name]
        # Initialise
        return type.__new__(self, name, bases, attrs)

    def __get__(self, instance, klass):
        return self(klass, instance)


class Urls(with_metaclass(UrlsMetaclass)):
    """
    Special object which lets you specify URL strings for objects.

    Declare urls as string attributes on the object in _python 3_ string
    format. If you need to you can also specify a handler function for a url.
    """
    def __init__(self, klass, instance):
        self.klass = klass
        self.instance = instance
        self.context = {"self": self.instance}
        self.context.update(self.urls)

    def __getattr__(self, attr):
        return self.get_url(attr)

    def get_url(self, attr):
        # Get the URL value
        try:
            url = self.urls[attr]
        except KeyError:
            raise ValueError("No URL called %r on %r" %
                             (attr, self.instance.__class__.__name__))
        else:
            if callable(url):
                url = url(self.instance)
            value = UrlFormatter(self).vformat(url, [], {})
        return UrlString(value)

    def get_example_url(self, attr):
        # Get the URL value
        try:
            url = self.urls[attr]
        except KeyError:
            raise ValueError("No URL called %r" % attr)
        else:
            if callable(url):
                url = url(self.instance)
            value = UrlFormatter(self, example=True).vformat(url, [], {})
        return value


class UrlString(str):
    """
    Special string subclass for URLs (for future with/without host modes)
    """
    def full(self, scheme='http', hostname='localhost', port='', params='',
             query='', fragment=''):
        netloc = hostname
        if port:
            netloc = '%s:%s' % (netloc, port)
        return urlunparse((scheme, netloc, self, params, query, fragment))


class UrlFormatter(string.Formatter):
    """
    Special string formatter that calls methods.
    """
    def __init__(self, urls, example=False):
        self.example = example
        self.urls = urls

    def get_value(self, key, args, kwargs):
        # First, try looking up the key in our own URLs
        try:
            if self.example:
                value = self.urls.get_example_url(key)
            else:
                value = self.urls.get_url(key)
        except ValueError:
            pass
        else:
            return value
        # Now, fall back to looking in the context (just self)
        if key == 'self':
            if self.example:
                return PrintMe('self')
            else:
                return self.urls.instance
        # Uh oh.
        raise KeyError("No other URL called %r for use in URL format" % key)

    def format_field(self, value, format_spec):
        if callable(value):
            value = value()
        return string.Formatter.format_field(self, value, format_spec)


class PrintMe(object):
    """Object which prints itself, essentially."""

    def __init__(self, obj):
        self.obj = obj

    def __getattr__(self, attr):
        return PrintMe(self.obj + '.' + attr)

    def __str__(self):
        return '{%s}' % self.obj
