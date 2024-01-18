from django.urls import path
from . import views
from .views import quiz_list

app_name = "quiz"

urlpatterns = [
    path('register', views.register_user, name="register_user"),
    path('login', views.login_user, name="login_user")
]
