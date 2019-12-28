from django.urls import path

from . import views

urlpatterns = [
    path('', views.getSearchListingsPage, name='index'),
    path('paginatedListings', views.getPaginatedListings, name='paginatedListings'),
    path('allListings', views.getAllListings, name='allListings'),
    path('toggleLikedProperty', views.toggleLikedProperty, name='toggleLikedProperty'),
    path('getLikedListings', views.getLikedListings, name='getLikedListings'),
    path('login', views.login, name='login'),
    path('isSignedIn', views.isSignedIn, name='isSignedIn'),
    path('logout', views.logout, name='logout')
]