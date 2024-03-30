from django import forms
from .models import Post, Category, Comment

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = ['name']
		
		widgets = {
		'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add new category', 'size': '25'}),
		}
		
		labels = {
		'name': '',
		}


#choices = [('coding', 'coding'), ('sports', 'sports'), ('entertainment', 'entertainment')]
choices = Category.objects.all().values_list('name', 'name')
choice_list = []

for item in choices:
	choice_list.append(item)

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'title_tag', 'author', 'category', 'body', 'snippet')

		def __init__(self, *args, **kwargs):
			category_choices = kwargs.pop('category_choices', [])
			super().__init__(*args, **kwargs)

			# Update the choices for the 'category' field
			self.fields['category'].widget.choices = category_choices
		
		widgets = {
		'title': forms.TextInput(attrs={'class':'form-control'}),
		'title_tag': forms.TextInput(attrs={'class':'form-control', 'type':'hidden'}),
		'author': forms.TextInput(attrs={'class':'form-control', 'value':'', 'id':'username', 'type':'hidden'}),
		#'author': forms.Select(attrs={'class':'form-control'}),
		'category': forms.Select(choices=choice_list, attrs={'class':'form-control'}),
		'body': forms.Textarea(attrs={'class':'form-control'}),
		'snippet': forms.Textarea(attrs={'class':'form-control'}),
		}


class EditForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'title_tag', 'category','body', 'snippet')

		widgets = {
		'title': forms.TextInput(attrs={'class':'form-control'}),
		'title_tag': forms.TextInput(attrs={'class':'form-control', 'type':'hidden'}),
		#'author': forms.Select(attrs={'class':'form-control'}),
		'category': forms.Select(choices=choice_list, attrs={'class':'form-control'}),
		'body': forms.Textarea(attrs={'class':'form-control'}),
		'snippet': forms.Textarea(attrs={'class':'form-control'}),

		}

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('name', 'body')

		widgets = {
		'name': forms.TextInput(attrs={'class':'form-control', 'value':'', 'id':'username', 'type':'hidden'}),
		'body': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'What are your thoughts?'}),
		}

		labels = {
		'name': '',
		'body': '',
		}
