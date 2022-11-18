from django.urls import  path
from . import views

urlpatterns = [
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='coursedetail'),
    path('test/<int:pk>/', views.TestDetailView.as_view(), name='testdetail'),
    path('', views.HomePage.as_view(), name='home'),
]