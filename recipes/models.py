from django.db import models
import datetime
import re
from django.utils import timezone
from django.template.defaultfilters import slugify # new

# Create your models here.

class Tag(models.Model):
  """ Tags """
  name = models.CharField(max_length=100)

  def __str__(self):
    return self.name

class Recipe(models.Model):
  """ Recipe """
  title = models.CharField(max_length=200)
  author = models.CharField(max_length=100, default="Anonymous")
  email = models.EmailField(max_length=254, blank=True)
  date_submitted = models.DateTimeField(auto_now_add=True)
  tags = models.ManyToManyField('Tag', related_name='recipes', blank=True)
  description = models.TextField(max_length=200, default=None)
  ingredients = models.TextField()
  instructions = models.TextField()
  link1 = models.URLField(max_length=300, blank=True)
  link2 = models.URLField(max_length=300, blank=True)
  visible = models.BooleanField(default=False)
  recipe_slug = models.SlugField(unique=True, null=True)

  def save(self, *args, **kwargs):
        self.recipe_slug = self.recipe_slug or slugify(self.title)
        super().save(*args, **kwargs)

  def __str__(self):
    return self.title

  def sep_add_tags(self):
    pass

  
class Comment(models.Model):
  """ Comments """
  author = models.CharField(max_length=60)
  body = models.TextField()
  published = models.DateTimeField(auto_now_add=True)
  article = models.ForeignKey('Recipe', on_delete=models.CASCADE)

  def __str__(self):
    return self.author +" said: '" + self.body +"'"
