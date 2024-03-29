from django.urls import path

from . import views


app_name = 'about'
urlpatterns = [
    path('author/', views.AboutAuthorView.as_view(), name='author'),
    path('spec/', views.AboutSpecView.as_view(), name='spec'),
]
