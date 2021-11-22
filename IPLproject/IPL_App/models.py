from django.db import models

# Create your models here.


def upload_cover_to(instance,filename):
	return f'coverImage/{instance.teamName}/{filename}'


class Team(models.Model):
    teamName = models.CharField(max_length=200, unique=True,blank=False)
    icon = models.ImageField(upload_to = upload_cover_to, null=True,blank=True)
    champ_win = models.IntegerField()
    
    def __str__(self):
        return self.teamName
    
def upload_profile_to(instance,filename):
	return f'Player_picture/{instance.playerName}/{filename}'
    
class Player(models.Model):
    Role = (('batsman', 'Batsman'), ('bowler', 'Bowler'), ('Allrounder', 'Allrounder'))
    playerName = models.CharField(max_length=200, blank=False)
    picture = models.ImageField(upload_to = upload_profile_to, null=False)
    team = models.ForeignKey(Team,related_name="player" , to_field="teamName", db_column="team",null=True, blank=True, on_delete=models.CASCADE)
    price = models.IntegerField()
    isPlaying = models.BooleanField(default=False)
    description = models.CharField(max_length=100, choices=Role, default='Allrounder')
    
    class Meta:
        ordering = ['-price']
    
    def __str__(self):
        return self.playerName
    