from django.urls import path

from . import views

urlpatterns = [
    path('', views.getSearchListingsPage, name='index'),
    path('paginatedListings', views.getPaginatedListings, name='paginatedListings'),
    path('allListings', views.getAllListings, name='allListings'),
    path('orderOptions', views.getOrderOptions, name='orderOptions'),
    path('areaOptions', views.getAreaOptions, name='areaOptions'),
    path('likeProperty', views.likeProperty, name='likeProperty'),
    path('unlikeProperty', views.unlikeProperty, name='unlikeProperty'),
    path('getLikedListings', views.getLikedListings, name='getLikedListings'),
    path('signIn', views.sign_in, name='signIn'),
    path('isSignedIn', views.isSignedIn, name='isSignedIn'),
    path('signOut', views.sign_out, name='signOut')
]
