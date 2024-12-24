"""
Этот файл содержит конфигурацию приложения блога.
Требования:
- Добавить комментарий в заголовке, объясняющий требования и изменения, внесенные после автотестов второго модуля.
"""

from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = 'Блог'
