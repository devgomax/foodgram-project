# Generated by Django 3.2.4 on 2021-06-17 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_alter_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composition',
            name='quantity',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='recipes.Composition', to='recipes.Ingredient', verbose_name='Ингредиенты'),
        ),
    ]