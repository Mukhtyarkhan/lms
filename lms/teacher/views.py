from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from auth_app.models import User
from .models import Course, Lesson, Question, StudentEnrollment, StudentAnswer
from django.http import JsonResponse
import json



@login_required
@user_passes_test(lambda u: u.is_teacher)
def teacher(request):
    teacher_courses = Course.objects.filter(teacher=request.user)
    data = {
        'courses': teacher_courses
    }
    return render(request, 'teacher/teacher.html', data)

@login_required
@user_passes_test(lambda u: u.is_teacher)
def create_course(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        course = Course.objects.create(
            name=name,
            description=description,
            teacher=request.user
        )
        course_data = {
            'id': course.id,
            'name': course.name,
            'description': course.description,
            'teacher': course.teacher.username
        }
        return JsonResponse({'course': course_data})
    return render(request, 'teacher/teacher.html')




def delete_course(request, course_id):
    print(course_id)
    if request.method == 'POST':
        course = Course.objects.get(id=course_id)
        course.delete()
        return JsonResponse({'success': True})
        
    

@login_required
@user_passes_test(lambda u: u.is_teacher)
def course_detail(request, course_id):
    course =Course.objects.get(id=course_id)
    lessons = course.lessons.all()
    courses = Course.objects.filter(teacher=request.user)  
    
    context = {
        'course': course,
        'lessons': lessons,
        'courses': courses,
    }
    return render(request, 'teacher/course_detail.html', context)


@login_required
@user_passes_test(lambda u: u.is_teacher)
def create_lesson(request, course_id):
    course = Course.objects.get(id=course_id, teacher=request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        lesson = Lesson.objects.create(
            name=name,
            description=description,
            course=course
        )
        lesson.save()
        return JsonResponse({'lesson_id': lesson.id, 'lesson_name': lesson.name, 'course_id': course.id})
    return render(request, 'teacher/lesson.html', {'course': course})

@login_required
@user_passes_test(lambda u: u.is_teacher)
def lesson_detail(request, course_id, lesson_id):
    course = Course.objects.get(id=course_id, teacher=request.user)
    lesson = Lesson.objects.get(id=lesson_id, course=course)
    questions = Question.objects.filter(lesson=lesson)
    question_types = Question.QUESTION_TYPES 
    data = {
        'course': course,
        'lesson': lesson,
        'questions': questions,
        'question_types': question_types,  
    }
    return render(request, 'teacher/lesson.html', data)



@login_required
@user_passes_test(lambda u: u.is_teacher)
def create_question(request, lesson_id):
    lesson =Lesson.objects.get(id=lesson_id, course__teacher=request.user)
    question = Question.objects.create(
    lesson=lesson,
    text=request.POST.get('text'),
    question_type=request.POST.get('question_type'),
    correct_answer=request.POST.get('correct_answer'))
    return JsonResponse({
    'question': {
    'id': question.id,
    'text': question.text,
    'type': question.get_question_type_display(),
    'correct_answer': question.correct_answer
    }
    })
    
    

@login_required
@user_passes_test(lambda u: u.is_teacher)
def assign_student(request, course_id):
    course = Course.objects.get(id=course_id, teacher=request.user)
    all_students = User.objects.filter(is_student=True)
    enrolled_students = User.objects.filter(
        enrollments__course=course,
        is_student=True
    )
    
    available_students = User.objects.filter(
        is_student=True
    ).exclude(
        enrollments__course=course
    )
    
    if request.method == 'POST':
        selected_student_ids = request.POST.getlist('students')
        # print(f"Selected student IDs: {selected_student_ids}")
        for student_id in selected_student_ids:
            StudentEnrollment.objects.create(
                student_id=student_id,
                course=course
            )
        
        return redirect('course_detail', course_id=course.id)
    
    data = {
        'course': course,
        'all_students': all_students,
        'enrolled_students': enrolled_students,
        'available_students': available_students
    }
    
    return render(request, 'teacher/assign_student.html', data)

@login_required
@user_passes_test(lambda u: u.is_teacher)
def view_results(request, lesson_id):
    lesson =Lesson.objects.get(id=lesson_id, course__teacher=request.user)
    enrolled_students = User.objects.filter(
        enrollments__course=lesson.course,
        enrollments__is_active=True
    )
    student_results = {}
    
    for student in enrolled_students:
        answers = StudentAnswer.objects.filter(student=student, question__lesson=lesson)
        total_questions = lesson.questions.count()
        answered_questions = answers.count()
        correct_answers = answers.filter(score__gt=0).count()
        if answered_questions > 0:
            score_percentage = (correct_answers / total_questions) * 100
        else:
            score_percentage = 0
    
        student_results[student] = {
            'answers': answers,
            'total_questions': total_questions,
            'answered_questions': answered_questions,
            'correct_answers': correct_answers,
            'score_percentage': score_percentage,
        }
  
    
    data = {
        'lesson': lesson,
        'student_results': student_results,
    }
    return render(request, 'teacher/results.html', data)

@login_required
def student(request):
        enrollments = StudentEnrollment.objects.filter(student=request.user)
        # courses = []
        # for enrollment in enrollments:
        #    courses.append(enrollment.course)
        
        courses = [enrollment.course for enrollment in enrollments]
        data = {
            'courses': courses,
            'enrollments': enrollments,  
        }
        return render(request, 'student/student.html', data)



@login_required
@user_passes_test(lambda u: u.is_student)
def study_lesson(request, course_id, lesson_id):
    course =Course.objects.get(id=course_id)
    lesson = Lesson.objects.get(id=lesson_id, course=course)
    questions = lesson.questions.all()
    
    data = {
        'course': course,
        'lesson': lesson,
        'questions': questions,
    }
    return render(request, 'student/lesson_detail.html', data)

@login_required
def submit_answer(request, question_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        answer = data.get('answer')
        question =Question.objects.get(id=question_id)
        score = 10 if answer == question.correct_answer else 0
        StudentAnswer.objects.create(
            student=request.user,
            question=question,
            answer=answer,
            score=score
        )
        return JsonResponse({
            'score': score,
            'answer': answer
        })

    

    

    
    