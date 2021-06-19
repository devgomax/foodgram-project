from django.contrib.auth import get_user_model
from django.db import models
from sorl.thumbnail import ImageField


class Ingredient(models.Model):
    title = models.CharField(verbose_name='Название',
                             max_length=50)
    dimension = models.CharField(verbose_name='Единицы измерения',
                                 max_length=50)

    class Meta:
        ordering = ['title']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.title


class Tag(models.Model):
    class Colors(models.TextChoices):
        ORANGE = 'orange'
        GREEN = 'green'
        PURPLE = 'purple'

    name = models.CharField(verbose_name='Название',
                            max_length=100,
                            unique=True)
    slug = models.SlugField(unique=True)
    color = models.CharField(verbose_name='Цвет',
                             max_length=10,
                             choices=Colors.choices,
                             default=Colors.GREEN)

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(get_user_model(),
                               verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name='recipes')
    title = models.CharField(verbose_name='Название рецепта',
                             max_length=100)
    image = ImageField(verbose_name='Загрузить фото',
                       upload_to='recipes/',
                       help_text='Загрузите изображение')
    description = models.TextField(verbose_name='Описание',
                                   max_length=250,
                                   help_text='Опишите рецепт')
    ingredients = models.ManyToManyField(Ingredient,
                                         verbose_name='Ингредиенты',
                                         through='Composition',
                                         related_name='recipes')
    tags = models.ManyToManyField(Tag,
                                  verbose_name='Теги',
                                  related_name='tags')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления'
    )
    created = models.DateTimeField(verbose_name='Дата публикации',
                                   auto_now_add=True,
                                   db_index=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title


class Composition(models.Model):
    recipe = models.ForeignKey(Recipe,
                               verbose_name='Рецепт',
                               on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient,
                                   verbose_name='Ингредиент',
                                   on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество',
                                                default=1)


class Favorites(models.Model):
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='favorites')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='favorites')
    created = models.DateTimeField(verbose_name='Дата добавления',
                                   auto_now_add=True,
                                   db_index=True)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ['-created']


class Cart(models.Model):
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='cart')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='cart')
    created = models.DateTimeField(verbose_name='Дата добавления',
                                   auto_now_add=True,
                                   db_index=True)

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        ordering = ['-created']
