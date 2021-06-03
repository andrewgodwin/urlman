try:
    from rest_framework.serializers import Field
except ImportError:  # pragma: no cover

    class Field:
        pass


class UrlManField(Field):
    """Serializer class for Django Restframework."""

    read_only = True
    write_only = False
    label = None
    source = "*"

    def __init__(self, urls, attribute="urls", full=True):
        self.urls = urls
        self.url_attribute = attribute
        self.full = full

    def to_representation(self, value):
        url_class = getattr(value, self.url_attribute)
        return {
            url: getattr(url_class, url).full()
            if self.full
            else getattr(url_class, url)
            for url in self.urls
        }
