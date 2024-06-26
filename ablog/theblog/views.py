from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Post, Category, Comment
from .forms import PostForm, EditForm, CommentForm, CategoryForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin


def admin_approval(request):
	template_name = 'admin_approval.html'

	if request.method == 'POST':
		if 'add_category' in request.POST:
			# Handle adding a new category
			cat_form = CategoryForm(request.POST)
			if cat_form.is_valid():
				cat_form.save()
				return redirect('admin_approval')
		elif 'update_category' in request.POST:
			# Handle updating an existing category
			category_id = request.POST.get('category_id')
			category = get_object_or_404(Category, pk=category_id)
			cat_form = CategoryForm(request.POST, instance=category)
			if cat_form.is_valid():
				cat_form.save()
				return redirect('admin_approval')
	else:
		cat_form = CategoryForm()

	user_count = User.objects.all().count()
	post_count = Post.objects.all().count()
	posts = Post.objects.all().order_by('-post_date')
	users = User.objects.all()
	categories = Category.objects.all()

	return render(request, template_name, {"user_count": user_count, "post_count": post_count, "users": users, "posts": posts, 'cat_form': cat_form, "categories": categories})

def delete_user(request, user_id):
	user = User.objects.get(pk=user_id)

	if request.user.is_superuser:
		user.delete()
		return redirect('admin_approval')  # Redirect to admin_approval page for superuser
	else:
		messages.error(request, "You are not authorized to delete user")
		return redirect('home')

def delete_category(request, category_id):
	category = Category.objects.get(pk=category_id)

	if request.user.is_superuser:
		category.delete()
		return redirect('admin_approval')  # Redirect to admin_approval page for superuser
	else:
		messages.error(request, "You are not authorized to delete this event")
		return redirect('home')

def update_category(request, category_id):
	template_name = 'update_category.html'

	category = Category.objects.get(pk=category_id)
	if request.user.is_superuser:
		form = CategoryForm(request.POST or None, instance=category)
	else:
		form = CategoryForm(request.POST or None, instance=category)
	
	if form.is_valid():
		form.save()
		return redirect('admin_approval')

	return render(request, template_name, {'category': category, 'form':form}) 

def LikeView(request, pk):
	post = get_object_or_404(Post, id=request.POST.get('post_id'))
	liked = False
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		liked = False
	else:
		post.likes.add(request.user)
		liked = True

	return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))

class CatMenuMixin(View):
	def get_context_data(self, *args, **kwargs):
		cat_menu = Category.objects.all()
		context = super().get_context_data(*args, **kwargs)
		context["cat_menu"] = cat_menu
		return context

class SearchBlogsView(CatMenuMixin, View):
	template_name = 'search_blogs.html'

	def get(self, request):
		return render(request, self.template_name, {'cat_menu': Category.objects.all()})

	def post(self, request):
		searched = request.POST.get('searched')
		posts = Post.objects.filter(title__contains=searched)
		context = {'searched': searched, 'posts': posts, 'cat_menu': Category.objects.all()}
		return render(request, self.template_name, context) 

'''class HomeView(CatMenuMixin, ListView):
	model = Post
	template_name = 'home.html'
	cats = Category.objects.all()
	#ordering = ['-id']
	ordering = ['-post_date']

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_superuser:
			return admin_approval(request)
		else:
			return super().dispatch(request, *args, **kwargs)
'''
class HomeView(CatMenuMixin, ListView):
	model = Post
	template_name = 'home.html'
	ordering = ['-post_date']
	paginate_by = 5  # Number of posts per page

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_superuser:
			return admin_approval(request)
		else:
			return super().dispatch(request, *args, **kwargs)

def CategoryListView(request):
	cat_menu_list = Category.objects.all()
	return render(request, 'category_list.html', {'cat_menu_list': cat_menu_list})

class CategoryView(ListView):
	model = Post
	template_name = 'categories.html'
	context_object_name = 'category_posts'

	def get_queryset(self):
		category_name = self.kwargs['cats']
		category = get_object_or_404(Category, name=category_name)
		return Post.objects.filter(category=category)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		category_name = self.kwargs['cats']
		context['cats'] = category_name.title()
		context["cat_menu"] = Category.objects.all()
		return context


class ArticleDetailView(CatMenuMixin, DetailView):
	model = Post
	template_name = 'article_details.html'

	def get_context_data(self, *args, **kwargs):
		cat_menu = Category.objects.all()
		context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)

		stuff = get_object_or_404(Post, id=self.kwargs['pk'])
		total_likes = stuff.total_likes()

		liked = False
		if stuff.likes.filter(id=self.request.user.id).exists():
			liked = True

		# Get comments ordered by date in descending order (most recent first)
		comments = stuff.comments.order_by('-date_added')

		context["cat_menu"] = cat_menu
		context["total_likes"] = total_likes
		context["liked"] = liked

		comment_form = CommentForm()
		context["comment_form"] = comment_form

		return context

class AddPostView(CatMenuMixin, CreateView):
	model = Post 
	form_class = PostForm
	template_name = 'add_post.html'
	#fields = '__all__'

	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		# Dynamically update the choices for the 'category' field
		form.fields['category'].widget.choices = Category.objects.values_list('name', 'name')
		return form

	def form_valid(self, form):
		# Handle form submission and save the data
		# ...
		return super().form_valid(form)

class UpdatePostView(CatMenuMixin, UpdateView):
	model = Post 
	form_class = EditForm
	template_name = 'update_post.html'
	#fields = ['title', 'title_tag', 'body']

	def get_success_url(self):
		return reverse_lazy('article-detail', kwargs={'pk': self.kwargs['pk']})

class AddCommentView(CatMenuMixin, CreateView):
	model = Comment 
	form_class = CommentForm
	template_name = 'add_comment.html'

	def form_valid(self, form):
		form.instance.post_id = self.kwargs['pk']
		messages.success(self.request, "Posting Comment") 
		return super().form_valid(form)

	def get_success_url(self):
		return reverse_lazy('article-detail', kwargs={'pk': self.kwargs['pk']})

def delete_comment(request, comment_id):
	comment = get_object_or_404(Comment, pk=comment_id)

	if request.user.username == comment.name:  # Check if the current user is the author of the post
		comment.delete()
		messages.success(request, "Comment deleted successfully")
	else:
		messages.error(request, "You are not authorized to delete this comment")

	# Redirect to the article detail page after deleting the comment
	return HttpResponseRedirect(reverse('article-detail', args=[str(comment.post.pk)]))

class AddCategoryView(CatMenuMixin, CreateView):
	model = Category 
	template_name = 'add_category.html'
	fields = '__all__'
	
class DeletePostView(CatMenuMixin, DeleteView):
	model = Post 
	template_name = 'delete_post.html'
	success_url = reverse_lazy('home')

def delete_post(request, post_id):
	post = Post.objects.get(pk=post_id)

	if request.user.is_superuser:
		post.delete()
		return redirect('admin_approval')  # Redirect to admin_approval page for superuser
	else:
		messages.error(request, "You are not authorized to delete this event")
		return redirect('home')
