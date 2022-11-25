from django.urls import path
from . import views

urlpatterns = [
    path('start/<int:test_pk>/', views.StartCertificationView.as_view(), name='startcertification'),
    path('decision/<int:question_num>/', views.DecisionView.as_view(), name='decisioncertification'),
    path('finish/', views.FinishCertificationView.as_view(), name='finishcertification'),
    path('finishpage/', views.FinishPageView.as_view(), name='finishpage'),
]