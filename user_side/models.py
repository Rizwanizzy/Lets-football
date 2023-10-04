from django.db import models
from authentication.models import CustomUser

# Create your models here.
class TeamMembers(models.Model):
    ROLE_CHOICES = (
        ('goal_keeper', 'Goal Keeper'),
        ('defender', 'Defender'),
        ('midfielder', 'Midfielder'),
        ('forward', 'Forward'),
    )

    name = models.CharField(max_length=100)
    number = models.IntegerField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='team_member')

    def __str__(self):
        return self.name