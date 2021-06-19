from django.forms import ModelForm
from sorl.thumbnail.fields import ImageFormField

from .models import Recipe


class CreationForm(ModelForm):
    image = ImageFormField()

    class Meta:
        model = Recipe
        fields = ['title', 'cooking_time', 'description', 'image']
