from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .models import Post, Category
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Q
from functools import reduce
from operator import and_

from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login, authenticate
from allauth.account import views


#メイン機能（投稿、編集、削除、一覧、詳細、カテゴリー、検索）
class HomeView(View):
    def get(self, request):
        post_data = Post.objects.order_by('-id')
        return render(request, 'app/home.html', {'post_data': post_data})

#機能していない


class DetailView(View):
    def get(self, request, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/detail.html' ,{'post_data': post_data})

class CreateView(View, LoginRequiredMixin):
    def get(self, request):
        form = PostForm(request.POST or None)
        return render(request, 'app/create.html', {'form': form})
    
    def post(self, request):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post()
            post_data.author = request.user
            post_data.title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            category_data  = Category.objects.get(name=category)
            post_data.category = category_data
            post_data.content = form.cleaned_data['content']
            if request.FILES:
                post_data.image = request.FILES.get('image')
            post_data.save()
        return redirect('home')

class EditView(View, LoginRequiredMixin):
    def get(self, request, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        form = PostForm(request.POST or None, 
        initial = {
            'title': post_data.title,
            'category': post_data.category,
            'content': post_data.content,
            'image' : post_data.image
        })
        return render(request, 'app/create.html', {'form': form})

    def post(self, request, **kwargs):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post.objects.get(id=self.kwargs['pk'])
            post_data.title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            category_data = Category.objects.get(name=category)
            post_data.category = category_data
            post_data.content = form.cleaned_data['content']
            if request.FILES:
                post_data.image = request.FILES.get('image')
            post_data.save()
            return redirect('detail', self.kwargs['pk'])
        return render(request, 'app/create.html', {'form': form})

class DeleteView(View, LoginRequiredMixin):
    def get(self, request, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/delete.html', {'post_data': post_data})

    def post(self, request, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        post_data.delete()
        return redirect('home')

class CategoryView(View):
    def get(self, request, *args, **kwargs):
        category_data = Category.objects.get(name=self.kwargs['category'])
        post_data = Post.objects.order_by('-id').filter(category=category_data)
        return render(request, 'app/home.html', {'post_data': post_data})

class SearchView(View):
    def get(self, request):
        post_data = Post.objects.order_by('-id')
        keyword = request.GET.get('keyword')

        if keyword:
            exclusion_list = set(['', '　'])
            query_list = ''
            for word in keyword:
                if not word in exclusion_list:
                    query_list += word
            query = reduce(and_, [Q(title__contains=q) | Q(content__contains=q) for q in query_list])
            post_data = post_data.filter(query)

            return render(request, 'app/home.html', {'keyword': keyword, 'post_data': post_data}) 

#user機能（ログイン、ログアウト、サインアップ）
def LoginView(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        user_password = request.POST['password']
        user = authenticate(request, username=user_name, password=user_password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'app/login.html', {'error': 'usenameかpasswordが間違っています'})
    return render(request, 'app/login.html')

class LogoutView(views.LogoutView):
    template_name = 'app/logout.html'

    def post(self, *args ,**kwargs):
        if self.request.user.is_authenticated:
            self.logout()
        return redirect('/')

def SignupView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'app/signup.html', {'form': form})




    
