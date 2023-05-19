from django.urls import reverse, path, include
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from hasker_app.models import CustomUser, Question, Answer, Tag

QUESTION_COUNT = 2


class TestAPIQuestionsList(APITestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def setUp(self):
        self.customuser = CustomUser.objects.create(username='TestUser',
                                                    email='testuser@mail.ru')
        self.customuser.set_password('test_pass')
        self.customuser.save()
        self.tag1 = Tag.objects.create(name='tag1')
        self.tag2 = Tag.objects.create(name='tag2')
        self.question1 = Question.objects.create(title='Test question',
                                                 body='How to test',
                                                 user=self.customuser,
                                                 answers_count=2,
                                                 votes_count=3)
        self.question1.tags.set([self.tag1.pk])
        self.question2 = Question.objects.create(title='Test question2',
                                                 body='How to test2',
                                                 user=self.customuser,
                                                 answers_count=1,
                                                 votes_count=1)
        self.question2.tags.set([self.tag2.pk])
        self.answer = Answer.objects.create(question=self.question2,
                                            body='How to test2',
                                            user=self.customuser)

    def tearDown(self) -> None:
        self.answer.delete()
        self.question2.delete()
        self.question1.delete()
        self.tag2.delete()
        self.tag1.delete()
        self.customuser.delete()

    def test_questions_list(self):
        url = reverse('api_questions_list')
        response = self.client.get(url, format="json")
        item = response.data['results'][0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(item['id'], self.question1.id)
        self.assertEqual(item['user'], self.question1.user.username)
        self.assertEqual(item['title'], self.question1.title)
        self.assertEqual(item['body'], self.question1.body)
        self.assertEqual(item['tags'][0]['name'], self.tag1.name)

    def test_question_detail(self):
        url = reverse('api_question_detail', kwargs={"pk": self.question1.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.question1.id)
        self.assertEqual(response.data['user'], self.question1.user.username)
        self.assertEqual(response.data['title'], self.question1.title)
        self.assertEqual(response.data['body'], self.question1.body)
        self.assertEqual(response.data['tags'][0]['name'], self.tag1.name)

    def test_trending_list(self):
        url = reverse('api_trending')
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), QUESTION_COUNT)

    def test_search_question(self):
        url = f"{reverse('api_search_question')}?search=Test"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), QUESTION_COUNT)

    def test_search_question_by_tag(self):
        url = f"{reverse('api_search_question')}?search=tag1"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_answers_list(self):
        c = APIClient()
        c.login(username='TestUser', password='test_pass')
        url = reverse('api_answers', kwargs={"question_id": self.question2.id})
        response = c.get(url, format="json")
        item = response.data['results'][0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(item['id'], self.answer.id)
        self.assertEqual(item['question_title'], self.question2.title)
        self.assertEqual(item['question_body'], self.question2.body)
        self.assertEqual(item['asked_user'], self.customuser.username)
        self.assertEqual(item['body'], self.answer.body)
