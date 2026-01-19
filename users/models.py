from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    Расширенная модель профиля пользователя
    Связана один-к-одному со стандартной моделью User Django
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")

    # Дополнительные поля
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name="Местоположение")
    bio = models.TextField(blank=True, null=True, verbose_name="О себе")

    # Статистика
    cars_added = models.PositiveIntegerField(default=0, verbose_name="Добавлено автомобилей")
    reviews_written = models.PositiveIntegerField(default=0, verbose_name="Написано обзоров")

    # Настройки
    email_notifications = models.BooleanField(default=True, verbose_name="Email уведомления")
    newsletter = models.BooleanField(default=True, verbose_name="Рассылка новостей")

    # Технические поля
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"Профиль {self.user.username}"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['-created']


# Сигналы для автоматического создания профиля при создании пользователя
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Создаем профиль автоматически при создании пользователя
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Сохраняем профиль при сохранении пользователя
    """
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)
