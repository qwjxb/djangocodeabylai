from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy
# Create your views here.

context = {
    "posts" : Post.objects.all()
}

    

def home(request):
    return render(request, 'blog/home.html', context)

class PostListView (ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post

class PostDelete(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog-home')

class PostCreate(CreateView):
    model = Post
    fields = ['title', 'content']  
    template_name = 'blog/post_form.html'  
    success_url = reverse_lazy('blog-home')

    def form_valid(self, form):
        form.instance.author = self.request.user  # Установка текущего пользователя как автора
        return super().form_valid(form)
    

class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False   


        
