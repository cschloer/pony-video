from django.urls import path

from . import views

urlpatterns = [
     # ex: /video/
     path('', views.IndexView.as_view(), name='index'),
     # ex: /video/5/
     path('<int:video_id>', views.detail, name='detail'),
]
