from django.db import models
from django.utils import timezone
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Restaurant(models.Model):
    name = models.CharField(max_length=100, verbose_name='店名')
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='電話番号')
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name='場所')
    genre = models.CharField(max_length=50, blank=True, null=True, verbose_name='ジャンル')
    category = models.CharField(max_length=50, default='未指定', verbose_name='カテゴリー')  # デフォルト値を '未指定' に設定
    price_range = models.CharField(max_length=50, blank=True, null=True, verbose_name='価格帯')
    google_maps = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='restaurant_photos/', blank=True, null=True)
    # photo = models.ImageField(upload_to='restaurant_photos/')
    url = models.URLField(max_length=200, blank=True, null=True)
    # created_at = models.DateTimeField(default=timezone.now)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    pass

    
class Photo(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='restaurant_photos/')
    
    
    def __str__(self):
        return f"Photo of {self.restaurant.name}"        
        # return f"{self.restaurant.name} - {self.caption[:20]}"       


# シグナルを使用してレストランが保存されたときに写真を追加
@receiver(post_save, sender=Restaurant)
def create_default_photo(sender, instance, created, **kwargs):
    if created:
        Photo.objects.create(restaurant=instance)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('メールアドレスは必須です')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField('メールアドレス', unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    






