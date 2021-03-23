from django.forms import ModelForm
from . models import Recipe

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        #fields = ['title', 'author', 'ingredients', 'tags' 'instructions', 'link1', 'link2']
        exclude = ['date_submitted', 'visible']

