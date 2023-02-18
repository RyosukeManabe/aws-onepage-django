from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)

    is_admin = models.BooleanField(default=False)

    is_insta = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

SITE_IMAGE_CHOICES = (
    ('kind', '優しい'),
    ('warm', '暖かい'),
    ('lively','にぎやか'),
    ('calm','落ち着きのある'),
    ('japanese_style','和風'),
    ('deluxe','高級な'),
    ('others','その他'),
)
COLOR_CHOICES = (
    ('red','赤'),
    ('blue','青'),
    ('green','緑'),
    ('black','黒'),
    ('White','白'),
    ('pink','ピンク'),
    ('orange','オレンジ'),
    ('others','その他'),
)

class Hp_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    new = models.BooleanField(null=True,blank=True) #新規製作かどうか
    site_url = models.URLField(blank=True) #現サイトのURL
    company_name = models.CharField(max_length=255,blank=True) #会社（店舗）名
    manager_name = models.CharField(max_length=100,blank=True) #担当者名
    email = models.EmailField(null=True,blank=True) #ご連絡先メールアドレス
    phone = models.CharField(max_length=16,blank=True) #日中ご連絡先電話番号
    post = models.CharField(max_length=10,blank=True) #郵便番号
    address = models.CharField(max_length=255,blank=True) #住所
    company_overview = models.TextField(blank=True) #会社（店舗）概要
    hope_domain = models.CharField(max_length=255,blank=True) #希望ドメイン
    site_image = models.CharField(max_length=50,choices=SITE_IMAGE_CHOICES,blank=True) #サイト希望イメージ
    site_image_text = models.TextField(blank=True) #希望イメージのその他
    color = models.CharField(max_length=50,choices=COLOR_CHOICES,blank=True) #希望カラー
    color_text = models.TextField(blank=True) #希望イメージのその他
    business = models.TextField(blank=True) #事業内容
    menu = models.TextField(blank=True) #取扱い商材（メニュー）
    strength = models.TextField(blank=True) #自社（自店舗）の強み
    keyword = models.TextField(blank=True) #サイトに記載されたいキーワード
    image_data =models.FileField(upload_to='',null=True,blank=True) #使用する画像とロゴデータ
    hp_plan =models.CharField(max_length=255,blank=True) #ホームページプラン
    created_at = models.DateTimeField("申込日", auto_now_add=True,null=True,blank=True) #申込日

    def __str__(self):
        return self.email

class Insta_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agency_id = models.CharField(max_length=255,blank=True) #代理店ID
    name = models.CharField(max_length=255,blank=True) #名前
    name_ruby = models.CharField(max_length=255,blank=True) #フリガナ
    phone = models.CharField(max_length=16,blank=True) #電話番号
    email = models.EmailField(null=True,blank=True) #ご連絡先メールアドレス
    post = models.CharField(max_length=10,blank=True) #郵便番号
    prefectures =models.CharField(max_length=20,blank=True)#都道府県
    address = models.CharField(max_length=255,blank=True) #住所
    insta_id = models.CharField(max_length=255,blank=True) #インスタアカウント名
    insta_pass = models.CharField(max_length=255,blank=True) #インスタパスワード
    insta_plan = models.CharField(max_length=255,blank=True) #インスタプラン
    created_at = models.DateTimeField("申込日", auto_now_add=True,null=True,blank=True) #申込日

    def __str__(self):
        return self.email

class Card(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    card_token = models.TextField(blank=True) #カードトークン
    customer_id = models.TextField(blank=True) #顧客ID
    sub_id =models.TextField(blank=True) #サブスクID
    email = models.EmailField(null=True,blank=True) #ご連絡先メールアドレス

    def __str__(self):
        return self.email


# def post_user_created(sender, instance, created, **kwargs):
#     if created:
#         hp_obj = Hp_profile(user=instance)
#         insta_obj = Insta_profile(user=instance)
#         card_obj = Card(user=instance)
#         hp_obj.email = instance.email
#         insta_obj.email =instance.email
#         card_obj.email =instance.email
#         hp_obj.save()
#         insta_obj.save()
#         card_obj.save()

# post_save.connect(post_user_created, sender=User)