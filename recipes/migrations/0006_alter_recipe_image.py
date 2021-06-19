# Generated by Django 3.2.4 on 2021-06-07 17:53

from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_alter_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=sorl.thumbnail.fields.ImageField(help_text='Загрузите изображение', upload_to='media/recipes/', verbose_name='Загрузить фото'),
        ),
    ]
