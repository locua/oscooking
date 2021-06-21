import re
import uuid
import datetime
import random, string

from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify # new

# Create your models here.

def ran_string(n):
  inputset="1234567890"+string.ascii_letters
  return ''.join(random.choice(inputset) for _ in range(n))

class Tag(models.Model):
  """ Tag """
  name = models.CharField(max_length=100)
  visible = models.BooleanField(default=False)
  slug = models.SlugField(unique=True, default=ran_string(18))

  def __str__(self):
    return self.name
  
  def save(self, *args, **kwargs):
    self.slug = slugify(self.name) + ran_string(5) or self.slug
    super().save(*args, **kwargs)

class Recipe(models.Model):
  """ Recipe """
  title = models.CharField(max_length=200)
  author = models.CharField(max_length=100, default="Anonymous")
  email = models.EmailField(max_length=254, blank=True)
  date_submitted = models.DateTimeField(auto_now_add=True)
  tags = models.ManyToManyField('Tag', related_name='recipes', blank=True)
  description = models.TextField(max_length=200, default=None)
  cooking_time = models.IntegerField(default=0)
  prep_time = models.IntegerField(default=0)
  ingredients = models.TextField()
  instructions = models.TextField()
  link1 = models.URLField(max_length=300, blank=True)
  link2 = models.URLField(max_length=300, blank=True)
  visible = models.BooleanField(default=False)
  recipe_slug = models.SlugField(unique=True, default=ran_string(18))
  image = models.ImageField(upload_to='uploads/', blank=True)

  def save(self, *args, **kwargs):
    # create slug from title
    #if len(self.title)>=50:
    mySlug = ran_string(5)+slugify(self.title[:30])+ran_string(5)
    self.recipe_slug =  mySlug or self.recipe_slug 
    #else:
    #  mySlug = ran_string(5)+slugify(self.title)+ran_string(5)
    #  self.recipe_slug =  mySlug or self.recipe_slug 
    # Make any hidden tags visible if Recipe is visible
    if self.visible:
      for t in self.tags.all():
        if t.visible==False:
          t.visible=True
          t.save()
    super().save(*args, **kwargs)


  def delete(self, *args, **kwargs):
    
    storage, path = self.image.storage, self.image.path
    # Delete the instance before the file
    super(Recipe, self).delete(*args, **kwargs)
    # Delete the image after the model
    storage.delete(path)

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
