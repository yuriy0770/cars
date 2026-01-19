from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView as AuthLoginView

from .forms import (
    UserRegisterForm,
    UserLoginForm,
    UserUpdateForm,
    ProfileUpdateForm,
    CustomPasswordChangeForm
)
from .models import Profile


class RegisterView(CreateView):
    """
    Представление для регистрации пользователя
    Наследуемся от CreateView - стандартного Django класса для создания объектов
    """
    form_class = UserRegisterForm  # Используем нашу форму
    template_name = 'users/register.html'  # Шаблон для отображения
    success_url = reverse_lazy('users:login')  # Куда перенаправить после успешной регистрации

    def form_valid(self, form):
        """
        Метод вызывается при успешной валидации формы
        """
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Аккаунт успешно создан! Теперь вы можете войти.'
        )
        return response

    def form_invalid(self, form):
        """
        Метод вызывается при невалидной форме
        """
        messages.error(
            self.request,
            'Пожалуйста, исправьте ошибки в форме.'
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """
        Добавляем дополнительные данные в контекст шаблона
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context


class LoginView(AuthLoginView):
    """
    Представление для входа пользователя
    Наследуемся от стандартного AuthLoginView Django
    """
    form_class = UserLoginForm  # Используем нашу кастомную форму
    template_name = 'users/login.html'  # Шаблон для отображения

    def form_valid(self, form):
        """
        Метод вызывается при успешной аутентификации
        """
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Добро пожаловать, {self.request.user.username}!'
        )
        return response

    def form_invalid(self, form):
        """
        Метод вызывается при неудачной аутентификации
        """
        messages.error(
            self.request,
            'Неверное имя пользователя или пароль.'
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """
        Добавляем дополнительные данные в контекст
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход'
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Представление для просмотра профиля пользователя
    LoginRequiredMixin - миксин, требующий авторизации
    TemplateView - стандартный класс для отображения шаблона
    """
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        """
        Получаем данные профиля для отображения
        """
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.profile
        context['title'] = 'Мой профиль'
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для обновления профиля пользователя
    UpdateView - стандартный класс для обновления объектов
    """
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        """
        Получаем объект профиля текущего пользователя
        """
        return self.request.user.profile

    def form_valid(self, form):
        """
        При успешном обновлении показываем сообщение
        """
        messages.success(self.request, 'Профиль успешно обновлен!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Добавляем форму пользователя в контекст
        """
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        context['title'] = 'Редактирование профиля'
        return context

    def post(self, request, *args, **kwargs):
        """
        Обрабатываем POST запрос для обеих форм
        """
        self.object = self.get_object()
        profile_form = self.get_form()
        user_form = UserUpdateForm(request.POST, instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            return self.form_valid(profile_form, user_form)
        else:
            return self.form_invalid(profile_form, user_form)

    def form_valid(self, profile_form, user_form):
        """
        Обрабатываем обе формы
        """
        profile_form.save()
        user_form.save()
        messages.success(self.request, 'Профиль успешно обновлен!')
        return redirect(self.success_url)

    def form_invalid(self, profile_form, user_form):
        """
        Обрабатываем ошибки в формах
        """
        context = self.get_context_data(
            form=profile_form,
            user_form=user_form
        )
        return self.render_to_response(context)


# Функциональные представления (для примера, как альтернатива классам)
@login_required
def logout_view(request):
    """
    Функциональное представление для выхода
    Декоратор @login_required требует авторизации
    """
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('cars:index')


@login_required
def password_change_view(request):
    """
    Функциональное представление для смены пароля
    """
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменен!')
            return redirect('users:profile')
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'users/password_change.html', {
        'form': form,
        'title': 'Смена пароля'
    })
