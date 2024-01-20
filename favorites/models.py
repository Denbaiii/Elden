from django.db import models
from django.contrib.auth import get_user_model
from post.models import Place

User = get_user_model()

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='favorites')

    def __str__(self):
        return f"{self.user.username} - {self.place.title}"
