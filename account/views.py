# from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, ListView
from django.urls import reverse_lazy
from .forms import LoginForm, SignUpForm, SearchForm, RestaurantForm, PhotoForm# EventFormをインポート

from.models import Restaurant, Photo
from django.http import HttpResponse, JsonResponse

import json
import time  # 日付の変換に使用
from . import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST


# Your other views...
# 既存のビューは変更なしで残す

class TopView(TemplateView):
    template_name = "account/top.html"

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "account/home.html"

class LoginView(LoginView):
    """ログインページ"""
    form_class = forms.LoginForm
    template_name = "account/login.html"
    def get_success_url(self):
        # messages.info(self.request, "ログインしました")
        return super().get_success_url()


class LogoutView(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = "account/login.html"

class SignUpView(CreateView):
    """サインアップ"""
    form_class = SignUpForm
    success_url = reverse_lazy('account:login')
    template_name = 'account/signup.html'    

# class CalendarView(TemplateView):
#     template_name = 'account/calendar.html'  # calendar.html テンプレートを使用する

# def index(request):
#     """
#     カレンダー画面
#     """
#     return HttpResponse("Calendar")
    
def logout_view(request):
    logout(request)
    messages.info(request, "ログアウトされました")
    return redirect('account:login')  

class restaurantListView(ListView):
    model = Restaurant
    template_name = 'account/restaurant_list.html'  
    context_object_name = 'restaurants' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm()  # 検索フォームをコンテキストに追加
        return context
    def get_queryset(self):
        form = SearchForm(self.request.GET or None)
        queryset = super().get_queryset()  # デフォルトのクエリセットを取得
        if form.is_valid():
            genre = form.cleaned_data.get('genre')
            location = form.cleaned_data.get('location')
            # date = form.cleaned_data.get('date')  # dateがモデルにある場合にコメントアウトを外す

            if genre:
                queryset = queryset.filter(genre__icontains=genre)
            if location:
                queryset = queryset.filter(location__icontains=location)
            # if date:
            #     queryset = queryset.filter(date=date)  # モデルのフィールドに合わせてコメントアウトを外す
        return queryset
    


def search_view(request):
    query = request.GET.get('q', '')
    if query:
        results = Restaurant.objects.filter(name__icontains=query)  # 'name' は Shop モデルの属性
    else:
        results = []
    context = {
        'query': query,
        'results': results
    }
    # 検索機能の実装をここに書きます
    # この例では単純に search.html テンプレートをレンダリングします
    return render(request, 'account/search.html', context)

def home(request):
    
    form = SearchForm()
    return render(request, 'home.html', {'form': form})

# Other class-based views...

def restaurant_list(request):
    restaurants = Restaurant.objects.all()  # すべての店舗を取得
    return render(request, 'account/restaurant_list.html', {'restaurants': restaurants})
    # return render(request, 'restaurants/restaurant_list.html', {'restaurants': restaurants})

def restaurant_detail(request, id):
    restaurant = get_object_or_404(Restaurant, pk=id)
    return render(request, 'account/restaurant_detail.html', {'restaurant': restaurant})  

def add_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('account:restaurant_list')

            # return redirect('account:restaurant_list')  # 保存後にリダイレクトするページ
    else:
        form = RestaurantForm()
    return render(request, 'account/add_restaurant.html', {'form': form})

def edit_restaurant(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    if request.method == "POST":
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect('account:restaurant_detail', id=restaurant.id)
    else:
        form = RestaurantForm(instance=restaurant)
    return render(request, 'account/edit_restaurant.html', {'form': form, 'restaurant': restaurant})

def delete_restaurant(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    if request.method == "POST":
        restaurant.delete()
        # messages.info(request, "レストランが削除されました。")
        return redirect('account:restaurant_list')
    #     return redirect('account:restaurant_list')
    # return render(request, 'account/delete_confirm.html', {'restaurant': restaurant})

def restaurant_photos(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    photos = restaurant.photos.all()
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.restaurant = restaurant
            photo.save()
            return redirect('restaurant_photos', restaurant_id=restaurant_id)
    else:
        form = PhotoForm()
    return render(request, 'account/restaurant_photos.html', {'restaurant': restaurant, 'photos': photos, 'form': form})

def add_photo(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.restaurant = restaurant
            photo.save()
            return redirect('account:restaurant_photos', restaurant_id=restaurant.id)
    else:
        form = PhotoForm()
    return render(request, 'account/add_photo.html', {'form': form, 'restaurant': restaurant})


class RestaurantCreateView(CreateView):
    model = Restaurant
    form_class = RestaurantForm
    template_name = 'account/restaurant_form.html'  # お店登録用テンプレート
    success_url = reverse_lazy('account:restaurant_list') 

# def your_view(request):
#     if request.method == 'POST':
#         # フォームのデータを取得
#         form = add_restaurant(request.POST)
#         if form.is_valid():
#             # フォームのデータが有効な場合の処理
#             ...
#         else:
#             # フォームのデータにエラーがある場合
#             messages.error(request, 'フォームにエラーがあります。')
#             return redirect('some_view_name')
#     else:
#         form = RestaurantForm()

#     context = {'form': form}
#     return render(request, 'myapp/template.html', context)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # ログインに成功したら、ホーム画面などにリダイレクト
                return redirect('home')
            else:
                # ユーザー認証失敗のメッセージ
                messages.error(request, 'ユーザー名かパスワードが間違っています。')
        else:
            # フォームが無効な場合
            messages.error(request, 'エラーが発生しました。フォームを再確認してください。')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})