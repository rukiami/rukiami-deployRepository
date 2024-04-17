from django.contrib.auth.forms import AuthenticationForm
from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class LoginForm(AuthenticationForm):
    """ログインフォーム"""
    username = forms.EmailField(label="メールアドレス", widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        email = self.cleaned_data['username']
        return User.objects.filter(email=email).first().username

# class LoginForm(AuthenticationForm):
#     """ログインフォーム"""
#     def __init__(self, *args, **kwargs):
#         super(LoginForm, self).__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs["class"] = "form-control"
#             for fieldname in ['email', 'password']:
#                 widget=forms.EmailInput(attrs={'class': 'form-control'})
            # widget =forms.EmailInput(attrs={'class': 'form-control'}) #
            #  email= forms.EmailField(label="メールアドレス", widget=forms.EmailInput(attrs={'class': 'form-control'}))

# class LoginForm(AuthenticationForm):
#     email = forms.EmailField(label="メールアドレス", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
#     def __init__(self, *args, **kwargs):
#         super(LoginForm, self).__init__(*args, **kwargs)
#         for fieldname in ['email', 'password']:
#             self.fields[fieldname].widget.attrs['class'] = 'form-control'

# class LoginForm(AuthenticationForm):
#     """ログインフォーム"""

#     def __init__(self, request=None, *args, **kwargs):
#         super().__init__(request=request, *args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'

# class LoginForm(AuthenticationForm):
#     email = forms.EmailField(label="メールアドレス", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
#     def __init__(self, *args, **kwargs):
#         super(LoginForm, self).__init__(*args, **kwargs)
#         for fieldname in ['email', 'password']:
#             self.fields[fieldname].widget.attrs['class'] = 'form-control'


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# class SignUpForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('username', 'password1', 'password2', )
        # 必要に応じて、'email', 'first_name', 'last_name' など他のフィールドを追加可能
class SignUpForm(UserCreationForm):
    email = forms.CharField(
        max_length=254, 
        help_text='必須。有効なメールアドレスを入力してください。',
        label='メールアドレス',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        help_text='大文字小文字数字を含む８文字以上であること。',
        label='パスワード'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        help_text='確認のため、再度パスワードを入力してください。',
        label='パスワード（確認用）'
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)
from django.contrib.auth.models import AbstractUser



class SearchForm(forms.Form):
    genre = forms.CharField(label='ジャンル', max_length=100, required=False)
    location = forms.CharField(label='場所', max_length=100, required=False)


from django import forms

class RestaurantSearchForm(forms.Form):
    genre = forms.CharField(required=False, label='ジャンル')
    location = forms.CharField(required=False, label='場所')
    date = forms.DateField(required=False, label='日付', widget=forms.TextInput(attrs={'type': 'date'}))

from .models import Restaurant
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class RestaurantForm(forms.ModelForm):
    GENRE_CHOICES = [
        ('和食', '和食'),
        ('洋食', '洋食'),
        ('中華', '中華'),
        ('韓国', '韓国'),
        ('イタリアン', 'イタリアン'),
        ('カフェ', 'カフェ'),
       
        # 他のジャンルをここに追加
    ]
    genre = forms.ChoiceField(choices=GENRE_CHOICES, required=True, label='ジャンル*')
    PRICE_RANGE_CHOICES = [
        ('0-999円', '～￥999'),
        ('1000-1999円', '￥1000～￥1999'),
        ('2000-2999円', '￥2000～￥2999'),
        ('3000-3999円', '￥3000～￥3999'),
        ('4000円', '￥4000～'),
]
    price_range = forms.ChoiceField(choices=PRICE_RANGE_CHOICES, required=True, label='価格帯*')
    phone_number = forms.CharField(required=False, label='電話番号 (任意)')
    location = forms.CharField(required=True, label='場所*')
    url = forms.URLField(required=True, label='ウェブサイトURL*')  
    google_maps = forms.URLField(required=True, label='GoogleマップURL*')
    name = forms.CharField(required=True, label='店舗名*')


    def clean_google_maps(self):
        google_maps_url = self.cleaned_data['google_maps']
        # 開発モードのときはバリデーションを実行しない
        # if settings.DEVELOPMENT_MODE:
        #     return google_maps_url
        # 本番モードのときはURLのバリデーションを実行
        if google_maps_url and not google_maps_url.startswith('https://www.google.com/maps'):
            raise ValidationError(_('無効なGoogleマップURLです。正しいURLを入力してください。'))
        return google_maps_url
    

  

    class Meta:
        model = Restaurant
        # fields = ['name', 'phone_number', 'location', 'genre', 'price_range', 'google_maps', 'photo', 'url']  
        fields = ['name', 'phone_number', 'location', 'genre', 'price_range', 'google_maps', 'url'] 
        labels = {
            'name': '店舗名',
            'phone_number': '電話番号', 
            'location': '場所',
            'genre': 'ジャンル',
            'price_range': '価格帯',
            'url': 'ウェブサイトURL',
            'google_maps': 'Googleマップ',
            # 'photo': '写真'
            
        }   
def __init__(self, *args, **kwargs):
    super(RestaurantForm, self).__init__(*args, **kwargs)
    self.fields['name'].help_text = '*は必須です'
    self.fields['google_maps_url'].widget.attrs.update({'class': 'form-control'})
    self.fields['website_url'].widget.attrs.update({'class': 'form-control'})
        # 他のフィールドに対しても必要に応じて同じ操作を行う


        
from .models import Photo
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']  

from django import forms


class ExampleForm(forms.Form):
    name = forms.CharField(max_length=100)
    photo = forms.ImageField()



