from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Course, Enrollment


def home(request):
    courses = Course.objects.all()

    return render(
        request,
        "courses/home.html",
        {"courses": courses}
    )


@login_required
def enroll(request):
    if request.method == "POST":
        student_name = request.user.username
        email = request.user.email
        course = request.POST.get("course")

        # Check if student is already enrolled
        already_enrolled = Enrollment.objects.filter(
            student_name=student_name,
            course=course
        ).exists()

        if already_enrolled:
            return render(
                request,
                "courses/enroll.html",
                {
                    "message": "You are already enrolled in this course!"
                }
            )

        # Create new enrollment
        Enrollment.objects.create(
            student_name=student_name,
            email=email,
            course=course
        )

        return render(
            request,
            "courses/enroll.html",
            {
                "message": "Enrollment successful!"
            }
        )

    return render(request, "courses/enroll.html")


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    return render(
        request,
        "courses/course_detail.html",
        {"course": course}
    )


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("/dashboard/")

        return render(
            request,
            "courses/login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(request, "courses/login.html")


def user_logout(request):
    logout(request)
    return redirect("/")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "courses/register.html",
                {
                    "error": "Username already exists."
                }
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("/login/")

    return render(request, "courses/register.html")


@login_required
def user_dashboard(request):
    enrollments = Enrollment.objects.filter(
        student_name=request.user.username
    )

    return render(
        request,
        "courses/dashboard.html",
        {
            "enrollments": enrollments
        }
    )