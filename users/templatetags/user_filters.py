from django import template
from recipes.models import Cart, Composition, Favorites

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def addtype(field, css):
    return field.as_widget(attrs={'type': css})


@register.filter
def diff(value, arg):
    return value - arg


@register.filter
def limit_query(query, arg):
    return query[:arg]


@register.filter
def is_purchased_by(recipe, user):
    return Cart.objects.filter(recipe=recipe, user=user).exists()


@register.filter
def is_favorite_for(recipe, user):
    return Favorites.objects.filter(recipe=recipe, user=user).exists()


@register.filter
def get_quantity(ingredient, recipe):
    return Composition.objects.get(
        recipe=recipe, ingredient=ingredient
    ).quantity


@register.filter
def suffix(count):
    """Подбираем верное окончание для слова 'рецепт' в зависимости от
    количества"""
    last_digit = count % 10
    if last_digit == 1:
        return ''
    elif last_digit in range(2,5):
        return 'а'
    else:
        return 'ов'


@register.filter
def addrows(field, css):
    return field.as_widget(attrs={'rows': css})
