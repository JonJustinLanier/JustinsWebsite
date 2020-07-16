from django.utils import timezone
from django.test import TestCase
from .models import Question
from django.urls import reverse

import datetime


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):

    def test_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for question whose pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date = time)
        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for question whose pub_date is older than one day.
        """
        time = timezone.now() - datetime.timedelta(days=1, hours=1)
        future_question = Question(pub_date = time)
        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for a question whose pub_date is less than one day.
        """
        time = timezone.now() - datetime.timedelta(hours=23)
        future_question = Question(pub_date = time)
        self.assertTrue(future_question.was_published_recently())
