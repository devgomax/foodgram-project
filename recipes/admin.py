from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

from . import models

admin.site.empty_value_display = '-пусто-'


class ModelAdmin(AdminImageMixin, admin.ModelAdmin):
    pass


class TabularInline(AdminImageMixin, admin.TabularInline):
    pass


class CompositionInline(TabularInline):
    model = models.Composition
    extra = 1


@admin.register(models.Tag)
class TagAdmin(ModelAdmin):
    list_display = ('id', 'name', 'color')
    list_filter = ('name',)
    search_fields = ('name',)
    readonly_fields = ('id',)


@admin.register(models.Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('id', 'title', 'dimension',)
    list_filter = ('title',)
    search_fields = ('title',)
    readonly_fields = ('id',)
    inlines = [CompositionInline]


@admin.register(models.Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('id', 'title', 'description', 'author', 'cooking_time',
                    'created')
    list_filter = ('author', 'title', 'cooking_time', 'created',)
    search_fields = ('author', 'title', 'description', 'cooking_time')
    date_hierarchy = 'created'
    list_display_links = ('title',)
    readonly_fields = ('id', 'created',)
    inlines = [CompositionInline]


@admin.register(models.Favorites)
class FavoritesAdmin(ModelAdmin):
    list_filter = ('user', 'recipe', 'created',)
    search_fields = ('user', 'recipe',)
    date_hierarchy = 'created'
    readonly_fields = ('id', 'created',)


@admin.register(models.Cart)
class CartAdmin(ModelAdmin):
    list_filter = ('user', 'recipe', 'created',)
    search_fields = ('user', 'recipe',)
    date_hierarchy = 'created'
    readonly_fields = ('id', 'created',)
