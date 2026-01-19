# admin.py - ЗАМЕНИ НА ЭТО
from django.contrib import admin
from django.utils.html import format_html
from .models import *


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ["title", "parent", "cars_count", "created"]
    list_display_links = ["title"]
    list_filter = ["created", "updated"]
    search_fields = ["title", "description"]
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created', 'updated']

    # ДОБАВЬ ЭТОТ МЕТОД:
    def cars_count(self, obj):
        return obj.cars_set.count()

    cars_count.short_description = "Количество машин"


@admin.register(Cars)
class AdminCars(admin.ModelAdmin):
    list_display = ["name", "year", "price", "horsepower", "category_link", "is_active", "created"]
    list_display_links = ["name"]
    list_filter = ["year", "price", "is_active", "created", "cat"]
    search_fields = ["name", "description"]
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['views', 'created', 'updated', 'image_preview']
    filter_horizontal = ['likes']  # Для удобного выбора лайков

    # ДОБАВЬ ЭТИ ПОЛЯ В fieldsets для красивого отображения:
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'description', 'cat', 'author', 'is_active')
        }),
        ('Технические характеристики', {
            'fields': ('year', 'price', 'engine_volume', 'horsepower',
                       'acceleration_0_100', 'top_speed')
        }),
        ('Медиа', {
            'fields': ('image', 'image_preview')
        }),
        ('Статистика', {
            'fields': ('views', 'likes', 'created', 'updated')
        }),
    )

    # КАСТОМНЫЕ МЕТОДЫ:
    def category_link(self, obj):
        if obj.cat:
            return format_html('<a href="/admin/cars/category/{}/change/">{}</a>',
                               obj.cat.id, obj.cat.title)
        return "-"

    category_link.short_description = "Категория"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" />', obj.image.url)
        return "Нет изображения"

    image_preview.short_description = "Предпросмотр"


# ДОБАВЬ РЕГИСТРАЦИЮ НОВЫХ МОДЕЛЕЙ:
@admin.register(Manufacturer)
class AdminManufacturer(admin.ModelAdmin):
    list_display = ["name", "country", "founded", "cars_count"]
    search_fields = ["name", "country"]
    prepopulated_fields = {'slug': ('name',)}

    def cars_count(self, obj):
        return Cars.objects.filter(name__icontains=obj.name).count()


@admin.register(CarPhoto)
class AdminCarPhoto(admin.ModelAdmin):
    list_display = ["car", "title", "is_main", "image_preview", "created"]
    list_filter = ["is_main", "created"]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "Нет изображения"


@admin.register(Article)
class AdminArticle(admin.ModelAdmin):
    list_display = ["title", "author", "views", "is_published", "created"]
    list_filter = ["is_published", "created", "author"]
    search_fields = ["title", "content"]
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['cars']
    readonly_fields = ['views', 'created', 'updated']


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ["user", "short_content", "car", "article", "is_active", "created"]
    list_filter = ["is_active", "created", "user"]
    search_fields = ["content", "user__username"]

    def short_content(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    short_content.short_description = "Комментарий"

