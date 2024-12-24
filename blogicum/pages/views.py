"""
Этот файл содержит представления для приложения страниц.
Требования:
- Добавить комментарий в заголовке, объясняющий требования и изменения, внесенные после автотестов второго модуля.
- Добавить док-строки к функциям, чтобы расширить заголовочный комментарий.
"""

from django.shortcuts import render
from django.views.generic import TemplateView


class AboutTemplateView(TemplateView):
    """
    Представление для отображения страницы "О нас".
    """
    template_name = 'pages/about.html'


class RulesTemplateView(TemplateView):
    """
    Представление для отображения страницы "Правила".
    """
    template_name = 'pages/rules.html'


def permission_denied(request, exception):
    """
    Обработчик ошибки 403.
    Возвращает страницу с ошибкой 403.
    """
    return render(request, 'pages/403.html', status=403)


def csrf_failure(request, reason=''):
    """
    Обработчик ошибки CSRF.
    Возвращает страницу с ошибкой CSRF.
    """
    return render(request, 'pages/403csrf.html', status=403)


def page_not_found(request, exception):
    """
    Обработчик ошибки 404.
    Возвращает страницу с ошибкой 404.
    """
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    """
    Обработчик ошибки 500.
    Возвращает страницу с ошибкой 500.
    """
    return render(request, 'pages/500.html', status=500)
