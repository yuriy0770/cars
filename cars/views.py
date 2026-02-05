from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Category, Cars, Article


class Template(TemplateView):
    '''Главная страница'''
    template_name = 'cars/index.html'


class CategoryList(ListView):
    '''Список категорий'''
    model = Category
    context_object_name = "category"
    template_name = 'cars/category_list.html'

    def get_queryset(self):
        return Category.objects.all().order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_cars'] = Cars.objects.count()
        return context


class CarsList(ListView):
    context_object_name = 'cars'
    template_name = 'cars/cars_list.html'

    def get_queryset(self):
        category_slug = self.kwargs.get('cat_slug')
        category = get_object_or_404(Category, slug=category_slug)
        return Cars.objects.filter(cat=category).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('cat_slug')
        context['category'] = get_object_or_404(Category, slug=category_slug)
        return context


class CarDetail(DetailView):
    model = Cars
    context_object_name = 'car'
    template_name = 'cars/car_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'car_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views += 1
        self.object.save(update_fields=['views'])
        return context


class AboutView(TemplateView):
    template_name = 'cars/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем статистику для страницы "О проекте"
        context['total_cars'] = Cars.objects.count()
        context['total_categories'] = Category.objects.count()
        context['total_articles'] = Article.objects.count()
        return context