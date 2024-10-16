from django.contrib import admin
from django.urls import path
from .views import PostListView, PostDetailView, PostDelete, PostCreate, PostUpdate

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post-detail'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post-delete'),
    path('post/create/', PostCreate.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdate.as_view(), name='post-update')
]