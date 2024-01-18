from django.urls import path
from . import views

app_name = "quiz"

urlpatterns = [
    path('register/', views.register_user, name="register_user"),
    path('login/', views.login_user, name="login_user"),
    path('create/', views.create_quiz, name="create_quiz"),
    path('<int:quiz_id>/question/new/', views.create_question, name="create_question"),
    path('<int:quiz_id>/question/generate/', views.generate_question, name="generate_question")
]
