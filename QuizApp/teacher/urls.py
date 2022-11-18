from django.urls import  path
from . import views

urlpatterns = [
    path('courseedit/<int:pk>/', views.CourseEditView.as_view(), name='courseedit'),
    path('testedit/<int:pk>/', views.TestEditView.as_view(), name='testedit'),
    path('questionedit/<int:pk>/', views.QuestionEditView.as_view(), name='questionedit'),
    path('', views.HomeTeacherPage.as_view(), name='teacherpage'),
]