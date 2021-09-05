import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question


class QuestionModelTest(TestCase):

    def test_was_recently_published_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        question = Question(pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertIs(question.was_published_recently(), False)

    def test_was_recently_published_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is long gone (ex: more than 3 days old).
        """
        question = Question(pub_date=timezone.now() - datetime.timedelta(days=3, seconds=1))
        self.assertIs(question.was_published_recently(), False)

    def test_was_recently_published_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is recent (ex: less than 3 days old).
        """
        question = Question(pub_date=timezone.now() - datetime.timedelta(days=2, hours=23, minutes=59, seconds=59))
        self.assertIs(question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        res = self.client.get(reverse('polls:index'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'No polls are available.')
        self.assertQuerysetEqual(res.context['questions'], [])

    def test_past_question(self):
        """
        Questions with pub_date in the past are displayed on the index page
        """
        question_text = 'the is a past question'
        q = create_question(question_text, -30)
        res = self.client.get(reverse('polls:index'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, question_text)
        self.assertQuerysetEqual(res.context['questions'], [q])

    def test_future_question(self):
        """
        Questions with pub_date in the future are NOT displayed on the index page
        """
        question_text = 'the is a future question'
        create_question(question_text, +1)
        res = self.client.get(reverse('polls:index'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'No polls are available.')
        self.assertQuerysetEqual(res.context['questions'], [])

    def test_past_and_future_questions(self):
        """
        If there are questions with pub_date in the past and future only the past ones are displayed on the index page
        """
        future = create_question('this is a future question', +1)
        past = create_question('this is a past question', -1)
        res = self.client.get(reverse('polls:index'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, past.question_text)
        self.assertNotContains(res, future.question_text)
        self.assertQuerysetEqual(res.context['questions'], [past])

    def test_multiple_past_questions(self):
        """
        Multiple past questions are displayed on the index page
        """
        questions = [
            create_question('past question 1', -1),
            create_question('past question 2', -30),
        ]
        res = self.client.get(reverse('polls:index'))
        self.assertEqual(res.status_code, 200)
        for q in questions:
            self.assertContains(res, q.question_text)
        self.assertQuerysetEqual(res.context['questions'], questions)

    def test_questions_without_choices(self):
        """
        Questions with no choices should NOT be shown on the index page
        """
        create_question('no choice?', with_choice=False)
        res = self.client.get(reverse('polls:index'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'No polls are available.')
        self.assertQuerysetEqual(res.context['questions'], [])

    def test_questions_with_choices(self):
        """
        Questions with choices should be shown on the index page
        """
        q = create_question('has a choice', with_choice=True)
        res = self.client.get(reverse('polls:index'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, q.question_text)
        self.assertQuerysetEqual(res.context['questions'], [q])

    def test_questions_with_and_without_choices(self):
        """
        Only the questions with choices should be shown and the ones without should be excluded from the index page
        """
        q_with_choice = create_question('has a choice', with_choice=True)
        q_without_choice = create_question('does not have a choice', with_choice=False)
        res = self.client.get(reverse('polls:index'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, q_with_choice.question_text)
        self.assertNotContains(res, q_without_choice.question_text)
        self.assertQuerysetEqual(res.context['questions'], [q_with_choice])


class QuestionDetailViewTests(TestCase):

    def test_past_question(self):
        q = create_question('past question', -1)
        res = self.client.get(reverse('polls:detail', args=(q.id,)))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, q.question_text)
        self.assertEqual(res.context['question'], q)

    def test_future_question(self):
        q = create_question('future question', 1)
        res = self.client.get(reverse('polls:detail', args=(q.id,)))
        self.assertEqual(res.status_code, 404)
        self.assertNotIn('question', res.context)


class QuestionResultsViewTests(TestCase):

    def test_past_question(self):
        q = create_question('past question', -1)
        res = self.client.get(reverse('polls:results', args=(q.id,)))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, q.question_text)
        self.assertEqual(res.context['question'], q)

    def test_future_question(self):
        q = create_question('future question', 1)
        res = self.client.get(reverse('polls:results', args=(q.id,)))
        self.assertEqual(res.status_code, 404)
        self.assertNotIn('question', res.context)


def create_question(question_text, days=0, with_choice=True):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    q = Question.objects.create(question_text=question_text, pub_date=time)
    if with_choice:
        q.choices.create(choice_text='auto generated choice 1')
    return q
