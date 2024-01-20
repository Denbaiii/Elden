from django.db import models
from category.models import Category

# Create your models here.

class Place(models.Model):
    title = models.CharField(max_length = 150)
    description = models.TextField()
    event_date = models.DateTimeField(null=True, blank=True)
    max_people = models.IntegerField(null=True, blank=True)
    preview = models.ImageField(upload_to='images/', null=True)
    category = models.ForeignKey(Category, 
                                 on_delete = models.SET_NULL, 
                                 null = True, 
                                 blank = True,
                                 related_name = 'places')
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['created_at']
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return f'{self.category} ----> {self.title}' if self.category else {self.title}
    
class PlaceImage(models.Model):
    title = models.CharField(max_length = 100, blank = True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='place_images/')

    def ganerate_name(self):
        from random import randint
        return 'image' + str(self.id) + str(randint(1, 1_000_000))
    
    def save(self, *args, **kwargs):
        self.title = self.ganerate_name()
        return super(PlaceImage, self).save(*args, **kwargs)

    
    
