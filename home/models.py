from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Track(models.Model):
    MUSCLE_GROUP_CHOICES = [
        ("chest", "Chest"),
        ("back", "Back"),
        ("legs", "Legs"),
        ("arms", "Arms"),
        ("shoulders", "Shoulders"),
        ("core", "Core"),
    ]
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    sets=models.IntegerField()
    reps=models.IntegerField()
    weight=models.FloatField()
    muscle_group=models.CharField(max_length=10, choices=MUSCLE_GROUP_CHOICES,default="chest")
    date=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}'
    
class Profile(models.Model):
    ACTIVITY_LEVEL_CHOICES = [
    ("sedentary", "Sedentary (Little or no exercise)"),
    ("light", "Lightly Active (1 to 3 days/week)"),
    ("moderate", "Moderately Active (3 to 5 days/week)"),
    ("active", "Active (6 to 7 days/week)"),
    ("very_active", "Very Active (Intense training / physical job)"),
    ]

    user=models.OneToOneField(User, on_delete=models.CASCADE)
    age=models.PositiveIntegerField()
    height=models.FloatField()
    weight=models.FloatField()
    gender=models.CharField(max_length=6,choices=
                            [("male","Male"),("female","Female")])
    activity_level=models.CharField(max_length=20,choices=ACTIVITY_LEVEL_CHOICES,
                                    default="sedentary")
    
    def __str__(self):
        return f'{self.user.username} Profile'