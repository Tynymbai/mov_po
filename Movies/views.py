from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import DeleteView
from django.contrib.auth.models import User

from .models import Movie, Comment, FavoriteMovie, Feedback
from .forms import MovieForm, CommentForm, SignUpForm, FeedbackForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
import requests
from django.conf import settings

def index(request):
    movies = Movie.objects.all()
    return render(request, 'movies/index.html', {'movies': movies})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    comments = movie.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.movie = movie
            comment.user = request.user
            comment.save()
            return redirect('movie_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'movies/movie_detail.html', {'movie': movie, 'comments': comments, 'form': form})

@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.created_by = request.user
            movie.save()
            return redirect('movie_detail', pk=movie.pk)
    else:
        form = MovieForm()
    return render(request, 'movies/add_movie.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'movies/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('create_user_profile')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    return render(request, 'movies/login.html')


def logout_view(request):
    logout(request)
    return redirect('index')


def home(request):
    api_key = '8b85b10fb95b5595a0aff704f068c2c7'
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=ru-RU&page=1'
    response = requests.get(url)
    data = response.json()
    movies = data['results']

    context = {'movies': movies}
    return render(request, 'movies/home.html', context)


def tmdb_detail(request, movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={settings.TMDB_API_KEY}&language=ru-RU&append_to_response=videos'

    response = requests.get(url)
    data = response.json()

    if 'videos' in data and data['videos'].get('results'):
        trailer_results = [r for r in data['videos']['results'] if r['type'] == 'Trailer']
        if trailer_results:
            trailer_key = trailer_results[0]['key']
            trailer_url = f'https://www.youtube.com/embed/{trailer_key}'
        else:
            trailer_url = None
    else:
        trailer_url = None

    movie = {
        'title': data['title'],
        'overview': data['overview'],
        'poster_path': f"{settings.TMDB_IMG_URL}{data['poster_path']}",
        'release_date': data['release_date'],
        'vote_average': data['vote_average'],
        'runtime': data['runtime'],
        'original_title': data['original_title'],
        'status': data['status'],
        'original_language': data['original_language'],
        'budget': data['budget'],
        'revenue': data['revenue'],
        'cast': [],
    }

    credits_url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={settings.TMDB_API_KEY}&language=ru-RU'
    credits_response = requests.get(credits_url)
    credits_data = credits_response.json()

    for cast in credits_data['cast'][:5]:
        movie['cast'].append(cast['name'])

    context = {
        'movie': movie,
        'trailer_url': trailer_url,
    }
    return render(request, 'movies/tmdb_detail.html', context)


class MovieDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Movie
    success_url = '/'

    def test_func(self):
        movie = self.get_object()
        if self.request.user == movie.created_by:
            return True
        return False


@login_required
def add_to_favorite(request, movie_id):
    try:
        favorite_movie = FavoriteMovie.objects.get(user=request.user, movie_id=movie_id)
        messages.warning(request, 'This movie is already in your favorites!')
    except FavoriteMovie.DoesNotExist:
        favorite_movie = FavoriteMovie(user=request.user, movie_id=movie_id)
        favorite_movie.save()
        messages.success(request, 'Movie added to favorites!')

    return redirect('movie_detail', pk=movie_id)

@login_required
def remove_from_favorite(request, movie_id):
    try:
        favorite_movie = FavoriteMovie.objects.get(user=request.user, movie_id=movie_id)
        favorite_movie.delete()
        messages.success(request, 'Фильм удален из избранных!')
    except FavoriteMovie.DoesNotExist:
        messages.warning(request, 'Данный фильм не является вашим избранным!')

    return redirect('movie_detail', pk=movie_id)


def leaderboard(request):
    users = User.objects.all()
    leaderboard_data = []
    for user in users:
        movie_count = Movie.objects.filter(created_by=user).count()
        leaderboard_data.append({'user': user, 'movie_count': movie_count})
    leaderboard_data.sort(key=lambda x: x['movie_count'], reverse=True)
    return render(request, 'movies/leaderboard.html', {'leaderboard_data': leaderboard_data})


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'movies/thanks.html')
    else:
        form = FeedbackForm()
    return render(request, 'movies/feedback.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def FeedBackView(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'movies/feedadm.html', {'feedbacks': feedbacks})
