from django import forms
from .models import Movie, Comment, Feedback
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('title', 'description', 'image', 'release', 'time', 'rating', 'language', 'budget', 'cast')
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'image': 'Обложка',
            'release': 'Дата выхода',
            'time': 'Время(минут)',
            'rating': 'Рейтинг',
            'language': 'Язык оригинала',
            'budget': 'Бюджет',
            'cast': 'В главных ролях'
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text': 'Комментарий',
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Обязательно. Введите действительный адрес электронной почты.')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'subject', 'message']
        labels = {
            'name': 'Имя',
            'email': 'Почта',
            'subject': 'Тема',
            'message': 'Сообщение'
        }