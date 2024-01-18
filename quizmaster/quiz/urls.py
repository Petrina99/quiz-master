from django.urls import path
from . import views

app_name = "quiz"

urlpatterns = [
    path('register', views.register_user, name="register_user"),
    path('login', views.login_user, name="login_user"),
    path('quiz_list', views.quiz_list, name='quiz_list'),
]
