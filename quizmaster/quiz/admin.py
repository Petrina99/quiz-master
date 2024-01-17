from django.contrib import admin

from .models import Quiz, Question, Answer, Like, Comment, UserQuiz
# Register your models here.

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(UserQuiz)