from django.core.files import File
from django.test import TestCase

import mock

from .models import CustomUser, Tag, Question, Answer


class TestCustomUser(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='TestUser',
                                                    email='testuser@mail.ru',
                                                    password='test_pass')

    def tearDown(self) -> None:
        self.customuser.delete()

    def test_init(self):
        self.assertTrue(isinstance(self.customuser.username, str))
        self.assertEqual(self.customuser.username, 'TestUser')
        self.assertTrue(isinstance(self.customuser.email, str))
        self.assertEqual(self.customuser.email, 'testuser@mail.ru')
        self.assertTrue(isinstance(self.customuser.password, str))
        self.assertEqual(self.customuser.password, 'test_pass')

    def test_file_field(self):
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = 'test.pdf'
        file_model = CustomUser(picture=file_mock)
        self.assertEqual(file_model.picture.name, file_mock.name)


class TestTag(TestCase):
    def setUp(self) -> None:
        self.tag = Tag.objects.create(name='testtag')

    def tearDown(self) -> None:
        self.tag.delete()

    def test_init(self):
        self.assertTrue(isinstance(self.tag.name, str))
        self.assertEqual(self.tag.name, 'testtag')


class TestQuestion(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='TestUser',
                                                    email='testuser@mail.ru',
                                                    password='test_pass')
        self.tag1 = Tag.objects.create(name='testtag')
        self.tag2 = Tag.objects.create(name='testtag2')
        self.question = Question.objects.create(title='Test question',
                                                body='How to test',
                                                user=self.customuser,
                                                answers_count=2,
                                                votes_count=3)
        self.question.tags.set([self.tag1.pk, self.tag2.pk])

    def tearDown(self) -> None:
        self.question.delete()
        self.tag2.delete()
        self.tag1.delete()
        self.customuser.delete()

    def test_init(self):
        self.assertTrue(isinstance(self.question.title, str))
        self.assertEqual(self.question.title, 'Test question')
        self.assertTrue(isinstance(self.question.body, str))
        self.assertEqual(self.question.body, 'How to test')
        self.assertEqual(self.question.user.username, 'TestUser')
        self.assertEqual(self.question.tags.count(), 2)
        self.assertEqual(self.question.answers_count, 2)
        self.assertEqual(self.question.votes_count, 3)


class TestAnswer(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='TestUser',
                                                    email='testuser@mail.ru',
                                                    password='test_pass')
        self.question = Question.objects.create(title='Test question',
                                                body='How to test',
                                                user=self.customuser,
                                                answers_count=2,
                                                votes_count=3)
        self.answer = Answer.objects.create(body='Answer on question',
                                            user=self.customuser,
                                            question=self.question,
                                            votes_count=3,
                                            is_correct=True)

    def tearDown(self) -> None:
        self.answer.delete()
        self.question.delete()
        self.customuser.delete()

    def test_init(self):

        self.assertTrue(isinstance(self.answer.body, str))
        self.assertEqual(self.answer.body, 'Answer on question')
        self.assertEqual(self.answer.user.username, 'TestUser')
        self.assertEqual(self.answer.question.title, 'Test question')
        self.assertEqual(self.answer.votes_count, 3)
        self.assertTrue(self.answer.is_correct)
