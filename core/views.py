from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from django.contrib.auth import authenticate, login, logout
from .forms import StudentForm
from django.db.models import Count, Avg, Min, Max
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import pandas as pd
from django.core.serializers.json import DjangoJSONEncoder
import json

def calendar_view(request):
    students = Student.objects.all()
    birthdays = [
        {
            "name": student.name,
            "date": student.date_of_birth.strftime('%Y-%m-%d')
        }
        for student in students
    ]
    return render(request, "core/calendar.html", {
        "birthdays_json": json.dumps(birthdays, cls=DjangoJSONEncoder)
    })

def upload_excel(request):
    print("working")
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file)

        for _, row in df.iterrows():
            Student.objects.create(
                first_name=row['first_name'],
                middle_name=row.get('middle_name', ''),
                last_name=row['last_name'],
                student_id=row['student_id'],
                year_level=int(row['year_level']),
                email=row['email'],
                date_of_birth=row['date_of_birth'],
                gender=row.get('gender'),
                phone_number=row.get('phone_number', ''),
                current_address=row.get('current_address', ''),
                permanent_address=row.get('permanent_address', ''),
                emergency_contact_name=row.get('emergency_contact_name', ''),
                emergency_contact_phone=row.get('emergency_contact_phone', ''),
                emergency_contact_relation=row.get('emergency_contact_relation', '')
            )
        messages.success(request, "Excel file uploaded successfully!")
        return redirect('student_list')

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
