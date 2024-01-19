from django.urls import path
from . import views
from .views import quiz_list

app_name = "quiz"

urlpatterns = [
    path('register/', views.register_user, name="register_user"),
    path('login/', views.login_user, name="login_user"),
    path('list/', views.quiz_list, name="quiz_list"),
    path('new/', views.create_quiz, name="create_quiz"),
    path('<int:quiz_id>/', views.detail, name="detail")
]
