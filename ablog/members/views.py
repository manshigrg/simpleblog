from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic import DetailView, CreateView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import SignUpForm, EditProfileForm, ProfilePageForm, ProfileEditForm
from theblog.models import Profile
from theblog.views import CatMenuMixin
#from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.decorators import login_required
#from .forms import EditProfileForm
from django.contrib import messages
#from .forms import RegisterUserForm

class CreateProfilePageView(CatMenuMixin, CreateView):
	model = Profile
	form_class = ProfilePageForm
	template_name = 'registration/create_user_profile_page.html'
	#fields = '__all__'

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)


class EditProfilePageView(CatMenuMixin, generic.UpdateView):
	model = Profile
	form_class = ProfileEditForm
	template_name = 'registration/edit_profile_page.html'

	success_url = reverse_lazy('home')

class ShowProfilePageView(CatMenuMixin, DetailView):
	model = Profile
	template_name = 'registration/user_profile.html'

	def get_context_data(self, *args, **kwargs):
		users = Profile.objects.all()
		context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)

		page_user = get_object_or_404(Profile, id=self.kwargs['pk'])

		context["page_user"] = page_user
		return context


class UserRegisterView(generic.CreateView):
	form_class = SignUpForm
	template_name = 'registration/register.html'
	success_url = reverse_lazy('login')

	def form_valid(self, form):
		response = super().form_valid(form)
		messages.success(self.request, 'Registration successful...')
		return response


class UserEditView(CatMenuMixin, generic.UpdateView):
	form_class = EditProfileForm
	template_name = 'registration/edit_profile.html'
	success_url = reverse_lazy('home')

	def get_object(self):
		return self.request.user

class PasswordsChangeView(PasswordChangeView):
	form_class = PasswordChangeForm
	success_url = reverse_lazy('home')




