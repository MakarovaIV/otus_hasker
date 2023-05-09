from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user

from .models import CustomUser, Tag, Question, Answer


class TestIndexView(TestCase):

    def test_response_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class TestQuestionCreateView(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='TestUser',
                                                     email='testuser@mail.ru')
        self.customuser.set_password('test_pass')
        self.customuser.save()

    def tearDown(self) -> None:
        self.customuser.delete()

    def test_create_question(self):
        c = Client()
        Client(enforce_csrf_checks=True)
        c.login(username='TestUser', password='test_pass')
        response = c.post('/ask/', {'title': 'Question',
                                    'body': 'test body'},
                          follow=True)
        self.assertEqual(response.status_code, 200)


class TestAnswerQuestionView(TestCase):
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

    def test_question_detail_negative(self):
        response = self.client.get('/question/999/')
        self.assertEqual(response.status_code, 404)

    def test_question_detail(self):
        response = self.client.get(f'/question/{self.question.pk}/')
        self.assertEqual(response.status_code, 200)


class TestUserSettings(TestCase):
    def setUp(self) -> None:
        self.customuser1 = CustomUser.objects.create(username='TestUser',
                                                    email='testuser@mail.ru')
        self.customuser1.set_password('test_pass')
        self.customuser1.save()
        self.customuser2 = CustomUser.objects.create(username='TestUser2',
                                                     email='testuser2@mail.ru',
                                                     password='test_pass2')

    def tearDown(self) -> None:
        self.customuser2.delete()
        self.customuser1.delete()

    def test_user_settings_negative(self):
        response = self.client.get(f'/settings/{self.customuser1.pk}/')
        self.assertEqual(response.status_code, 404)

    def test_user_settings_positive(self):
        c = Client()
        Client(enforce_csrf_checks=True)
        c.login(username='TestUser', password='test_pass')
        response = c.get(f'/settings/{self.customuser1.pk}/')
        self.assertEqual(response.status_code, 200)


class TestUserSettingView(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='TestUser',
                                                    email='testuser@mail.ru',
                                                    password='test_pass')

    def tearDown(self) -> None:
        self.customuser.delete()

    def test_response_status_code(self):
        response = self.client.get(f'/user/{self.customuser.pk}/')
        self.assertEqual(response.status_code, 200)


class TestSearchQuestion(TestCase):
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

    def test_search_question(self):
        c = Client()
        response = c.get('/', {'search': 'question'})
        self.assertEqual(response.status_code, 200)

    def test_search_question_by_tag(self):
        c = Client()
        response = c.get('/', {'search': 'tag%3Atesttag'})
        self.assertEqual(response.status_code, 200)
