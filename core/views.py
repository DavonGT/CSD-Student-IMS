from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from django.contrib.auth import authenticate, login, logout
from .forms import StudentForm
from django.db.models import Count, Avg, Min, Max
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Accounts
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']
        if password != password1:
            messages.error(request, "Passwords didn't match!")
            return render(request, 'core/register')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Registered successfully.')
            return redirect('login')
    return render(request, 'core/register.html')

def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'core/login.html')

def logoutView(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    total_students = Student.objects.count()


    # Gender distribution
    gender_counts = Student.objects.values('gender').annotate(count=Count('gender'))
    gender_data = {
        'Male': 0,
        'Female': 0,
        'Other': 0,
        'Unspecified': 0
    }
    for item in gender_counts:
        key = dict(Student.GENDER_CHOICES).get(item['gender'], 'Unspecified')
        gender_data[key] = item['count']

    # Students per year level
    year_level_data = Student.objects.values('year_level').annotate(count=Count('year_level')).order_by('year_level')

    # Age statistics
    from datetime import date
    def calculate_age(dob):
        today = date.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    ages = [calculate_age(student.date_of_birth) for student in Student.objects.all() if student.date_of_birth]
    average_age = sum(ages) / len(ages) if ages else 0
    min_age = min(ages) if ages else 0
    max_age = max(ages) if ages else 0

    context = {
        'total_students': total_students,
        'gender_data': gender_data,
        'year_level_data': year_level_data,
        'average_age': round(average_age, 1),
        'min_age': min_age,
        'max_age': max_age,
    }

    return render(request, 'core/dashboard.html', context)

def student_info(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'core/student_other_info.html', {'student': student})

@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'core/student_list.html', {'students': students})

@login_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'core/student_form.html', {'form': form})

@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'core/student_form.html', {'form': form})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'core/student_confirm_delete.html', {'student': student})
