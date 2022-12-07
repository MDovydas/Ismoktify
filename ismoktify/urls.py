from django.urls import path, include
from . import views
from .views import ArticleCreateView, CoursesListView, CourseCreateView, TestCreateView, TestDetailView, QuestionDetailView, TestResulListView
app_name = 'ismoktify'
urlpatterns = [
    path('', views.index, name='index'),
    path('newarticle/', ArticleCreateView.as_view(), name='new_article'),
    path('courses/', CoursesListView.as_view(), name='course_list'),
    path('courses/<str:course_name>', views.course_view, name='course_detail'),
    path('courses/<str:course_name>/<int:article_id>', views.article_view, name='article_detail'),
    path('courses/<str:course_name>/<int:article_id>/edit', views.article_edit_view, name='article_edit'),
    path('new_course', CourseCreateView.as_view(), name='new_course'),
    path('courses/<str:course_name>/new_test/', TestCreateView.as_view(), name='new_test'),
    path('new_test/<int:pk>', TestDetailView.as_view(), name='test_detail'),
    path('new_question/<int:pk>', QuestionDetailView.as_view(), name='question_detail'),
    path('delete_answer/<int:pk>', views.answer_delete, name='answer_delete'),
    path('delete_question/<int:pk>', views.question_delete, name='question_delete'),
    path('test_generator/<int:pk>', views.unique_test, name='test_generator'),
    path('quiz_time/<int:pk>', views.quiz_time, name='quiz_time'),
    path('teacher', TestResulListView.as_view(), name='teacher_list'),
]