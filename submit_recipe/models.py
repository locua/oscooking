from django.db import models
import datetime
from django.utils import timezone

# Create your models here.

class Tag(models.Model):
  """ Recipe tags """
  name = models.CharField(max_length=100)

  def __str__(self):
    return self.name

class Recipe(models.Model):
  """ Recipe """
  title = models.CharField(max_length=200)
  author = models.CharField(max_length=100)
  date_submitted = models.DateTimeField(auto_now_add=True)
  tags = models.ManyToManyField('Tag', related_name='recipes')
  ingredients = models.TextField()
  instructions = models.TextField()
  link1 = models.URLField(max_length=300)
  link2 = models.URLField(max_length=300)
  visible = models.BooleanField(default=False)

  def __str__(self):
    return self.title
  
class Comment(models.Model):
  """ Comments """
  author = models.CharField(max_length=60)
  body = models.TextField()
  published = models.DateTimeField(auto_now_add=True)
  article = models.ForeignKey('Recipe', on_delete=models.CASCADE)

  def __str__(self):
    return self.author +" said: '" + self.body +"'"
