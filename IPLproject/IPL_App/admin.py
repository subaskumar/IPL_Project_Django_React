from django.contrib import admin
from .models import Team,Player

# Register your models here.

class TeamAdmin(admin.ModelAdmin):
    list_display = ['id','teamName','champ_win']
    
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id','playerName','team','price','isPlaying','description']
    
    
admin.site.register(Team,TeamAdmin)
admin.site.register(Player,PlayerAdmin)