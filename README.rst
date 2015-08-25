urlman
------

A nicer way to do URLs for Django models.

Replaces things like get_absolute_url with a .urls attribute that
can reference other URLs and build sensible trees of things, and can
then be accessed using instance.urls.name.

Example::
    
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
`get_absolute_url`, and have a function like this on your model::

    def get_absolute_url(self):
        return self.urls.view
