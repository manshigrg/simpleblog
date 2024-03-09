from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import SignUpForm, EditProfileForm
#from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.decorators import login_required
#from .forms import EditProfileForm
#from django.contrib import messages
#from .forms import RegisterUserForm

class UserRegisterView(generic.CreateView):
	form_class = SignUpForm
	template_name = 'registration/register.html'
	success_url = reverse_lazy('login')


class UserEditView(generic.UpdateView):
	form_class = EditProfileForm
	template_name = 'registration/edit_profile.html'
	success_url = reverse_lazy('home')

	def get_object(self):
		return self.request.user

class PasswordsChangeView(PasswordChangeView):
	form_class = PasswordChangeForm
	success_url = reverse_lazy('home')




