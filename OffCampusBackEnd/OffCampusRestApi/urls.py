from django.urls import path

from . import views

urlpatterns = [
    path('', views.getSearchListingsPage, name='index'),
    path('paginatedListings', views.getPaginatedListings, name='paginatedListings'),
    path('allListings', views.getAllListings, name='allListings'),
]