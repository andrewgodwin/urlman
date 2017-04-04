import string


class UrlsMetaclass(type):
    """
    Metaclass which makes attribute access instantiate the class with the instance.
    """

    def __new__(self, name, bases, body):
        # Collect patterns off of the body
        body["urls"] = {}
        for name, item in list(body.items()):
            if name not in ["urls", "get_url", "get_example_url"] and not name.startswith("__"):
                body["urls"][name] = item
                del body[name]
        # Initialise
        return type.__new__(self, name, bases, body)

    def __get__(self, instance, klass):
        return self(klass, instance)


class Urls(object):
    """
    Special object which lets you specify URL strings for objects.

    Declare urls as string attributes on the object in _python 3_ string
    format. If you need to you can also specify a handler function for a url.
    """

    __metaclass__ = UrlsMetaclass

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
            raise ValueError("No url pattern called %s on %s" % (attr, self.instance.__class__.__name__))
        else:
            if callable(url):
                value = url(self.instance)
            else:
                value = UrlFormatter(self).vformat(url, [], {})
        return UrlString(value)

    def get_example_url(self, attr):
        # Get the URL value
        try:
            url = self.urls[attr]
        except KeyError:
            raise ValueError("No url pattern called %s" % attr)
        else:
            if callable(url):
                value = "??METHOD??"
            else:
                value = UrlFormatter(self, example=True).vformat(url, [], {})
        return value


class UrlString(str):
    """
    Special string subclass for URLs (for future with/without host modes)
    """


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
            # If it's a callable, call it with the outer instance as self
            if callable(value):
                value = value(self.urls.instance)
            return value
        # Now, fall back to looking in the context (just self)
        if key == "self":
            if self.example:
                return PrintMe("self")
            else:
                return self.urls.instance
        # Uh oh.
        raise ValueError("No other URL called %r for use in URL format" % key)

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
