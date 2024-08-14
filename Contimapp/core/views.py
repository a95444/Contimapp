from django.shortcuts import render, redirect
from article.models import Category, Article
from django.core.paginator import Paginator
from .forms import SignupForm
from django.contrib.auth import logout

def home(request):
    articles = Article.objects.all() 
    paginator = Paginator(articles, 3)
    page_number = request.GET.get('page')  # Obtém o número da página da query string
    page_obj = paginator.get_page(page_number)


    categories = Category.objects.all()
    return  render(request, 'core/home.html', {
        'categories': categories,
        'articles': articles, 
        'page_obj': page_obj,
    }) 


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST) #guarda toda a info do forms

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    } )

def login(request):
    if request.method == 'POST':
        form = SignupForm(request.POST) #guarda toda a info do forms

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    } )

def logout_view(request):
    logout(request)
    return redirect('/')