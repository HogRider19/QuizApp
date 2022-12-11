from django.urls import  path
from . import views

urlpatterns = [
    path('courseedit/<int:course_id>/testedit/<int:test_id>/questionedit/<int:pk>/',
                                views.QuestionEditView.as_view(), name='questionedit'),
    path('courseedit/<int:course_id>/testedit/<int:pk>/',
                                views.TestEditView.as_view(), name='testedit'),
    path('courseedit/<int:pk>/', 
                                views.CourseEditView.as_view(), name='courseedit'),

    path('course/<int:course_id>/test/<int:test_id>/createquestion/',
                                views.CreateQuestionView.as_view(), name='createquestion'),
    path('course/<int:course_id>/createtest/',
                                views.CreateTestView.as_view(), name='createtest'),
    path('question/<int:question_id>/createanswer/',
                                views.CreateAnswerView.as_view(), name='createanswer'),

    path('deletetest/<int:pk>/', views.DeleteTestView.as_view(), name='deletetest'),
    path('deletequestion/<int:pk>/', views.DeleteQuestionView.as_view(), name='deletequestion'),
    path('deleteanswer/<int:pk>/', views.DeleteAnswerView.as_view(), name='deleteanswer'),

    path('', views.HomeTeacherPage.as_view(), name='teacherpage'),
]