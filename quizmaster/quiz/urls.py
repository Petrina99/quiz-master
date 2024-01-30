from django.urls import path
from . import views
from .views import quiz_list, user_profile

app_name = "quiz"

urlpatterns = [
    path('register/', views.register_user, name="register_user"),
    path('login/', views.login_user, name="login_user"),
    path('list/', views.quiz_list, name="quiz_list"),
    path('<int:quiz_id>/', views.detail, name="detail"),
    path('new/', views.create_quiz, name="create_quiz"),
    path('<int:quiz_id>/edit/', views.edit_quiz, name="edit_quiz"),
    path('<int:quiz_id>/delete/', views.delete_quiz, name="delete_quiz"),
    path('<int:quiz_id>/question/new', views.create_question, name="create_question"),
    path('<int:question_id>/question/delete/', views.delete_question, name="delete_question"),
    path('<int:question_id>/question/', views.question_detail, name="question_detail"),
    path('<int:quiz_id>/comments/new/', views.post_comment, name="post_comment"),
    path("<int:comment_id>/comments/delete/", views.delete_comment, name="delete_comment"),
    path("<int:quiz_id>/like/", views.like_quiz, name="like"),
    path("<int:quiz_id>/solve/", views.solve_quiz, name="solve_quiz"),
    path("<int:quiz_id>/solve/result/", views.submit_quiz, name="submit_quiz"),
    path("<int:quiz_id>/solve/results/<int:result_id>/", views.result_quiz, name="result_quiz"),
    path('<int:user_id>/profile/', views.user_profile, name="user_profile"),
]
