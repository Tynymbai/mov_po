from django.contrib import admin
from .models import Movie, Comment, FavoriteMovie, UserProfile, Feedback

# Register your models here.

admin.site.register(Movie)
admin.site.register(Comment)
admin.site.register(FavoriteMovie)
admin.site.register(UserProfile)
admin.site.register(Feedback)
