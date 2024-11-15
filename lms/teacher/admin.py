from django.contrib import admin
from .models import Course, Lesson, Question, StudentEnrollment


admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Question)
admin.site.register(StudentEnrollment)

# Register your models here.
