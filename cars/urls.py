from django.urls import path
from . import views

app_name = 'cars'


urlpatterns = [
    path("", views.Template.as_view(), name='index'),
    path("categories/", views.CategoryList.as_view(), name='category'),
    path("categories/<slug:cat_slug>/", views.CarsList.as_view(), name='cars'),
    path("car/<slug:car_slug>/", views.CarDetail.as_view(), name='car_detail'),
    path("about/", views.AboutView.as_view(), name='about'),
]





