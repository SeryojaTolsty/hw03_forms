from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post


User = get_user_model()
LEN_OF_POSTS = 15
# константа длины строки


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.post = Post.objects.create(
            text='Тестовый текст (строка 15 символов)',
            author=cls.user,
        )

    def test_post_str(self):
        """Проверка __str__ у post."""
        self.assertEqual(PostModelTest.post.text[:15], str(PostModelTest.post))

    def test_post_verbose_name(self):
        """Проверка verbose_name у post."""
        self.post_model_field_to_verbose = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
        }
        for (
            value,
            expected,
        ) in self.post_model_field_to_verbose.items():
            with self.subTest(value=value):
                verbose_name = self.post._meta.get_field(value).verbose_name
                self.assertEqual(verbose_name, expected)

    def test_post_help_text(self):
        """Проверка help_text у post."""
        self.post_model_field_to_help = {
            'text': 'Введите текст поста',
            'group': 'Группа, относительно поста',
        }
        for (
            value,
            expected
        ) in self.post_model_field_to_help.items():
            with self.subTest(value=value):
                help_text = self.post._meta.get_field(value).help_text
                self.assertEqual(help_text, expected)
