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
    restaurant = get_object_or_404(Restaurant, id=id)
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

# def register_restaurant(request):
#     if request.method == 'POST':
#         form = RestaurantForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('account:restaurant_list')  # 成功した場合のリダイレクト先
#     else:
#         form = RestaurantForm()
#     return render(request, 'account/register_restaurant.html')  # 適切な

    # ビュー関数の内容...
    # return render(request, 'account/register.html')


# @csrf_exempt
# def add_event(request):
#     if request.method == 'POST':
#         # JSONの解析
#         data = json.loads(request.body)
#         # logger.info(f"Received data: {data}")  # ログに受け取ったデータを記録
        
#         # バリデーション
#         event_form = EventForm(data)
#         if not event_form.is_valid():
#             return JsonResponse({'status': 'error', 'errors': event_form.errors}, status=400)
        
#         # EventFormがModelFormの場合、フォームから直接モデルを保存
#         if hasattr(EventForm, 'save'):
#             new_event = event_form.save()  # EventFormがModelFormの場合
#         else:
#             # EventFormがModelFormでない場合、ここでEventモデルインスタンスを直接作成します。
       

        
    
    
#         # POST以外のメソッドでアクセスされた場合、エラーレスポンスを返す
#         # 
         



# @csrf_exempt
# def get_events(request):
#     if request.method == 'POST':
#         # JSONの解析
#         data = json.loads(request.body)

#         # 日付の変換
#         start_date = time.strftime("%Y-%m-%d", time.localtime(data['start_date'] / 1000))
#         end_date = time.strftime("%Y-%m-%d", time.localtime(data['end_date'] / 1000))

#         # 指定された期間内のイベントを取得
#         events = Event.objects.filter(start_date__gte=start_date, end_date__lte=end_date)

#         # イベントデータの準備
#         event_list = [{
#             'title': event.event_name,
#             'start': event.start_date,
#             'end': event.end_date,
#         } for event in events]

#         # JSONで返す
#         return JsonResponse(event_list, safe=False)
#     else:
#         # POST以外のメソッドでアクセスされた場合
#         return JsonResponse({'status': 'error'}, status=400)

# # イベント取得用のビューを追加していないため、必要に応じて追加してください。

