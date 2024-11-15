from django.shortcuts import render
from teacher.models import Course, Lesson, Question


def admin_home(request):
    
    return render(request, 'home.html')

