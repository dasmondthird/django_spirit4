"""
Этот файл содержит представления для приложения блога.
Требования:
- Добавить комментарий в заголовке, объясняющий требования и изменения, внесенные после автотестов второго модуля.
- Добавить док-строки к функциям, чтобы расширить заголовочный комментарий.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CreateCommentForm, CreatePostForm
from .models import Category, Comment, Post, User
from .mixins import (CommentEditMixin, PostsEditMixin)
from .utils import (filter_published_posts)

PAGINATED_BY = 10


class PostDeleteView(PostsEditMixin, LoginRequiredMixin, DeleteView):
    """
    Представление для удаления публикации.
    Удаляет публикацию, если пользователь является автором.
    """
    model = Post
    success_url = reverse_lazy('blog:index')
    pk_url_kwarg = 'post_id'

    def delete(self, request, *args, **kwargs):
        """Удаляет публикацию, если пользователь является автором."""
        post = get_object_or_404(Post, pk=self.kwargs[self.pk_url_kwarg])
        if self.request.user != post.author:
            return redirect('blog:index')

        return super().delete(request, *args, **kwargs)


class PostUpdateView(PostsEditMixin, LoginRequiredMixin, UpdateView):
    """
    Представление для обновления публикации.
    Обрабатывает запрос, если пользователь является автором.
    """
    form_class = CreatePostForm
    model = Post
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        """Обрабатывает запрос, если пользователь является автором."""
        post = get_object_or_404(Post, pk=self.kwargs[self.pk_url_kwarg])
        if self.request.user != post.author:
            return redirect('blog:post_detail',
                            post_id=self.kwargs[self.pk_url_kwarg])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """Возвращает URL успешного выполнения после обновления публикации."""
        return reverse('blog:post_detail',
                       args=[self.kwargs[self.pk_url_kwarg]])


class PostCreateView(PostsEditMixin, LoginRequiredMixin, CreateView):
    """
    Представление для создания новой публикации.
    Устанавливает автора публикации текущим пользователем.
    """
    model = Post
    form_class = CreatePostForm

    def form_valid(self, form):
        """Устанавливает автора публикации текущим пользователем."""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        """Возвращает URL успешного выполнения после создания публикации."""
        return reverse(
            'blog:profile',
            args=[self.request.user.username]
        )


class CommentCreateView(CommentEditMixin, LoginRequiredMixin, CreateView):
    """
    Представление для создания нового комментария.
    Устанавливает пост и автора комментария.
    """
    model = Comment
    form_class = CreateCommentForm

    def form_valid(self, form):
        """Устанавливает пост и автора комментария."""
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentDeleteView(CommentEditMixin, LoginRequiredMixin, DeleteView):
    """
    Представление для удаления комментария.
    Удаляет комментарий, если пользователь является автором.
    """
    model = Comment
    pk_url_kwarg = 'comment_id'

    def delete(self, request, *args, **kwargs):
        """Удаляет комментарий, если пользователь является автором."""
        comment = get_object_or_404(Comment, pk=self.kwargs[self.pk_url_kwarg])
        if self.request.user != comment.author:
            return redirect('blog:post_detail', post_id=self.kwargs['post_id'])
        return super().delete(request, *args, **kwargs)


class CommentUpdateView(CommentEditMixin, LoginRequiredMixin, UpdateView):
    """
    Представление для обновления комментария.
    Обрабатывает запрос, если пользователь является автором.
    """
    model = Comment
    form_class = CreateCommentForm
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        """Обрабатывает запрос, если пользователь является автором."""
        comment = get_object_or_404(Comment, pk=self.kwargs[self.pk_url_kwarg])
        if self.request.user != comment.author:
            return redirect('blog:post_detail', post_id=self.kwargs['post_id'])

        return super().dispatch(request, *args, **kwargs)


class AuthorProfileListView(ListView):
    """
    Представление для отображения профиля автора.
    Возвращает набор публикаций для профиля автора.
    """
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = PAGINATED_BY

    def get_queryset(self):
        """Возвращает набор публикаций для профиля автора."""
        author = get_object_or_404(User, username=self.kwargs['username'])
        posts = author.posts.all()
        if self.request.user != author:
            posts = filter_published_posts(posts)
        return posts

    def get_context_data(self, **kwargs):
        """Возвращает контекстные данные для профиля автора."""
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User, username=self.kwargs['username']
        )
        return context


class BlogIndexListView(ListView):
    """
    Представление для отображения главной страницы блога.
    Возвращает набор опубликованных публикаций.
    """
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = PAGINATED_BY

    queryset = filter_published_posts(Post.objects)


class BlogCategoryListView(ListView):
    """
    Представление для отображения публикаций по категориям.
    Возвращает набор публикаций для указанной категории.
    """
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'post_list'
    paginate_by = PAGINATED_BY

    def get_queryset(self):
        """Возвращает набор публикаций для указанной категории."""
        category_slug = self.kwargs['category_slug']
        category = get_object_or_404(Category, slug=category_slug,
                                     is_published=True)
        posts = filter_published_posts(category.posts.all())
        return posts


class PostDetailView(DetailView):
    """
    Представление для детального просмотра публикации.
    Возвращает объект публикации для детального просмотра.
    """
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        """Возвращает контекстные данные для детального просмотра публикации."""
        context = super().get_context_data(**kwargs)
        context['form'] = CreateCommentForm()
        context['comments'] = (
            self.get_object().comments.prefetch_related('author').all()
        )
        return context

    def get_object(self, queryset=None):
        """Возвращает объект публикации для детального просмотра."""
        post = get_object_or_404(Post, pk=self.kwargs.get(self.pk_url_kwarg))
        if self.request.user == post.author:
            return post
        return get_object_or_404(
            filter_published_posts(Post.objects.all()),
            pk=self.kwargs.get(self.pk_url_kwarg)
        )
