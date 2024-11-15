from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm
from .models import User

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        user_type = request.POST.get('user_type') 
        if form.is_valid():
            user = form.save(commit=False)
            # print(form)   
    
            # user= User.objects.create(user=user)
            if user_type == 'admin':
                user.is_admin = True
            elif user_type == 'teacher':
                user.is_teacher = True
            elif user_type == 'student':
                user.is_student = True
            user.save()
            # login(request, user)
            # print()

            return redirect('login')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()  
            login(request, user)   
            if user.is_admin or user.is_superuser: 
                return redirect('/admin/')  
            elif user.is_teacher:
                return redirect('teacher')
            elif user.is_student:
                return redirect('student')  
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('login')




