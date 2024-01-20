from django.db import models
from post.models import Place
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Comment(models.Model):
    owner = models.ForeignKey(User, related_name = 'comments', on_delete = models.CASCADE)
    place = models.ForeignKey(Place, related_name = 'comments', on_delete = models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.owner} ==> {self.place}'