import pytest
import urlman


class Post(object):
    slug = 'hello-world'  # the object-specific attribute to refer to in the URL

    class urls(urlman.Urls):
        view = '/posts/{self.slug}/'
        authors = '{view}authors/'
        admin = '{authors}admin/'
        broken = '/{does_not_exist}/'
        recursion = '/{recursion}/'


@pytest.fixture
def post():
    return Post()


def test_urlstring_standalone():
    assert urlman.UrlString('/posts/').full(scheme='https', hostname='localhost') == 'https://localhost/posts/'


def test_basic(post):
    assert post.urls.view == '/posts/hello-world/'
    assert post.urls.authors == '/posts/hello-world/authors/'
    assert post.urls.admin == '/posts/hello-world/authors/admin/'


def test_get_example_url(post):
    assert post.urls.get_example_url('view') == '/posts/{self.slug}/'


def test_non_extistent_url(post):
    "If the URL does not exist raise a ValueError"
    with pytest.raises(ValueError):
        post.urls.non_existent


def test_broken_url(post):
    """
    If the format string used in an existing URL does not exist raise a
    KeyError
    """
    with pytest.raises(KeyError):
        post.urls.broken


def test_recursion_url(post):
    "Fail completely if a recursive format string was used"
    with pytest.raises(RuntimeError):
        post.urls.recursion


def test_full_default_url(post):
    assert post.urls.view.full() == 'http://localhost/posts/hello-world/'


def test_full_scheme_url(post):
    assert post.urls.view.full(scheme='https') == 'https://localhost/posts/hello-world/'


def test_full_hostname_url(post):
    assert post.urls.view.full(hostname='127.0.0.1') == 'http://127.0.0.1/posts/hello-world/'


def test_full_port_url(post):
    assert post.urls.view.full(port=8000) == 'http://localhost:8000/posts/hello-world/'


def test_full_params_url(post):
    assert post.urls.view.full(params='param=1') == 'http://localhost/posts/hello-world/;param=1'


def test_full_query_url(post):
    assert post.urls.view.full(query='query=1') == 'http://localhost/posts/hello-world/?query=1'


def test_full_fragement_url(post):
    assert post.urls.view.full(fragment='fragment') == 'http://localhost/posts/hello-world/#fragment'


class Blog(object):
    slug = 'blog'

    def atom(self):
        return self.urls.posts + 'atom/'

    class urls(urlman.Urls):

        view = '/{self.slug}/'

        def posts(self):
            assert isinstance(self, Blog)
            return '{view}posts/'

        def all(self):
            return '{posts}all/'

        def feed(self):
            return '{self.atom}'


def test_callable():
    blog = Blog()
    assert blog.urls.view == '/blog/'
    assert blog.urls.posts == '/blog/posts/'
    assert blog.urls.all == '/blog/posts/all/'
    assert blog.urls.feed == '/blog/posts/atom/'
    assert blog.urls.get_example_url('all') == '/{self.slug}/posts/all/'


def test_rest_framework_serializer(post):
    field = urlman.UrlManField(urls=['authors', 'admin'])
    relative_field = urlman.UrlManField(urls=['view'], full=False)

    assert field.to_representation(post) == {
        'authors': post.urls.authors.full(),
        'admin': post.urls.admin.full(),
    }
    assert relative_field.to_representation(post) == {
        'view': post.urls.view,
    }
