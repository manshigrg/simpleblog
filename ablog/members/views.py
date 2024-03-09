from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import SignUpForm
#from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.decorators import login_required
#from .forms import EditProfileForm
#from django.contrib import messages
#from .forms import RegisterUserForm

class UserRegisterView(generic.CreateView):
	form_class = SignUpForm
	template_name = 'registration/register.html'
	success_url = reverse_lazy('login')
