from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('category/<slug:slug>/', views.category_post, name='category_post'),
    path('tag/<slug:slug>/', views.tag_view, name='tag'),
  
]