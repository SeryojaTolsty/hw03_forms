from django import forms
from django.test import Client, TestCase
from django.urls import reverse

from ..models import User, Group, Post
from .constants import (
    AUTHOR_USERNAME,
    GROUP_SLUG,
    URL_INDEX,
    URL_GROUP,
    URL_AUTHOR_PROFILE,
    URL_CREATE_POST,
)


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author_user = User.objects.create_user(username=AUTHOR_USERNAME)
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug=GROUP_SLUG,
            description='Тестовое описание группы',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст поста',
            author=cls.author_user,
            group=cls.group,
        )
        cls.POST_URL = reverse('posts:post_detail', args=[cls.post.id])
        cls.POST_EDIT_URL = reverse('posts:post_edit', args=[cls.post.id])

    def setUp(self):
        self.auth = Client()
        self.auth.force_login(PostPagesTests.author_user)

    def check_post_info(self, post):
        self.assertEqual(post.text, PostPagesTests.post.text)
        self.assertEqual(post.author, PostPagesTests.post.author)
        self.assertEqual(post.group, PostPagesTests.post.group)
        self.assertEqual(post.pk, PostPagesTests.post.pk)

    def test_create_edit_pages_show_correct_context(self):
        """Проверка корректности формы."""
        addresses = (URL_CREATE_POST, PostPagesTests.POST_EDIT_URL)
        for address in addresses:
            with self.subTest(address=address):
                response = self.auth.get(address)
                self.assertIsInstance(
                    response.context['form'].fields['text'],
                    forms.fields.CharField,
                )
                self.assertIsInstance(
                    response.context['form'].fields['group'],
                    forms.fields.ChoiceField,
                )

    def test_post_pages_show_correct_context(self):
        """
        Страницы создаются с верным контекстом
        """
        addresses = [
            URL_INDEX,
            URL_GROUP,
            URL_AUTHOR_PROFILE,
            PostPagesTests.POST_URL,
        ]
        for address in addresses:
            response = self.auth.get(address)
            if (
                'page_obj' in response.context
            ):
                post = response.context.get('page_obj')[
                    0
                ]
            else:
                post = response.context.get('post')
            self.check_post_info(post)

    def test_group_page_show_correct_context(self):
        group = self.auth.get(URL_GROUP).context.get('group')
        self.assertEqual(group.title, PostPagesTests.group.title)
        self.assertEqual(group.slug, PostPagesTests.group.slug),
        self.assertEqual(group.pk, PostPagesTests.group.pk),
        self.assertEqual(group.description, PostPagesTests.group.description)

    def test_profile_page_show_correct_context(self):
        author = self.auth.get(URL_AUTHOR_PROFILE).context.get('author')
        self.assertEqual(author.username, PostPagesTests.author_user.username)
        self.assertEqual(author.pk, PostPagesTests.author_user.pk)


class PaginatorViewsTest(TestCase):
    POSTS_ON_FIRST_PAGE = 10
    POSTS_ON_SECOND_PAGE = 3

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username=AUTHOR_USERNAME)
        cls.group = Group.objects.create(
            title='Тестовое название группы',
            slug=GROUP_SLUG,
            description='Тестовое описание группы',
        )
        cls.PAGES_WITH_PAGINATOR = [URL_INDEX, URL_GROUP, URL_AUTHOR_PROFILE]
        objs = [
            Post(text=f'Пост #{i}', author=cls.user, group=cls.group)
            for i in range(13)
        ]
        Post.objects.bulk_create(objs)

    def setUp(self):
        self.anon = Client()

    def test_paginator_on_pages(self):
        """Проверка паджинации на страницах."""
        for reverse_address in PaginatorViewsTest.PAGES_WITH_PAGINATOR:
            with self.subTest(reverse_address=reverse_address):
                self.assertEqual(
                    len(
                        self.anon.get(
                            reverse_address
                        ).context.get('page_obj')
                    ),
                    self.POSTS_ON_FIRST_PAGE,
                )
                self.assertEqual(
                    len(
                        self.anon.get(
                            reverse_address + '?page=2'
                        ).context.get('page_obj')
                    ),
                    self.POSTS_ON_SECOND_PAGE,
                )
