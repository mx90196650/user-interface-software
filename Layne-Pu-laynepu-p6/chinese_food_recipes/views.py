from django.shortcuts import render, redirect
from django.db.models import Q, F, Sum
from .models import Recipes, User, Comments
from django.contrib import messages
from django.http import JsonResponse
from actions.models import Action

# Create your views here.


def recipes_index_page(request):
    hot_recipe_list = Recipes.objects.filter(tags__contains=["hot"]).order_by('-date_posted')
    actions = Action.objects.all().order_by('-created')[:10]
    return render(request, "chinese_food_recipes/recipes/home.html", {"recipes": hot_recipe_list, "tag": "hot", "actions": actions})


def recipes_home_page(request, tag):
    recipe_list = []
    if tag == 'hot':
        recipe_list = Recipes.objects.all().annotate(hot_index=F('shareNum') + F('commentNum')).order_by('-hot_index')[:10]
    elif tag == 'new':
        recipe_list = Recipes.objects.all().order_by('-date_posted')[:10]
    elif tag == 'top':
        recipe_list = Recipes.objects.all().order_by('-rating', '-date_posted')[:10]
    actions = Action.objects.all().order_by('-created')[:10]
    return render(request, "chinese_food_recipes/recipes/home.html", {"recipes": recipe_list, "tag": tag, "actions": actions})


def recipes_list_page(request, category):
    recipe_list = []
    if category[0] == "#":
        searchValue = category[1:]
        recipe_list = Recipes.objects.filter(Q(title__icontains=searchValue) | Q(tags__icontains=[searchValue])).order_by('-date_posted')
    elif category == "your_recipes":
        recipe_list = Recipes.objects.filter(user__username__exact=request.session.get('username'))
    else:
        recipe_list = Recipes.objects.filter(tags__contains=[category]).order_by('-date_posted')
    return render(request, "chinese_food_recipes/recipes/list.html",
                  {"recipes": recipe_list, "category": category})


def recipes_detail_page(request, recipe_id):
    if request.method == "POST":
        user = User.objects.get(username__exact=request.session.get('username'))
        recipe = Recipes.objects.get(id__exact=recipe_id)
        new_comment = Comments(
            user=user,
            recipe=recipe,
            content=request.POST.get('comment-text-field')
        )
        new_comment.save()

        action = Action(
            user=new_comment.user,
            verb="commented on the recipe:",
            target=new_comment.recipe
        )
        action.save()
        messages.success(request, 'You have successfully commented on the recipe: %s' % new_comment.recipe.title)
        return redirect('chinese_food_recipes:recipes_detail_page', recipe_id=new_comment.recipe.id)
    recipe = Recipes.objects.get(id__exact=recipe_id)
    return render(request, "chinese_food_recipes/recipes/detail.html", {"recipe": recipe})


def recipes_add_page(request):
    if not request.session.get("username", False):
        return redirect('chinese_food_recipes:recipes_home_page')
    if request.method == "POST":
        max_id = None
        try:
            max_id = Recipes.objects.latest('id').id
        except Recipes.DoesNotExist:
            pass
        user = User.objects.get(username__exact=request.session.get('username'))
        newRecipe = Recipes(
            id=max_id+1,
            title=request.POST.get('dish-name'),
            description=request.POST.get('introduction'),
            ingredient=request.POST.get('ingredient'),
            instruction=request.POST.get('instruction'),
            user=user
        )
        newRecipe.save()

        action = Action(
            user=user,
            verb="created the new recipe:",
            target=newRecipe
        )
        action.save()

        messages.success(request, 'You have successfully posted the recipe: %s' % newRecipe.title)
        return redirect('chinese_food_recipes:recipes_detail_page', recipe_id=max_id+1)
    return render(request, "chinese_food_recipes/recipes/add.html")


def recipes_edit_page(request, recipe_id):
    if not request.session.get("username", False):
        return redirect('chinese_food_recipes:recipes_home_page')
    if request.method == "POST":
        user = User.objects.get(username__exact=request.session.get('username'))
        recipe = Recipes.objects.get(id__exact=recipe_id)
        recipe.title = request.POST.get('dish-name')
        recipe.description = request.POST.get('introduction')
        recipe.num_of_ser = request.POST.get('number-of-serving')
        recipe.prep_time = request.POST.get('dish-prep-time')
        recipe.cook_time = request.POST.get('cook-time')
        recipe.ingredient = request.POST.get('ingredient')
        recipe.instruction = request.POST.get('instruction')
        recipe.save()

        action = Action(
            user=user,
            verb="edited the recipe:",
            target=recipe
        )
        action.save()

        messages.info(request, 'You have successfully edited the recipe: %s' % recipe.title)
        return redirect('chinese_food_recipes:recipes_detail_page', recipe_id=recipe_id)
    recipe = Recipes.objects.get(id__exact=recipe_id)
    return render(request, "chinese_food_recipes/recipes/edit.html", {"recipe": recipe})


def delete_recipe(request, recipe_id):
    recipe = Recipes.objects.get(id__exact=recipe_id)
    recipeTitle = recipe.title
    user = User.objects.get(username__exact=request.session.get('username'))
    recipe.delete()

    action = Action(
        user=user,
        verb='deleted the recipe: "' + recipeTitle + '"'
    )
    action.save()

    messages.warning(request, 'You have successfully deleted the recipe: %s' % recipeTitle)
    return redirect(request.META.get('HTTP_REFERER'))


def search_recipe(request):
    return redirect('chinese_food_recipes:recipes_list_page', category="#" + request.GET.get('searchValue'))


def collection_icon_clicked(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax and request.method == "POST":
        recipe_id = request.POST.get('recipe_id')
        try:
            recipe = Recipes.objects.get(id__exact=recipe_id)
            author = request.session.get('username')
            action = ""
            if author in recipe.collected_by:
                recipe.collected_by.remove(author)
                action = "collection_removed"
            else:
                recipe.collected_by.append(author)
                action = "collection_saved"
            recipe.save()
            return JsonResponse({'success': 'success', 'action': action}, status=200)
        except Recipes.DoesNotExist:
            return JsonResponse({'error': 'No recipe found with that ID.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax request.'}, status=400)


def comment_add(request, recipe_id):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax and request.method == "POST":
        try:
            user = User.objects.get(username__exact=request.session.get('username'))
            recipe = Recipes.objects.get(id__exact=recipe_id)
            new_comment = Comments(
                user=user,
                recipe=recipe,
                content=request.POST.get('comment-text-field')
            )
            new_comment.save()

            action = Action(
                user=new_comment.user,
                verb="commented on the recipe:",
                target=new_comment.recipe
            )
            action.save()
            # return HttpResponse("<h1>Hello World</h1>")
            return JsonResponse({'success': 'success', 'comment_user': new_comment.user.username, 'comment_content': new_comment.content, 'comment_id': new_comment.id}
                                , status=200)
        except Comments.DoesNotExist:
            return JsonResponse({'error': 'No comment found with that ID.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax request.'}, status=400)


def comment_edit(request, comment_id):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax and request.method == "POST":
        try:
            user = User.objects.get(username__exact=request.session.get('username'))
            comment = Comments.objects.get(id__exact=comment_id)
            comment.content = request.POST.get('edit-comment-field')
            comment.save()
            return JsonResponse({'success': 'success', 'comment_content': comment.content}, status=200)
        except Comments.DoesNotExist:
            return JsonResponse({'error': 'No comment found with that ID.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax request.'}, status=400)


def comment_delete(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax and request.method == "POST":
        comment_id = request.POST.get('comment_id')
        try:
            comment = Comments.objects.get(id__exact=comment_id)
            comment.delete()
            return JsonResponse({'success': 'success'}, status=200)
        except Comments.DoesNotExist:
            return JsonResponse({'error': 'No comment found with that ID.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax request.'}, status=400)

