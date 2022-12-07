from .forms import QuillFieldForm, ArticleForm, QuestionForm, AnswerForm
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormMixin
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from .models import Article, Course, Test, Question, Answer, UniqueTest, TestResult
import random


def index(request):
    return render(request, 'ismoktify/index.html')


class ArticleCreateView(CreateView):
    model = Article
    fields = ['course', 'title', 'content']

    def get_success_url(self) -> str:
        return reverse('ismoktify:course_detail', kwargs={'course_name': Article.objects.latest('title').course.name})


class CoursesListView(ListView):
    model = Course
    template_name = 'ismoktify/course_list.html'


def course_view(request, course_name):
    course = get_object_or_404(Course, pk=course_name)
    articles = Article.objects.filter(course=course_name)
    context = {
        'course': course,
        'articles': articles
    }
    return render(request, 'ismoktify/course_detail.html', context=context)


def article_view(request, article_id, course_name):
    article = get_object_or_404(Article, pk=article_id)
    context = {
        'article': article
    }
    return render(request, 'ismoktify/article_detail.html', context=context)


def article_edit_view(request, article_id, course_name):
    article = Article.objects.get(id=article_id)
    article_copy = Article.objects.get(id=article_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article.course = article_copy.course
            form.save()
            return redirect('ismoktify:article_detail', article.course.name, article.id)
    else:
        form = ArticleForm(instance=article)

    return render(request, 'ismoktify/article_edit.html', {'form': form})


class CourseCreateView(CreateView):
    model = Course
    fields = ['name']
    success_url = reverse_lazy('ismoktify:course_list')


class TestCreateView(CreateView):
    model = Test
    fields = ['course', 'title', 'number_of_easy_questions',
              'number_of_medium_questions', 'number_of_hard_questions']

    def get_success_url(self):
        return reverse('ismoktify:test_detail', kwargs={'pk': Test.objects.latest('id').id})


class TestDetailView(FormMixin, DetailView):
    model = Test
    template_name = 'ismoktify/test_detail.html'
    form_class = QuestionForm

    def get_success_url(self):
        return reverse('ismoktify:question_detail', kwargs={'pk': Question.objects.latest('id').id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.test = self.object
        form.save()
        return super(TestDetailView, self).form_valid(form)


class QuestionDetailView(FormMixin, DetailView):
    model = Question
    template_name = 'ismoktify/question_detail.html'
    form_class = AnswerForm

    def get_success_url(self):
        return reverse('ismoktify:question_detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.question = self.object
        form.save()
        return super(QuestionDetailView, self).form_valid(form)


def answer_delete(request, pk):
    query = Answer.objects.get(id=pk)
    link = query.question.id
    query.delete()
    return (redirect('ismoktify:question_detail', link))


def question_delete(request, pk):
    query = Question.objects.get(id=pk)
    link = query.test.id
    query.delete()
    return (redirect('ismoktify:test_detail', link))


def unique_test(request, pk):
    test_model = Test.objects.get(id=pk)
    available_easy_questions = list(
        Question.objects.filter(test=test_model).filter(weight=1))
    availible_medium_question = list(
        Question.objects.filter(test=test_model).filter(weight=2))
    availible_hard_question = list(
        Question.objects.filter(test=test_model).filter(weight=3))
    random_easy_questions = random.sample(
        available_easy_questions, test_model.number_of_easy_questions)
    random_medium_questions = random.sample(
        availible_medium_question, test_model.number_of_medium_questions)
    random_hard_questions = random.sample(
        availible_hard_question, test_model.number_of_hard_questions)
    arranged_test = UniqueTest(user=request.user)
    arranged_test.save()
    for question in random_easy_questions:
        arranged_test.questions.add(question)
    for question in random_medium_questions:
        arranged_test.questions.add(question)
    for question in random_hard_questions:
        arranged_test.questions.add(question)
    arranged_test.save()
    return(redirect('ismoktify:quiz_time', arranged_test.id))

def quiz_time(request, pk):
    unique_test = UniqueTest.objects.get(id=pk)
    if request.method == 'POST':
        answers = []
        data = request.POST 
        for question in unique_test.questions.all():
            if str(question.id) in data:
                answers.append(data[str(question.id)])
            else:
                answers.append(None)
        score = answers.count("True") / len(answers) * 10
        result_model = TestResult(user=request.user, score=score)
        result_model.save()
        return render(request, 'ismoktify/result.html', {'score':score})
    else:
        return render(request, 'ismoktify/uniquetest_detail.html', {'uniquetest':unique_test})

class TestResulListView(ListView):
    model = TestResult
    paginate_by = 50
