from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    # ex: /video/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /video/5/
    path(
        '<int:video_id>',
        login_required(
            views.detail,
            login_url='/login/',
        ),
        name='detail',
    ),
    path(
        '<int:video_id>/create_note/',
        login_required(
            views.create_note,
            login_url='/login/',
        ),
        name='create_note',
    ),
]
