from django.forms import ModelForm, ModelMultipleChoiceField, TextInput, Textarea
from . models import Recipe, Tag
from django import forms

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
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder':'Authors name. Is Anonymous if left blank', 
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
    cooking_time = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder':'Cooking time in minutes'} )
    )
    prep_time = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder':'Preperation time in minutes'} )
    )

    ingredients = forms.CharField(
        # max_length=200, 
        widget=forms.Textarea(attrs={
            'placeholder':'Ingredient list for the recipe. Please include a quantity and ingredient/s on each line.',
            'class':'form-control'}
        )
    )
    instructions = forms.CharField(
        # max_length=200, 
        widget=forms.Textarea(attrs={
            'placeholder':'Short list of instructions. Put each instruction on a new line and it will be numbererd automatically.',
            'class':'form-control'}
        )
    )
    tags = ModelMultipleChoiceField (
        required=False,
        queryset=Tag.objects.filter(visible=True),
        widget=forms.CheckboxSelectMultiple
    )
    additional_tags=forms.CharField(
        max_length=400,
        required=False,
        label='Optional: Additional tags. Seperate with commas <i> i.e </i> <strong> fruit,vegetarian,gluten free</strong>',
        widget=forms.TextInput(attrs={
            'placeholder':'Additional tags, please seperate tags with commas.',
            'class':'form-control'}
        )
    )
    image = forms.ImageField(
        label="Optionally upload an image of the recipe...max size 1mb!",
        required=False
    )

    # from hcaptcha.fields import hCaptchaField
    # hcaptcha_field=hCaptchaField()
