from django.shortcuts import render
from .forms import RecipeForm
from .models import Recipe, Comment, Tag
from django.views import generic
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from ipware import get_client_ip
from itertools import chain
from django.db.models import Q
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import re
# Create your views here.

class IndexView(generic.ListView):
    """ Recipes index view """
    template_name='recipes/index.html'
    # context_object_name='recipe_list'
    from django.core.mail import send_mail
    
    def get_context_data(self,*args, **kwargs):
        context = super(IndexView, self).get_context_data(*args,**kwargs)
        context['recipe_list'] = Recipe.objects.filter(visible=True)[:33]
        context['tags'] = Tag.objects.filter(visible=True)[:40]
        return context

    def get_queryset(self):
        """Return the published recipes"""
        return Recipe.objects.filter(visible=True)

class AllTagView(generic.ListView):
    """ All tags view """
    template_name='recipes/all_tags.html'
    # context_object_name='recipe_list'
    from django.core.mail import send_mail
    
    def get_context_data(self,*args, **kwargs):
        context = super(AllTagView, self).get_context_data(*args,**kwargs)
        # context['recipe_list'] = Recipe.objects.filter(visible=True)
        context['tags'] = Tag.objects.filter(visible=True)
        return context

    def get_queryset(self):
        """Return the published recipes"""
        return Recipe.objects.filter(visible=True)

class AllRecipeView(generic.ListView):
    """ All recipes view """
    template_name='recipes/all_recipes.html'
    # context_object_name='recipe_list'
    from django.core.mail import send_mail
    
    def get_context_data(self,*args, **kwargs):
        context = super(AllRecipeView, self).get_context_data(*args,**kwargs)
        context['recipe_list'] = Recipe.objects.filter(visible=True)
        # context['tags'] = Tag.objects.filter(visible=True)
        return context

    def get_queryset(self):
        """Return the published recipes"""
        return Recipe.objects.filter(visible=True)

def donate_view(request):
    return render(request, 'recipes/donate.html')

def donate_thanks_view(request):
    return render(request, 'recipes/donationthanks.html')

def thanks(request):
    return render(request, 'recipes/thanks.html')

def send_recipe_as_email(recipe):
    # Create message
    message = (recipe.title + 
                "\n by " + recipe.author + "\n---DESCRIPTION:-\n"+
                recipe.description + "\n---INGREDIENTS:-\n" + 
                recipe.ingredients + "\n---METHOD:-\n" + 
                recipe.instructions)
    # Send email
    send_mail(
        'OSCooking: New recipe by ' + recipe.author,
        message,
        'contact@opensource.cooking',
        ['contact@opensource.cooking'],
        fail_silently=False,
    )

def convert_to_webp(img):
    i = Image.open(img)
    i = i.convert('RGB')
    thumb_io = BytesIO()
    i.save(thumb_io, format="webp", quality=80)
    # remove file type from ending for saving
    img_name = re.match(r"(^.{1,})\..{1,}$", img.name).group(1)
    # get file from memory and add to model
    file_in_mem = InMemoryUploadedFile(thumb_io, None, img_name+'.webp', \
    'image/webp', thumb_io.tell(), None)
    return file_in_mem   


def submit_recipe_view(request):
    # if this is a POST request we need to process the form data
    errors=None
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RecipeForm(request.POST, request.FILES)
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
                cooking_time=form.cleaned_data["cooking_time"],
                prep_time=form.cleaned_data["prep_time"],
                # image=form.cleaned_data["image"],
            )
            # convert image to webp and store
            if request.FILES.get("image") is not None:
                img = request.FILES.get("image")
                print(img.size) # get size in bytes
                if img.size > 1*1024*1024: # limit upload size to 2mb
                    err_message = """<i><ul>
                    <li> Image is too large </li>
                    <li> Max size 1mb.</li>
                    <li> You could compress it using an online converter...</li>
                    </ul></i>
                    """
                    return render(request, 'recipes/submit_recipe.html', {'form': form, 'errors':err_message})
                recipe.image = convert_to_webp(img)
            send_recipe_as_email(recipe)
            recipe.save()
            # Add additional tags
            split_tags = list(filter(None, additional_tags.split(",")))
            for t in split_tags:
                tag = Tag(name=t.lower()) 
                tag.save()
                recipe.tags.add(tag)
            # add existing tags
            for t in tags:
                recipe.tags.add(t)
            recipe.save()
            # redirect to a new URL:
            if form.cleaned_data["email"]:
                mess = """Thanks for submitting a recipe."""
                send_mail(
                    'OSCooking: New recipe by ' + recipe.author,
                    mess,
                    'contact@opensource.cooking',
                    [form.cleaned_data["email"]],
                    fail_silently=True,
                )


            return HttpResponseRedirect('/thanks/')
        else:
            errors=form.errors
            print(form.errors)
            print("not valid")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RecipeForm()
    if errors is not None:
        return render(request, 'recipes/submit_recipe.html', {'form': form, 'errors':errors})
    else:
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
    # commgoogle analytics how toents = Comment.objects.filter(article=article)
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

class SearchResultsView(generic.ListView):
    model = Recipe
    template_name = 'recipes/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Recipe.objects.filter(
            Q(visible=True),
            Q(description__icontains=query) | 
            Q(ingredients__icontains=query) | 
            Q(instructions__icontains=query) |
            Q(title__icontains=query)
        )
