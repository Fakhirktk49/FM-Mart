from django.contrib import admin
from django.urls import path
from website.views import website,Home,about,loginview,register,forgot_pass,verify_email,activate_account,profile,cart,buy,change_password,edit_profile,delete_account,checkout
from django.views.generic import TemplateView,RedirectView
from django.contrib.auth.views import LogoutView
from django.contrib import messages

urlpatterns = [
    path('base/',website,name='website'),
    path('home/',Home.as_view(),name='home'),
    path('about/',about,name='about'),
    path('login/',loginview,name='login'),
    path('register/',register,name='register'),
    path('forgot_pass/',forgot_pass,name='forgot_pass'),
    path('verify_email/',verify_email,name='verif_email'),
    path('activation_email/',TemplateView.as_view(template_name='website/activation_email.html'),name='activation_email'),
    path('activate_account/<str:uid>/<str:token>/',activate_account,name='activate_account'),
    path('profile/',profile,name='profile'),
    path('cart/',cart,name='cart'),
    path('buy/<str:id>/',buy,name='buy'),
    path('logout/',LogoutView.as_view(),{'success':'You have been logedout.'},name='logout'),
    path('change_password/',change_password,name='change_password'),
    path('edit_profile/',edit_profile,name='edit_profile'),
    path('delete_account/',delete_account,name='delete_account'),
    path('checkout/',checkout,name='checkout')
]