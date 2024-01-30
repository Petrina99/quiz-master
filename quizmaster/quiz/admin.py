from django.contrib import admin

from .models import Quiz, Question, Answer, Like, Comment, QuizResult, Choice, Account
# Register your models here.

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(QuizResult)
admin.site.register(Choice)
admin.site.register(Account)