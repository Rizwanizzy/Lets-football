from django.db import models

# Create your models here.
class Fixtures(models.Model):
    venue = models.CharField(max_length=100)
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=20, default="7:00 PM")
    team1 = models.CharField(max_length=100)
    result1 = models.IntegerField()
    result2 = models.PositiveIntegerField()
    team2 = models.CharField(max_length=100)
    group = models.CharField()
    updated = models.BooleanField(default=False)
    round = models.CharField(max_length=20, choices=[
        ('Round 1', 'Round 1'),
        ('Semi-Finals', 'Semi-Finals'),
        ('Finals', 'Finals'),
    ], default='Round 1')
    
    def __str__(self):
        return f"Fixture between {self.team1} and {self.team2} on {self.date} at {self.time}"