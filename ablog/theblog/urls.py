from django.urls import path
from . import views
from .views import HomeView, ArticleDetailView, AddPostView, UpdatePostView, DeletePostView, AddCategoryView, CategoryView, CategoryListView, LikeView, AddCommentView, admin_approval

urlpatterns = [
    #path('', views.home, name="home"),
    path('', HomeView.as_view(), name="home"),
    path('article/<int:pk>', ArticleDetailView.as_view(), name="article-detail"),
    path('add_post/', AddPostView.as_view(), name="add_post"),
    path('add_category/', AddCategoryView.as_view(), name="add_category"),
    path('article/edit/<int:pk>', UpdatePostView.as_view(), name="update_post"),
    path('article/<int:pk>/remove', DeletePostView.as_view(), name="delete_post"),
    path('category/<str:cats>/', CategoryView.as_view(), name="category"),
    path('category-list/', CategoryListView, name="category-list"),
    path('like/<int:pk>', LikeView, name='like_post'),
    path('article/<int:pk>/comment/', AddCommentView.as_view(), name="add_comment"),
    path('admin_approval/', admin_approval, name='admin_approval'),
    path('delete_post/<post_id>', views.delete_post, name='delete-post'),
    path('delete_category/<category_id>/', views.delete_category, name='delete-category'),
    path('update_category/<category_id>', views.update_category, name='update-category'),
]
