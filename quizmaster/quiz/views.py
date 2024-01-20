from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from .models import Quiz, Question, Answer

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from django.urls import reverse

from .models import Quiz

# Create your views here.
def home(request):

    return render(request, 'quiz/home.html')

def register_user(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        repeat_password = request.POST['repeat-password']

        does_exist = User.objects.filter(username=username).exists()

        if does_exist is False:
            if password == repeat_password:
                user = User.objects.create_user(username = username, password = password)
               
                user.save()
                # odma nakon registracije logiramo korisnika
                new_user = authenticate(username=username, password=password)
                login(request, new_user)
                return HttpResponseRedirect('/')
            else:
                context = {
                    'error': "Passwords don't match"
                }
                return render(request, 'registration/register.html', context)
        else:
            context = {
                'error': "User with that username already exists"
            }
            return render(request, 'registration/register.html', context)
            
    return render(request, 'registration/register.html')

def login_user(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            context = {
                'error': "Invalid credentials"
            }
        
            return render(request, 'registration/login.html', context)
    
    return render(request, 'registration/login.html')

def quiz_list(request):

    context = {}
    quizzes = Quiz.objects.all()

    context = {
        "quizzes": quizzes
    }
    
    return render(request, 'quiz/list.html', context)

def detail(request, quiz_id):
    context = {}

    quiz = get_object_or_404(Quiz,pk=quiz_id)
    context = {
        "quiz": quiz
    }

    return render(request, 'quiz/detail.html', context)

def create_quiz(request):

    if request.method == "POST" and request.user.is_authenticated:
        title = request.POST["title"]
        
        quiz = Quiz(quiz_name=title, author=request.user)
        quiz.save()
        
        return HttpResponseRedirect(reverse('quiz:edit_quiz', args=[quiz.id, ]))
    
    return render(request, 'quiz/create_quiz.html')

def delete_quiz(request, quiz_id):

    if request.method == "POST" and request.user.is_authenticated:
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        quiz.delete()

        return render(request, 'quiz/home.html')
    
def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    context = {
        "quiz": quiz,
        "range": range(1, 5)
    }
        
    return render(request, 'quiz/edit_quiz.html', context)

def create_question(request, quiz_id):

    quiz = get_object_or_404(Quiz, pk=quiz_id)

    if request.method == "POST" and request.user.is_authenticated:
        title = request.POST["title"]
            
        question = Question(question_text=title, quiz=quiz)
        
        question.save()

        for i in range(1, 5):
            curr_ans = request.POST["answer_" + str(i)]
            if request.POST["radio_button"] == "radio_answer_" + str(i):
                is_corr = True
            else:
                is_corr = False
            answer = Answer(answer_text=curr_ans, is_correct=is_corr, question=question)
            answer.save()

        return HttpResponseRedirect(reverse('quiz:edit_quiz', args=[quiz.id, ]))

def delete_question(request, question_id):

    if request.method == "POST" and request.user.is_authenticated:
        question = get_object_or_404(Question, pk=question_id)
        question.delete()

        return HttpResponseRedirect(reverse('quiz:edit_quiz', args=[question.quiz.id, ]))


