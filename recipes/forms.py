from django.forms import ModelForm, ModelMultipleChoiceField
from sorl.thumbnail.fields import ImageFormField

from .models import Ingredient, Recipe, Tag


class RecipeForm(ModelForm):
    image = ImageFormField()
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all(),
                                    to_field_name='slug')

    class Meta:
        model = Recipe
        fields = ['title', 'tags', 'cooking_time', 'description', 'image']
