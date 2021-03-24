from django.shortcuts import render
from .forms import RecipeForm
from .models import Recipe, Comment
from django.views import generic
# Create your views here.

class IndexView(generic.ListView):
    """ Recipes index view """
    template_name='recipes/index.html'
    context_object_name='recipe_list'
    def get_queryset(self):
        """Return the published recipes"""
        return Recipe.objects.all()


def detail_view(request, pk):
    pass


def submit_recipe_view(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RecipeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RecipeForm()

    return render(request, 'recipes/submit_recipe.html', {'form': form})

def detail_view(request, pk):
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
    recipe=Recipe.objects.get(pk=pk)
    context = {
        "recipe": recipe,
    }
    return render(request, "recipes/detail.html", context)
