from django.contrib import admin
from movie.models import Movie

# Register your models here.

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('m_id','m_title','m_genre','m_runtime','m_opendate','m_class','m_director','m_actor', 'm_scenario')