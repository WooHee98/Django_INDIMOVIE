from django.contrib import admin
from reservation.models import Movietime, Screentheater, Seat

# Register your models here.

@admin.register(Movietime)
class MovietimeAdmin(admin.ModelAdmin):
    list_display = ('mt_id','m_id','st_id','mt_day','mt_time')

@admin.register(Screentheater)
class ScreentheaterAdmin(admin.ModelAdmin):
    list_display = ('st_id', 't_id', 'st_name')

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('mt_id', 's_name', 's_reserved', 'u_id')

