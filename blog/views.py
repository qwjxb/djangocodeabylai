from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

context = {
        'posts': [
            {
                'author': 'CoreyMS',
                'title': 'Nurel is not Hacker',
                'content': 'First post content',
                'date_posted': 'August 27, 2018'
            },
            {
                'author': 'Jane Doe',
                'title': 'Daniel is genius',
                'content': 'Second post content',
                'date_posted': 'August 28, 2018'
            }
        ]
    }

def home(request):
    return render(request, 'blog/home.html', context)
