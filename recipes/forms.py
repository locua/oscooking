from django.forms import ModelForm, ModelMultipleChoiceField, TextInput, Textarea
from . models import Recipe, Tag
from django import forms

#   title = models.CharField(max_length=200)
#   author = models.CharField(max_length=100)
#   email = models.EmailField(max_length=254, blank=True)
#   date_submitted = models.DateTimeField(auto_now_add=True)
#   tags = models.ManyToManyField('Tag', related_name='recipes', blank=True)
#   description = models.TextField(max_length=200, default=None)
#   ingredients = models.TextField()
#   instructions = models.TextField()
#   link1 = models.URLField(max_length=300, blank=True)
#   link2 = models.URLField(max_length=300, blank=True)
#   visible = models.BooleanField(default=False)

class RecipeForm(forms.Form):
    # class Meta:
        # model = Recipe
        #fields = ['title', 'author', 'ingredients', 'tags' 'instructions', 'link1', 'link2']
        # exclude = ['date_submitted', 'visible']
    title = forms.CharField(
        max_length=200, 
        widget=forms.TextInput(attrs={
            'placeholder':'Recipe title', 
            'class': 'form-control'}
        )
    )
    author = forms.CharField(
        max_length=200, 
        widget=forms.TextInput(attrs={
            'placeholder':'Authors name', 
            'class': 'form-control'}
        )
    )
    email = forms.CharField(
        required=False,
        max_length=200, 
        # label="Email",
        widget=forms.TextInput(attrs={
            'placeholder':'Email (optional)', 
            'class': 'form-control'}
        )
    )
    description = forms.CharField(
        max_length=200, 
        widget=forms.Textarea(attrs={
            'placeholder':'A short description of the recipe. Could include information about its origins or a short anecdote.', 
            'class': 'form-control'}
        )
    )
    ingredients = forms.CharField(
        max_length=200, 
        widget=forms.Textarea(attrs={
            'placeholder':'Ingredient list for the recipe. Please include a quantity and ingredient on each line.',
            'class':'form-control'}
        )
    )
    instructions = forms.CharField(
        max_length=200, 
        widget=forms.Textarea(attrs={
            'placeholder':'Short list of instructions. Each instruction should begin with a number and a period. For example 1.',
            'class':'form-control'}
        )
    )
    tags = ModelMultipleChoiceField (
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    additional_tags=forms.CharField(
        max_length=400,
        required=False,
        label='Additional tags. Seperate with commas <i> i.e </i> <strong> fruit,vegetarian,gluten free</strong>',
        widget=forms.TextInput(attrs={
            'placeholder':'Additional tags, please seperate tags with commas.',
            'class':'form-control'}
        )
    )
