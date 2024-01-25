from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    quiz_name = models.CharField(max_length=200, blank=False)
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    description = models.TextField(blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.quiz_name
    
    def toggle_like(self, user):
        if self.likes.filter(user=user).count() > 0:
            like = self.likes.filter(user=user)
            like.delete()
        else:
            like = self.likes.create(user=user)
   
class Question(models.Model):
    question_text = models.CharField(max_length=200, blank=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

class Answer(models.Model):
    answer_text = models.CharField(max_length=200, blank=False)
    is_correct = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer_text

class Comment(models.Model):
    comment_text = models.TextField(blank=False)
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_text

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"{self.user.username} likes {self.quiz.quiz_name}"

class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(blank=False)
    correct_answers = models.IntegerField(blank=False)

class Choice(models.Model):
    correct = models.BooleanField()
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    current_quiz = models.ForeignKey(QuizResult, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.question.question_text} in quiz {self.quiz.quiz_name} answered {self.correct}"
