from audioop import reverse

from django.test import TestCase
from django.test import Client

from .models import CustomUser, Tag, Question


class TestGetTrendingQuestions(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='TestUser',
                                                    email='testuser@mail.ru',
                                                    password='test_pass')
        self.tag1 = Tag.objects.create(name='testtag')
        self.question = Question.objects.create(title='Test question',
                                                body='How to test',
                                                user=self.customuser,
                                                answers_count=2,
                                                votes_count=3)
        self.question.tags.set([self.tag1.pk])

    def tearDown(self) -> None:
        self.question.delete()
        self.tag1.delete()
        self.customuser.delete()

    def test_returned_trending_list(self):
        users = Question.objects.all()
        self.assertEqual(users.count(), 1)


class TestIndexView(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='TestUser',
                                                    email='testuser@mail.ru',
                                                    password='test_pass')
        self.tag1 = Tag.objects.create(name='testtag')
        self.question = Question.objects.create(title='Test question',
                                                body='How to test',
                                                user=self.customuser,
                                                answers_count=2,
                                                votes_count=3)
        self.question.tags.set([self.tag1.pk])

    def tearDown(self) -> None:
        self.question.delete()
        self.tag1.delete()
        self.customuser.delete()

    def test_index_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_returned_list(self):
        users = Question.objects.all()
        self.assertEqual(users.count(), 1)

    def test_index_page_view_name(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, template_name='hasker_app/index.html')


class TestRegister(TestCase):
    def setUp(self) -> None:
        self.username = 'testuser'
        self.email = 'testuser@email.com'
        self.age = 20
        self.password = 'q1w2e3r4t5y61'

    def test_registre_status_code(self):
        response = self.client.get("/signup/")
        self.assertEqual(response.status_code, 200)

    def test_signup_form(self):
        self.client.post('/signup/', {
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password
        })
        users = CustomUser.objects.all()
        self.assertEqual(users.count(), 1)

    def test_signup_page_view_name(self):
        response = self.client.get('/signup/')
        self.assertTemplateUsed(response, template_name='hasker_app/signup_form.html')


class TestLogin(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='TestUser',
                                                    email='testuser@mail.ru')
        self.customuser.set_password('test_pass')
        self.customuser.save()

    def tearDown(self) -> None:
        self.customuser.delete()

    def test_login_status_code(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_login_form(self):
        response = self.client.post('/login/', {
            'username': self.customuser.username,
            'password': self.customuser.password,
        })
        self.assertEqual(response.status_code, 200)

    def test_login_page_view_name(self):
        response = self.client.get('/login/')
        self.assertTemplateUsed(response, template_name='hasker_app/login.html')


class TestLogout(TestCase):
    def test_logout_status_code(self):
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 200)

    def test_logout_page_view_name(self):
        response = self.client.get('/logout/')
        self.assertTemplateUsed(response, template_name='hasker_app/logout.html')


class TestGetUserImage(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='TestUser',
                                                    email='testuser@mail.ru')
        self.customuser.set_password('test_pass')
        self.customuser.save()

    def test_response_status_code(self):
        response = self.client.get(f'/get_user_image/{self.customuser.pk}/',)
        self.assertEqual(response.status_code, 200)

    def tearDown(self) -> None:
        self.customuser.delete()


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

    def test_question_page_view_name(self):
        response = self.client.get('/ask/')
        self.assertTemplateUsed(response, template_name='hasker_app/question_form.html')


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

    def test_answer_page_view_name(self):
        response = self.client.get(f'/question/{self.question.pk}/')
        self.assertTemplateUsed(response, template_name='hasker_app/answer_form.html')


class TestCreateAnswer(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='TestUser',
                                                    email='testuser@mail.ru',
                                                    password='test_pass')
        self.tag1 = Tag.objects.create(name='testtag')
        self.question = Question.objects.create(title='Test question',
                                                body='How to test',
                                                user=self.customuser,
                                                answers_count=2,
                                                votes_count=3)
        self.question.tags.set([self.tag1.pk])

    def tearDown(self) -> None:
        self.question.delete()
        self.tag1.delete()
        self.customuser.delete()

    def test_create_answer(self):
        c = Client()
        Client(enforce_csrf_checks=True)
        c.login(username='TestUser', password='test_pass')
        response = c.post('/answer/',
                          {'body': 'answer',
                           'question_id': self.question.pk,
                           'user_id': self.customuser},
                          follow=True)
        self.assertEqual(response.status_code, 200)


class TestUserSettings(TestCase):
    def setUp(self) -> None:
        self.customuser1 = CustomUser.objects.create(username='TestUser',
                                                     email='testuser@mail.ru')
        self.customuser1.set_password('test_pass')
        self.customuser1.save()

    def tearDown(self) -> None:
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

    def test_change_profile_page_view_name(self):
        c = Client()
        Client(enforce_csrf_checks=True)
        c.login(username='TestUser', password='test_pass')
        response = c.get(f'/settings/{self.customuser1.pk}/')
        self.assertTemplateUsed(response, template_name='hasker_app/customuser_form.html')


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

    def test_profile_page_view_name(self):
        response = self.client.get(f'/user/{self.customuser.pk}/')
        self.assertTemplateUsed(response, template_name='hasker_app/customuser_detail.html')


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
