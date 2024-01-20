from django.db import models
from django.utils.text import slugify

# My models here.
class Category(models.Model):
    name = models.CharField(max_length = 150)
    slug = models.SlugField(max_length = 50, primary_key= True, blank = True)
    parent = models.ForeignKey('self',
                               on_delete = models.SET_NULL, 
                               null = True, blank = True, 
                               related_name = 'parents')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)   
    
    def __str__(self):
        return f'{self.name} => {self.parent}' if self.parent else f'{self.name}'
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'