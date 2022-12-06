from django.urls import  path
from . import views

urlpatterns = [
    path('course/<int:course_id>/test/<int:pk>/', views.TestDetailView.as_view(), name='testdetail'),
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='coursedetail'),
    path('estimates/', views.EstimatesView.as_view(), name='estimates'),
    path('', views.HomePage.as_view(), name='home'),
]