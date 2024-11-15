from django.db import models
from auth_app.models import User

class Course(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    teacher=models.ForeignKey(User, on_delete=models.CASCADE,related_name='courses', limit_choices_to={'is_teacher': True})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    
class Lesson(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    course=models.ForeignKey(Course, on_delete=models.CASCADE,related_name='lessons')
    
    
class Question(models.Model):
    QUESTION_TYPES = [
        ('fill_in_the_blank', 'Fill in the Blank'),
        ('true_false', 'True/False'),
        ('multiple_choice', 'Multiple Choice'),
    ]
        
    text = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='fill_in_the_blank')
    correct_answer = models.CharField(max_length=200)
       

class StudentEnrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    date_enrolled = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    
class StudentAnswer(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)
    score = models.IntegerField(default=0)
    date_submitted = models.DateTimeField(auto_now_add=True)

    


