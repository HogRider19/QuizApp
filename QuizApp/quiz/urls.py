from django.urls import  path
from . import views

urlpatterns = [
    path('course/<int:pk>/', views.courseDetailView.as_view(), name='coursedetail'),
    path('test/<int:pk>/', views.TestDetailView.as_view(), name='testdetail'),
    path('teacherpage/', views.HomeTeacherPage.as_view(), name='teacherpage'),
    path('courseedit/<int:pk>/', views.CourseEditView.as_view(), name='courseedit'),
    path('testedit/<int:pk>/', views.TestEditView.as_view(), name='testedit'),
    path('', views.HomePage.as_view(), name='home'),
]