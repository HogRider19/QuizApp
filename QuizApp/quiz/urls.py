from django.urls import  path
from . import views

urlpatterns = [
    path('cource/<int:pk>/', views.CourceDetailView.as_view(), name='courcedetail'),
    path('test/<int:pk>/', views.TestDetailView.as_view(), name='testdetail'),
    path('', views.HomePage.as_view(), name='home'),
]