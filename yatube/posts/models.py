from django.contrib.auth import get_user_model
from django.db import models
# from pytils.translit import slugify

User = get_user_model()


LEN_OF_POSTS = 15
# константа длины строки


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название группы',
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Ключ',
        help_text='Ключ для группы в адресной строке',
    )
    description = models.TextField(
        verbose_name='Описание',
    )

    class Meta:
        verbose_name = 'Жанр'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        'Текст поста',
        help_text='Введите текст поста',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='posts',
    )
    group = models.ForeignKey(
        Group,
        related_name='posts',
        verbose_name='Группа',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text='Группа, относительно поста'
    )

    class Meta:
        verbose_name = 'Пост'
        ordering = ('-pub_date', 'author')

    def __str__(self,):
        return self.text[:LEN_OF_POSTS]
