from django.shortcuts import render
from django.views import View
from django.views import generic
from .models import Cource, Test


class HomePage(generic.ListView):
    model = Cource
    template_name = 'quiz/home.html'
    context_object_name = 'cources'

    def get_queryset(self):
        return self.request.user.profile.group.cources.all()

class CourceDetailView(generic.DetailView):
    model = Cource
    template_name = 'quiz/courcedetail.html'
    context_object_name = 'cource'

class TestDetailView(generic.DetailView):
    model = Test
    template_name = 'quiz/testdetail.html'
    context_object_name = 'test'



