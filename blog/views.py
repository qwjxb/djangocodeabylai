from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
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

class PostListView(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = 'posts'
    ordering = ['-date_posted']  # Sorting by date posted
    paginate_by = 5  # Paginate by 5 posts per page

    def get_queryset(self):
        query = self.request.GET.get('q')  # Get the search query
        if query:
            return Post.objects.filter(title__icontains=query) | Post.objects.filter(content__icontains=query)
        else:
            return Post.objects.all().order_by('-date_posted')  # Return all posts, ordered by date

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Add the query to context for form re-population
        return context



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
    
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')  # Сортируем посты по дате создания

    # Настройка пагинации (показываем 1 постов на странице)
    paginator = Paginator(posts, 1)  # 1 постов на каждой странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'post_list.html', {'page_obj': page_obj})



        
