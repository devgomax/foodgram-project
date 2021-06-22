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
    extra = 0
    min_num = 2


@admin.register(models.Tag)
class TagAdmin(ModelAdmin):
    list_display = ('id', 'slug', 'name', 'color')
    list_filter = ('name', 'slug')
    search_fields = ('name', 'slug')
    readonly_fields = ('id',)


@admin.register(models.Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('id', 'title', 'dimension',)
    list_filter = ('dimension',)
    search_fields = ('title',)
    readonly_fields = ('id',)
    inlines = [CompositionInline]


@admin.register(models.Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('id', 'title', 'description', 'author', 'cooking_time',
                    'count_favorites', 'created')
    list_filter = ('cooking_time', 'created',)
    search_fields = ('author', 'title', 'description', 'cooking_time')
    date_hierarchy = 'created'
    list_display_links = ('id', 'title',)
    readonly_fields = ('id', 'created',)
    inlines = [CompositionInline]

    @admin.display(description='Кол-во добавлений в избранное')
    def count_favorites(self, obj):
        return models.Favorites.objects.filter(recipe=obj).count()


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
