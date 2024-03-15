from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from theblog.models import Profile

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic', 'website_url', 'facebook_url', 'twitter_url', 'instagram_url', 'pinterest_url']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'website_url': forms.URLInput(attrs={'class': 'form-control'}),
            'facebook_url': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter_url': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram_url': forms.URLInput(attrs={'class': 'form-control'}),
            'pinterest_url': forms.URLInput(attrs={'class': 'form-control'}),
        }
        
class ProfilePageForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('bio', 'profile_pic', 'website_url', 'facebook_url', 'twitter_url', 'instagram_url', 'pinterest_url')
		widgets = {
		'bio': forms.Textarea(attrs={'class':'form-control'}),
		'profile_pic': forms.ClearableFileInput(attrs={'class':'form-control'}),
		'website_url': forms.TextInput(attrs={'class':'form-control'}),
		'facebook_url': forms.TextInput(attrs={'class':'form-control'}),
		'twitter_url': forms.TextInput(attrs={'class':'form-control'}),
		'instagram_url': forms.TextInput(attrs={'class':'form-control'}),
		'pinterest_url': forms.TextInput(attrs={'class':'form-control'}),
		}
        
class SignUpForm(UserCreationForm):
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['class'] = 'form-control'

class EditProfileForm(UserChangeForm):
	username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	#last_login = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	#is_superuser = forms.CharField(max_length=50, widget=forms.CheckboxInput(attrs={'class':'form-check'}))
	#is_staff = forms.CharField(max_length=50, widget=forms.CheckboxInput(attrs={'class':'form-check'}))
	#is_active = forms.CharField(max_length=50, widget=forms.CheckboxInput(attrs={'class':'form-check'}))
	#date_joined = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))


	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password')

	def __init__(self, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)

		#self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
		# Set the password field widget to HiddenInput
		self.fields['password'].widget = forms.HiddenInput()
		# Remove help text for the password field
		self.fields['password'].help_text = ''