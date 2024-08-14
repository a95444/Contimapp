from django.shortcuts import render, redirect, get_object_or_404

from article.models import Category, Article  # vai buscar o ficheiro models à pasta item
# Create your views here.

#from .forms import SignupForm

def detail(request, id):
    article= get_object_or_404(Article, id=id) #1º id: o da função, 2º id: o do url

    return render (request, 'article/detail.html', {
        'article': article
        })
