from django.db.models import Sum
from django.shortcuts import get_object_or_404, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from foodgram.settings import FILE_NAME, CONTENT_TYPE
from users.serializers import RecipeInfoSerializer
from recipes.models import (Recipe, Ingredient, Tag, Favorite, ShoppingList)
from api.serializers import (CreateRecipeSerializer, TagSerializer,
                             IngredientSerializer,
                             GetRecipeSerializer, FavoriteSerializer,
                             ShoppingListSerializer)
from api.permissions import IsAuthorOrReadOnly
from api.filters import CustomFilter, CustomSearchFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """ CRUD операции с рецептом/списком рецептов. """
    queryset = Recipe.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomFilter
    permission_classes = (IsAuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'DELETE'):
            return CreateRecipeSerializer
        return GetRecipeSerializer

    def create_object(self, model, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=self.request.user, recipe=recipe)
        serializer = RecipeInfoSerializer(recipe, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete_object(self, model, pk):
        instance = model.objects.filter(user=self.request.user, recipe__id=pk)
        if instance.exists():
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Запрашиваемый рецепт отсутствует в базе'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        methods=('POST', 'DELETE'),
        detail=True,
        url_path='favorite',
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.create_object(Favorite, request, pk)
        return self.delete_object(Favorite, pk)

    @action(
        methods=('POST', 'DELETE'),
        detail=True,
        url_path='shopping_cart',
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        """ Добавить рецепт в список покупок или удалить из него. """
        if request.method == 'POST':
            return self.create_object(ShoppingList, request, pk)
        return self.delete_object(ShoppingList, pk)

    @action(
        detail=False,
        url_path='download_shopping_cart'
    )
    def download_shopping_cart(self, request):
        ingredients = Recipe.objects.prefetch_related(
            'ingredients', 'recipeingredient'
        ).filter(shoppinglist__user=request.user
        ).order_by('ingredients__name'
        ).values('ingredients__name', 'ingredients__measurement_unit'
        ).annotate(total_sum=Sum('recipeingredient__amount')
        )

        ingredient_txt = [
            (
                f"{item['ingredients__name']}: "
                f"{item['total_sum']}{item['ingredients__measurement_unit']}\n"
            )
            for item in ingredients
        ]
        filename = FILE_NAME
        response = HttpResponse(ingredient_txt, content_type=CONTENT_TYPE)
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ Возвращает тег или список тегов. """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ Возвращает ингредиент или список ингредиентов. """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (CustomSearchFilter, DjangoFilterBackend)
    search_fields = ('^name',)
    pagination_class = None


class FavoriteViewSet(viewsets.ModelViewSet):
    """ Возвращает список избранных рецептов. """
    serializer_class = FavoriteSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('recipe_id'))
        serializer.save(user=self.request.user, recipe=recipe)

    def get_queryset(self):
        user = self.request.user
        return user.favorites.all()


class ShoppingListViewSet(viewsets.ModelViewSet):
    """ Возвращает список покупок. """
    serializer_class = ShoppingListSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('recipe_id'))
        serializer.save(user=self.request.user, recipe=recipe)

    def get_queryset(self):
        user = self.request.user
        return user.shoppinglist.all()
