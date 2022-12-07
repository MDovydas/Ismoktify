from django import forms
from django.forms import ModelForm
from django_quill.forms import QuillFormField
from .models import Course, Article, Test, Question, Answer, UniqueTest


class QuillFieldForm(forms.Form):
    content = QuillFormField()


class ArticleForm(forms.ModelForm):
    template = 'ismoktify/new_article.html'

    class Meta:
        model = Article
        fields = ['course', 'title', 'content']
        template = 'ismoktify/new_article.html'

class CourseForm(forms.ModelForm):
    template = 'ismoktify/new_course.html'
    
    class Meta:
        model = Course
        fields = ['name']
        template = 'ismoktify/new_course.html'
        
class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['course', 'title', 'number_of_easy_questions', 'number_of_medium_questions', 'number_of_hard_questions']
        
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['test', 'content', 'weight']
        labels = {
            'content': 'Question',
            'weight': 'Points / question'
        }    
        widgets = {'test': forms.HiddenInput()}
    
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content', 'is_true']
        labels = {
            'content': 'Answer',
            'is_true': 'Correct answer'
        }
        widgets = {'question': forms.HiddenInput()}

