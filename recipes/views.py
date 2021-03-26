from django.shortcuts import render
from .forms import RecipeForm
from .models import Recipe, Comment, Tag
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from ipware import get_client_ip
from itertools import chain
# Create your views here.

class IndexView(generic.ListView):
    """ Recipes index view """
    template_name='recipes/index.html'
    # context_object_name='recipe_list'
    
    def get_context_data(self,*args, **kwargs):
        context = super(IndexView, self).get_context_data(*args,**kwargs)
        context['recipe_list'] = Recipe.objects.filter(visible=True)
        context['tags'] = Tag.objects.filter(visible=True)
        return context

    def get_queryset(self):
        """Return the published recipes"""
        return Recipe.objects.filter(visible=True)


def detail_view(request, pk):
    pass

def thanks(request):
    return render(request, 'recipes/thanks.html')


def submit_recipe_view(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RecipeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            tags = form.cleaned_data.get('tags')
            additional_tags = form.cleaned_data["additional_tags"]
            recipe = Recipe(
                title=form.cleaned_data["title"],
                author=form.cleaned_data["author"],
                email=form.cleaned_data["email"],
                description=form.cleaned_data["description"],
                ingredients=form.cleaned_data["ingredients"],
                instructions=form.cleaned_data["instructions"],
            )
            recipe.save()
            # Add additional tags
            split_tags = list(filter(None, additional_tags.split(",")))
            for t in split_tags:
                tag = Tag(name=t) 
                tag.save()
                recipe.tags.add(tag)
            # add existing tags
            for t in tags:
                recipe.tags.add(t)
            recipe.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')
        else:
            print("not valid")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RecipeForm()

    return render(request, 'recipes/submit_recipe.html', {'form': form})

def detail_view(request, recipe_slug):
    """ Shows recipe in full """
    # article = Article.objects.get(pk=pk)
    # form = CommentForm()
    # if request.method == 'POST':
    #     form = CommentForm(request.POST)
    #     if form.is_valid():
    #         comment = Comment(
    #             author=form.cleaned_data["author"],
    #             body=form.cleaned_data["body"],
    #             article=article
    #         )
    #         comment.save()
    # comments = Comment.objects.filter(article=article)
    recipe=Recipe.objects.filter(recipe_slug=recipe_slug)
    ip1 = get_client_ip(request)
    print(ip1)
    context = {
        "recipe": recipe[0],
    }
    return render(request, "recipes/detail.html", context)

def tag_view(request, slug):
    """ view all recipes for a given tag """
    tag = Tag.objects.filter(slug=slug, visible=True)
    recipes=Recipe.objects.filter(
        tags__in=tag,
        visible=True
    )
    context = {
        "tag" : tag[0],
        "recipes_in_tag": recipes,
    }
    return render(request, "recipes/tag.html", context)