from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import CustomUserViewSet
from api.views import (RecipeViewSet, TagViewSet, IngredientViewSet,
                       FavoriteViewSet, ShoppingListViewSet)


v1_router = DefaultRouter()

v1_router.register('users', CustomUserViewSet, basename='follow')
v1_router.register('recipes', RecipeViewSet)
v1_router.register('tags', TagViewSet)
v1_router.register('ingredients', IngredientViewSet)

v1_router.register('favorites', FavoriteViewSet, basename='favorites')
v1_router.register('shopping_cart', ShoppingListViewSet, basename='shopping_cart')


urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
