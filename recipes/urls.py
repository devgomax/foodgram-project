from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/<int:id>', views.get_recipe, name='recipe_page'),
    path('recipes/<int:id>/edit', views.edit_recipe, name='edit_recipe'),
    path('recipes/<int:id>/remove', views.delete_recipe, name='delete_recipe'),
    path('recipes', views.new_recipe, name='new_recipe'),
    path('ingredients', views.ingredients, name='ingredients'),
    path('profiles/<str:username>', views.profile, name='profile'),
    path('cart', views.cart, name='cart_page'),
    path('purchases', views.purchases, name='purchases'),
    path('purchases/<int:id>', views.delete_purchase, name='delete_purchase'),
    path('subscriptions', views.new_subscription, name='new_subscription'),
    path('subscriptions/<int:id>', views.delete_subscription,
         name='delete_subscription'),
    path('favorites', views.favorites, name='favorites'),
    path('favorites/<int:id>', views.delete_favorites,
         name='delete_favorites'),
    path('follows', views.follows, name='follows'),
    path('download', views.download_cart, name='download'),
]
