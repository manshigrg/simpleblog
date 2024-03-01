from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Post, Category, Comment
from .forms import PostForm, EditForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages


# Create your views here.
#def home(request):
#	return render(request, 'home.html', {})

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

class HomeView(CatMenuMixin, ListView):
	model = Post
	template_name = 'home.html'
	cats = Category.objects.all()
	#ordering = ['-id']
	ordering = ['-post_date']

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

class AddCommentView(CatMenuMixin, CreateView):
	model = Comment 
	form_class = CommentForm
	template_name = 'add_comment.html'

	def form_valid(self, form):
		form.instance.post_id = self.kwargs['pk']
		return super().form_valid(form)

	def get_success_url(self):
		return reverse_lazy('article-detail', kwargs={'pk': self.kwargs['pk']})

class AddCategoryView(CatMenuMixin, CreateView):
	model = Category 
	template_name = 'add_category.html'
	fields = '__all__'
		
class UpdatePostView(CatMenuMixin, UpdateView):
	model = Post 
	form_class = EditForm
	template_name = 'update_post.html'
	#fields = ['title', 'title_tag', 'body']

	def get_success_url(self):
		return reverse_lazy('article-detail', kwargs={'pk': self.kwargs['pk']})

class DeletePostView(CatMenuMixin, DeleteView):
	model = Post 
	template_name = 'delete_post.html'
	success_url = reverse_lazy('home')