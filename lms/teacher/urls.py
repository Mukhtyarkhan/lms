from django.urls import path
from . import views

urlpatterns = [
    path('teacher/', views.teacher, name='teacher'),
    path('courses/create/', views.create_course, name='create_course'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('delete-course/<int:course_id>/', views.delete_course, name='delete_course'),
    path('courses/<int:course_id>/lessons/create/', views.create_lesson, name='create_lesson'),
   
    path('teacher/lesson/<int:course_id>/<int:lesson_id>/', views.lesson_detail, name='teacher_lesson_detail'),
    
    path('lessons/<int:lesson_id>/questions/create/', views.create_question, name='create_question'),
    # path('courses/', views.course_list, name='course_list'),
    # path('courses/<int:course_id>/students/',views.course_students, name='course_students'),
    
    # path('courses/<int:course_id>/students/<int:student_id>/', views.student_detail, name='student_detail'),
    # path('questions/<int:question_id>/submit/', views.submit_answer, name='submit_answer'),
    path('student/lesson/<int:course_id>/<int:lesson_id>/', views.study_lesson, name='student_study_lesson'),
    path('lesson/submit-answer/<int:question_id>/', views.submit_answer, name='submit_answer'),
    path('student/', views.student, name='student'),
    path('assign_student/<int:course_id>/', views.assign_student, name='assign_student'),
    path('view_results/<int:lesson_id>/', views.view_results, name='view_results'),

]