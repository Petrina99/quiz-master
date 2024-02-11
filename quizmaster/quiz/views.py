from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import Quiz, Question, Answer, Comment, Choice, QuizResult, Account

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from django.urls import reverse

import logging
logger = logging.getLogger('django')
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
                account = Account(user=user, moderator=False)
                user.save()
                account.save()
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
        "quiz": quiz,
        "liked": quiz.liked_by(request.user)
    }

    return render(request, 'quiz/quiz_detail.html', context)

def create_quiz(request):

    if request.method == "POST" and request.user.is_authenticated:
        title = request.POST["title"]
        description = request.POST["description"]
        quiz = Quiz(quiz_name=title, description=description, author=request.user)
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

def question_detail(request, question_id):
    context = {}

    question = get_object_or_404(Question, pk=question_id)
    context = {
        "question": question
    }

    return render(request, 'quiz/question_detail.html', context)


def post_comment(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    if request.method == "POST" and request.user.is_authenticated:
        comment = Comment(
            user = request.user,
            comment_text=request.POST['comment_text'],
            quiz=quiz
        )
        comment.save()

    return HttpResponseRedirect(reverse("quiz:detail", args=[quiz_id,]))

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    quiz = get_object_or_404(Quiz, pk=comment.quiz.id)

    if request.method == "POST" and request.user.is_authenticated:
        comment.delete()

        return HttpResponseRedirect(reverse("quiz:detail", args=[quiz.id, ])) 

def like_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST' and request.user.is_authenticated:
        quiz.toggle_like(request.user)
        
    return HttpResponseRedirect(reverse("quiz:detail", args=[quiz_id,]))

def solve_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    context = {
        "quiz": quiz,
    }

    return render(request, 'quiz/quiz_solve.html', context)

def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    if request.method == 'POST' and request.user.is_authenticated:
        questions = quiz.question_set.all()
        quiz_result = QuizResult(user=request.user, quiz=quiz, score=0, correct_answers=0)
        quiz_result.save()

        for question in questions:
            correct_answer = question.answer_set.get(is_correct=True)
            current_choice = request.POST["radio-" + str(question.id)]
            current_answer = question.answer_set.get(pk=int(current_choice))

            if int(current_choice) == correct_answer.id:
                quiz_result.correct_answers += 1
                choice = Choice(correct=True, quiz=quiz, current_quiz=quiz_result, question=question, answer=current_answer)
                quiz_result.save()
                choice.save()
            else:
                choice = Choice(correct=False, quiz=quiz, current_quiz=quiz_result, question=question, answer=current_answer)
                choice.save()
    
        return HttpResponseRedirect(reverse('quiz:result_quiz', args=[quiz_id, quiz_result.id, ]))
    else:
        return HttpResponseRedirect(reverse('quiz:solve_quiz', args=[quiz_id, ]))
    
def result_quiz(request, quiz_id, result_id):
    
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    result = get_object_or_404(QuizResult, pk=result_id)

    questions = quiz.question_set.all()
    choices = result.choice_set.all()

    questions_count = quiz.question_set.count()
    score = (result.correct_answers / questions_count) * 100

    result.score = round(score, 2)
    result.save()

    content = []
    
    for i in range(questions_count):
        content.append({
            "question": questions[i],
            "choice": choices[i],
            "correct": questions[i].answer_set.get(is_correct=True)
        })

    context = {
        "quiz": quiz,
        "result": result,
        "content": content,
    }

    return render(request, 'quiz/quiz_result.html', context)

def user_profile(request, user_id):
    user_profile = get_object_or_404(User, pk=user_id)
    
    quiz_results = QuizResult.objects.filter(user=user_profile)
    created_quizzes = Quiz.objects.filter(author=user_profile)
    
    total_percentage = 0
    for result in quiz_results:
        total_percentage += result.score
    
    if total_percentage > 0 and quiz_results.count() > 0:
        average_percentage = total_percentage / quiz_results.count()
    else:
        average_percentage = 0

    context = {
        'user_profile': user_profile,
        'quiz_results': quiz_results,
        'average_percentage': round(average_percentage, 2),
        'created_quizzes': created_quizzes
    }

    return render(request, 'quiz/user_profile.html', context)