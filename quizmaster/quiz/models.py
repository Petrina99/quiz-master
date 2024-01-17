from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    quiz_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.quiz_name

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

class Answer(models.Model):
    answer_text = models.CharField(max_length=200)
    is_correct = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer_text

class Comment(models.Model):
    comment_text = models.TextField()
    pub_date = models.DateTimeField("date published")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_text

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f"{self.user.username} likes {self.quiz.quiz_name}"

