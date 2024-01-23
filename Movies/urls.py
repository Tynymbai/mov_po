from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from .views import MovieDelete

urlpatterns = [
    path('', views.index, name='index'),
    path('movies/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('movies/<int:pk>/delete/', MovieDelete.as_view(), name='movie-delete'),
    path('add_to_favorite/<int:movie_id>/', views.add_to_favorite, name='add_to_favorite'),
    path('remove_from_favorite/<int:movie_id>/', views.remove_from_favorite, name='remove_from_favorite'),
    path('tmdb/', views.home, name='home'),
    path('tmdb/<int:movie_id>/', views.tmdb_detail, name='tmdb_detail'),
    path('movies/add/', views.add_movie, name='add_movie'),
    path('login/', auth_views.LoginView.as_view(template_name='movies/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('feedback/', views.feedback, name='feedback'),
    path('feedadm/', views.FeedBackView, name='feedadm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
