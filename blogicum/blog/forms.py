"""
Этот файл содержит формы для приложения блога.
Требования:
- Добавить комментарий в заголовке, объясняющий требования и изменения, внесенные после автотестов второго модуля.
- Добавить док-строки к функциям, чтобы расширить заголовочный комментарий.
"""

from django import forms
from django.utils import timezone

from .models import Comment, Post


class CreatePostForm(forms.ModelForm):
    pub_date = forms.DateTimeField(
        initial=timezone.now,
        required=True,
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
            },
            format='%Y-%m-%dT%H:%M',
        ),
    )

    class Meta:
        model = Post
        fields = (
            'title',
            'image',
            'text',
            'pub_date',
            'location',
            'category',
            'is_published',
        )

    def __init__(self, *args, **kwargs):
        """Инициализирует форму с пользовательскими настройками."""
        super().__init__(*args, **kwargs)


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)

    def __init__(self, *args, **kwargs):
        """Инициализирует форму с пользовательскими настройками."""
        super().__init__(*args, **kwargs)
