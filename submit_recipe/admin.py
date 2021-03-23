from django.contrib import admin
from .models import *
from .forms import *

# Register your models here.
class TagAdmin(admin.ModelAdmin):
  pass

class RecipeAdmin(admin.ModelAdmin):
  pass

class CommentAdmin(admin.ModelAdmin):
  pass

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagAdmin)