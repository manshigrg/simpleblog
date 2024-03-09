from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import UserRegisterView
#from . import views

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name="register"),
    path('logout/', LogoutView.as_view(), name='logout'),

]
