from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, verbose_name="Слаг")
    description = models.TextField(verbose_name="Описание категории")
    image = models.ImageField(upload_to='category')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE, null=True,blank=True, related_name='children',verbose_name="Родительская категория")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['-created']



class Cars(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название машины')
    slug = models.SlugField(max_length=100, verbose_name="Слаг")
    description =  models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=12,decimal_places=2,verbose_name='Цена ($)',null=True,  blank=True)
    image = models.ImageField(upload_to='cars/')
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    engine_volume = models.DecimalField(max_digits=3,decimal_places=1,verbose_name='Объём двигателя (л)',null=True,blank=True)
    horsepower = models.IntegerField(verbose_name='Лошадиные силы',null=True,blank=True)
    year = models.PositiveIntegerField(verbose_name='Год выпуска',null=True,blank=True)
    acceleration_0_100 = models.DecimalField(max_digits=3,decimal_places=1,verbose_name='Разгон 0-100 км/ч (сек)',null=True,blank=True)
    top_speed = models.IntegerField(verbose_name='Максимальная скорость (км/ч)',null=True,blank=True)
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,verbose_name='Автор записи')
    likes = models.ManyToManyField(User,related_name='car_likes',blank=True,verbose_name='Лайки')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'
        ordering = ['-created']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['created']),
            models.Index(fields=['price']),
            models.Index(fields=['year']),
        ]


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True)
    country = models.CharField(max_length=50, verbose_name="Страна")
    founded = models.PositiveIntegerField(verbose_name="Год основания")
    logo = models.ImageField(upload_to='manufacturers/', blank=True)
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'


class CarPhoto(models.Model):
    car = models.ForeignKey(Cars, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='cars/gallery/')
    title = models.CharField(max_length=100, verbose_name="Название фото", blank=True)
    is_main = models.BooleanField(default=False, verbose_name="Главное фото")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Фотография автомобиля'
        verbose_name_plural = 'Фотографии автомобилей'
        ordering = ['-is_main', '-created']


class CarVideo(models.Model):
    car = models.ForeignKey(Cars, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200, verbose_name="Название видео")
    youtube_url = models.URLField(verbose_name="Ссылка на YouTube")
    duration = models.DurationField(verbose_name="Длительность", null=True, blank=True)
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Видео обзор'
        verbose_name_plural = 'Видео обзоры'


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField(verbose_name="Содержание")
    excerpt = models.TextField(max_length=300, verbose_name="Краткое описание")
    image = models.ImageField(upload_to='articles/', verbose_name="Главное изображение")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    cars = models.ManyToManyField(Cars, blank=True, verbose_name="Связанные автомобили")
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created']


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    content = models.TextField(verbose_name="Комментарий")
    car = models.ForeignKey(Cars, on_delete=models.CASCADE, null=True, blank=True,
                            related_name='comments', verbose_name="Автомобиль")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='comments', verbose_name="Статья")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='replies', verbose_name="Ответ на комментарий")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created']









