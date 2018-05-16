from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'blog_post'
urlpatterns = [
    url(r'^$', views.BlogPostListView.as_view()),
    url(r'^create/$', login_required(
        views.BlogPostCreateView.as_view(
            success_url='/blog/',
        ),
        login_url='/login/',
    )),
    url(r'^update/(?P<pk>[^/]+)', login_required(
        views.BlogPostUpdateView.as_view(
            success_url='/blog/',
        ),
        login_url='/login/',
    )),
    url(r'(?P<pk>[^/]+)', views.BlogPostDetailView.as_view())
]
