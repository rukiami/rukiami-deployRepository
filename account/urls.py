
from django.urls import path
# from django.conf import settings
# from django.conf.urls.static import static
from .views import(
    TopView, HomeView, LoginView, LogoutView, SignUpView,
    restaurantListView, delete_restaurant,  RestaurantCreateView)
from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name="account"
urlpatterns = [
path("", views.TopView.as_view(), name="top"),
    path("home/", views.HomeView.as_view(), name="home"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),

    path('restaurant/', views.restaurantListView.as_view(), name='restaurant_list'),
    path('search/', views.search_view, name='search'), 

    path('restaurants/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('add_restaurant/', views.add_restaurant, name='add_restaurant'),
    path('restaurant/edit/<int:id>/', views.edit_restaurant, name='edit_restaurant'),
    path('restaurant/delete/<int:id>/', views.delete_restaurant, name='restaurant_delete'),
    path('restaurant/<int:restaurant_id>/photos/', views.restaurant_photos, name='restaurant_photos'),
    path('restaurant/<int:restaurant_id>/add_photo/', views.add_photo, name='add_photo'),
    path('restaurant/add/', RestaurantCreateView.as_view(), name='restaurant_add'),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
