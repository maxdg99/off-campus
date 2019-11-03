from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('banana/', views.banana, name='banana'),
    path('query_json', views.query_json, name='query_json')
]