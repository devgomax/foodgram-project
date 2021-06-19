def get_form_ingredients(request):
    ingredients = {}
    post_body = request.POST
    for key, name in post_body.items():
        if key.startswith('nameIngredient'):
            num = key.split('_')[1]
            ingredients[name] = post_body.get(f'valueIngredient_{num}')
    return ingredients
