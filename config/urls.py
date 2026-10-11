from django.contrib import admin
from django.urls import path
from courses import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("enroll/", views.enroll, name="enroll"),
    path("course/<int:course_id>/", views.course_detail, name="course_detail"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.user_dashboard, name="dashboard"),
]