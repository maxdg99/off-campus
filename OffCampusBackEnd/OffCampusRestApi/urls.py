from django.urls import path

from . import views

urlpatterns = [
    path('', views.getSearchListingsPage, name='index'),
    path('paginatedListings', views.getPaginatedListings, name='paginatedListings'),
    path('allListings', views.getAllListings, name='allListings'),
    path('authUser', views.authenticate, name='authUser'),
    path('isSignedIn', views.isSignedIn, name='isSignedIn'),
    path('signOut', views.signOut, name='signOut')
]