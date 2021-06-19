import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from sorl.thumbnail import delete, default

from users.models import Follow
from .forms import CreationForm
from .models import Cart, Composition, Favorites, Ingredient, Recipe, Tag

User = get_user_model()


def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)


def index(request):
    query_params = request.GET.get('filter')
    context = {}
    if query_params:
        tags_list = query_params.split(',')
        names_list = []
        if 'break' in tags_list:
            names_list.append('Завтрак')
        if 'lunch' in tags_list:
            names_list.append('Обед')
        if 'dinner' in tags_list:
            names_list.append('Ужин')
        recipes = list(set(Recipe.objects.filter(tags__name__in=names_list)))
        context['filters'] = tags_list
    else:
        recipes = Recipe.objects.all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context['page'] = page
    context['paginator'] = paginator
    return render(request, 'index.html', context)


def get_recipe(request, id):
    recipe = Recipe.objects.get(id=id)
    author = recipe.author
    context = {'recipe': recipe, 'follow_exists': False}
    if request.user.is_authenticated:
        if Follow.objects.filter(follower=request.user, author=author).exists():
            context['follow_exists'] = True
    return render(request, 'recipe_page.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    query_params = request.GET.get('filter')
    context = {}
    if query_params:
        tags_list = query_params.split(',')
        names_list = []
        if 'break' in tags_list:
            names_list.append('Завтрак')
        if 'lunch' in tags_list:
            names_list.append('Обед')
        if 'dinner' in tags_list:
            names_list.append('Ужин')
        recipes = list(set(author.recipes.filter(tags__name__in=names_list)))
        context['filters'] = tags_list
    else:
        recipes = author.recipes.all()
    paginator = Paginator(recipes, 6)
    context['author'] = author
    context['paginator'] = paginator
    context['follow_exists'] = False
    if request.user.is_authenticated:
        if Follow.objects.filter(follower=request.user, author=author).exists():
            context['follow_exists'] = True
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context['page'] = page
    return render(request, 'author_page.html', context)


@login_required()
def follows(request):
    authors = User.objects.filter(followings__follower=request.user)
    paginator = Paginator(authors, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,
                  'follows_page.html',
                  {'paginator': paginator,
                   'page': page})


@login_required()
def cart(request):
    cart = Cart.objects.filter(user=request.user)
    return render(request, 'cart_page.html', {'cart': cart})


@login_required()
def purchases(request):
    if request.method == 'POST':
        id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, id=id)
        cart, created = Cart.objects.get_or_create(user=request.user,
                                                   recipe=recipe)
        if not created:
            return JsonResponse({'success': False})
    if request.method == 'GET':
        if not request.user.cart.all():
            return JsonResponse({'success': False})
    return JsonResponse({'success': True})


@login_required()
def delete_purchase(request, id):
    if Cart.objects.filter(recipe__id=id, user=request.user).exists():
        Cart.objects.filter(recipe__id=id, user=request.user).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required()
def new_subscription(request):
    id = json.loads(request.body).get('id')
    if request.user.id == int(id):
        return JsonResponse({'success': False,
                             'error': 'cannot follow yourself'})
    author = User.objects.get(id=id)
    Follow.objects.create(follower=request.user, author=author)
    return JsonResponse({'success': True})


@login_required()
def delete_subscription(request, id):
    author = User.objects.get(id=id)
    if Follow.objects.filter(follower=request.user, author=author).exists():
        Follow.objects.filter(follower=request.user, author=author).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required()
def favorites(request):
    if request.method == 'POST':
        id = json.loads(request.body).get('id')
        recipe = Recipe.objects.get(id=id)
        if Favorites.objects.filter(user=request.user, recipe=recipe).exists():
            return JsonResponse({'success': False,
                                 'error': 'recipe is already in favorites'})
        Favorites.objects.create(user=request.user, recipe=recipe)
        return JsonResponse({'success': True})
    elif request.method == 'GET':
        user = request.user
        query_params = request.GET.get('filter')
        context = {}
        if query_params:
            tags_list = query_params.split(',')
            names_list = []
            if 'break' in tags_list:
                names_list.append('Завтрак')
            if 'lunch' in tags_list:
                names_list.append('Обед')
            if 'dinner' in tags_list:
                names_list.append('Ужин')
            recipes = list(
                set(Recipe.objects.filter(tags__name__in=names_list,
                                          favorites__user=user)))
            context['filters'] = tags_list
        else:
            recipes = Recipe.objects.filter(favorites__user=user)
        paginator = Paginator(recipes, 6)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['paginator'] = paginator
        context['page'] = page
        return render(request, 'favorites_page.html', context)


@login_required()
def delete_favorites(request, id):
    if Favorites.objects.filter(user=request.user, recipe__id=id).exists():
        Favorites.objects.filter(user=request.user, recipe__id=id).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def ingredients(request):
    text = request.GET.get('query')
    ingredients = Ingredient.objects.filter(title__contains=text)
    filtered_list = []
    for ingredient in ingredients:
        filtered_list.append(
            {'title': ingredient.title, 'dimension': ingredient.dimension}
        )
    return JsonResponse(filtered_list, safe=False)


@login_required()
def new_recipe(request):
    form = CreationForm(request.POST or None, files=request.FILES or None)
    context = {}
    if form.is_valid():
        context = save_recipe(request, form)
        if not context:
            return redirect('index')
    context['form'] = form
    return render(request, 'recipe_form.html', context)


@login_required()
def edit_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if request.user != recipe.author:
        return redirect('recipe_page', id=id)
    edit = True
    if request.method != 'POST':
        form = CreationForm(instance=recipe)
        return render(request, 'recipe_form.html', {'form': form,
                                                    'edit': edit,
                                                    'recipe_id': recipe.id})
    form = CreationForm(request.POST, instance=recipe)
    context = {}
    if form.is_valid():
        context = save_recipe(request, form)
        if not context:
            return redirect('index')
    context['form'] = form
    context['edit'] = edit
    context['recipe_id'] = recipe.id
    return render(request, 'recipe_form.html', context)


@login_required()
def delete_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if request.user == recipe.author:
        delete(recipe.image)
        recipe.delete()
        default.kvstore.cleanup()
    return redirect('index')


def get_form_ingredients(request):
    ingredients = {}
    post_body = request.POST
    for key, name in post_body.items():
        if key.startswith('nameIngredient'):
            num = key.split('_')[1]
            ingredients[name] = post_body.get(f'valueIngredient_{num}')
    return ingredients


def save_recipe(request, form):
    recipe = form.save(commit=False)
    recipe.author = request.user
    breakfast = request.POST.get('breakfast')
    lunch = request.POST.get('lunch')
    dinner = request.POST.get('dinner')
    if not breakfast and not lunch and not dinner:
        return {'tags_error': 'Обязательное поле'}
    recipe.save()
    recipe.tags.clear()
    if breakfast:
        recipe.tags.add(Tag.objects.get(name='Завтрак'))
    if lunch:
        recipe.tags.add(Tag.objects.get(name='Обед'))
    if dinner:
        recipe.tags.add(Tag.objects.get(name='Ужин'))
    ingredients = get_form_ingredients(request)
    if not ingredients:
        return {'ings_error': 'Обязательное поле'}
    compositions = []
    Composition.objects.filter(recipe=recipe).delete()
    for title, quantity in ingredients.items():
        ingredient = get_object_or_404(Ingredient, title=title)
        compositions.append(Composition(recipe=recipe,
                                        ingredient=ingredient,
                                        quantity=quantity))
    Composition.objects.bulk_create(compositions)
    form.save_m2m()


@login_required()
def download_cart(request):
    recipes = Recipe.objects.filter(cart__user=request.user)
    total = {}
    content = ''
    for recipe in recipes:
        for comp in recipe.composition_set.all():
            if comp.ingredient.title in total.keys():
                total[comp.ingredient.title] += comp.quantity
            else:
                total[comp.ingredient.title] = comp.quantity
    for key, value in total.items():
        dimension = Ingredient.objects.get(title=key).dimension
        line = f'{key} ({dimension}) - {value}\n'
        content += line
    filename = f'{request.user.username}_cart.txt'
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
