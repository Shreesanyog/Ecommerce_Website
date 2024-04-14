from django.contrib import admin
from django.urls import path, include
from store import views
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='store'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('login', views.handlelogin, name='handlelogin'),
    path('signup', views.handlesignup, name='handlesignup'),
    path('logout', views.handlelogout, name='handlelogout'), 
    path('cart/', views.cart_view, name='cart'),
    path('help', views.help, name='help'),
]
