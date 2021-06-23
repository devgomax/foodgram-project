def get_form_ingredients(request):
    ingredients = {}
    post_body = request.POST
    for key, name in post_body.items():
        if key.startswith('nameIngredient'):
            num = key.split('_')[1]
            try:
                quantity = int(post_body.get(f'valueIngredient_{num}'))
                if quantity < 1:
                    return 'failed'
            except ValueError:
                return 'failed'
            ingredients[name] = post_body.get(f'valueIngredient_{num}')
    return ingredients
