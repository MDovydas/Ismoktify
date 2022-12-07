from django_quill.fields import QuillField
from django.db import models
from django.conf import settings


class Course(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200)
    content = QuillField()


class QuillPost(models.Model):
    content = QuillField()


class Test(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=180)
    number_of_easy_questions = models.IntegerField()
    number_of_medium_questions = models.IntegerField()
    number_of_hard_questions = models.IntegerField()
    def __str__(self):
        return self.title
    
    
class Question(models.Model):
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, blank=True, null=True)
    content = models.CharField(max_length=180)
    weight = models.IntegerField()
    

    def __str__(self):
        return self.content
    
    
class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, blank=True, null=True)
    content = models.CharField(max_length=180)
    is_true = models.BooleanField()
    
    def __str__(self):
        return self.content
    

class UniqueTest(models.Model):
    questions = models.ManyToManyField(Question)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    

class TestResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.FloatField()
    