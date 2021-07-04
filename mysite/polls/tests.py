from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question
import datetime

# Create your tests here.
class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    """
    Creates a Question with pub_date +/- the timedelta of days from timezone.now()
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """
        If no questions, appropriate message is displayed
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
    
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
    
    def test_past_question(self):
        question = create_question("test past question", -30)
        question.save()

        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(response.context['latest_question_list'], [question])
    
    def test_future_question(self):
        question = create_question("test future question", 30)
        question.save()

        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(response.context['latest_question_list'], [])
    
    def test_future_and_past_question(self):
        question_future = create_question("test future question", 30)
        question_past = create_question("test past question", -30)
        question_future.save()
        question_past.save()
        
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question_past])
    
    def test_two_past_questions(self):
        qone = create_question("past question one", -30)
        qtwo = create_question("past question two", -30)
        qone.save()
        qtwo.save()
        
        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(response.context['latest_question_list'], [qone, qtwo])

    def test_two_future_questions(self):
        qone = create_question("future question one", 30)
        qtwo = create_question("future question two", 30)
        qone.save()
        qtwo.save()
        
        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(response.context['latest_question_list'], [])

class DetailViewTest(TestCase):
    
    def test_view_returns_404_if_future_question(self):
        """
        Ensures 404 is returned if question is in the future
        """
        qone = create_question("test future quesiton", 30)
        qone.save()

        response = self.client.get(reverse('polls:detail', args=(qone.id,)))
        self.assertEqual(response.status_code, 404)
    
    def test_view_returns_200_if_past_question(self):
        """
        Ensures question_text of past question exists in detail page
        """
        qone = create_question("test future quesiton", -30)
        qone.save()

        response = self.client.get(reverse('polls:detail', args=(qone.id,)))
        self.assertContains(response, qone.question_text)