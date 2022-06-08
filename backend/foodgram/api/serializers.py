from django.core.validators import MinValueValidator
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from drf_base64.fields import Base64ImageField

from foodgram.settings import LIMIT_VALUE
from users.serializers import UserSerializer
from recipes.models import (Recipe, Ingredient, Tag,
                            IngredientRecipe, TagRecipe,
                            Favorite, ShoppingList)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug', 'color')


class ChooseIngredientsForRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class GetIngredientsForRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class CreateRecipeSerializer(serializers.ModelSerializer):
    ingredients = ChooseIngredientsForRecipeSerializer(
        many=True,
        source='recipeingredient'
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    author = serializers.SlugRelatedField(read_only=True, slug_field='email')
    image = Base64ImageField(required=False)
    cooking_time = serializers.IntegerField(
        validators=(
            MinValueValidator(
                limit_value=LIMIT_VALUE,
                message=f'Минимальное время приготовления {LIMIT_VALUE} м.'),
            ),
        )

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'ingredients', 'tags',
                  'image', 'name', 'text', 'cooking_time')

    def to_representation(self, instance):
        serializer = GetRecipeSerializer(
            instance,
            context={'request': self.context.get('request')}
        )
        return serializer.data

    @transaction.atomic()
    def create(self, validated_data):
        current_user = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipeingredient')
        recipe = Recipe.objects.create(author=current_user, **validated_data)
        for tag in tags:
            TagRecipe.objects.create(recipe=recipe, tag=tag)
        for ingredient in ingredients:
            current_ingredient = ingredient.get('id')
            if IngredientRecipe.objects.filter(
                    recipe=recipe,
                    ingredient=current_ingredient).exists():
                raise serializers.ValidationError(
                    'Выбранный ингредиент уже добавлен.')
            amount = ingredient.get('amount')
            IngredientRecipe.objects.create(
                recipe=recipe,
                ingredient=current_ingredient,
                amount=amount
            )
        return recipe

    @transaction.atomic()
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipeingredient')
        instance.tags.clear()
        instance.ingredients.clear()
        IngredientRecipe.objects.filter(recipe=instance).delete()
        TagRecipe.objects.filter(recipe=instance).delete()
        instance = super().update(instance, validated_data)
        for tag in tags:
            TagRecipe.objects.create(recipe=instance, tag=tag)
        for ingredient in ingredients:
            current_ingredient = ingredient.get('id')
            amount = ingredient.get('amount')
            if IngredientRecipe.objects.filter(
                    recipe=instance,
                    ingredient=current_ingredient).exists():
                raise serializers.ValidationError(
                    'Выбранный ингредиент уже добавлен.')
            IngredientRecipe.objects.create(
                recipe=instance,
                ingredient=current_ingredient,
                amount=amount
            )
        instance.save()
        return instance


class GetRecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart'
    )
    tags = TagSerializer(many=True, read_only=True)
    ingredients = GetIngredientsForRecipeSerializer(
        many=True,
        source='recipeingredient',
        read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        if self.context.get('request').user.is_authenticated:
            user = self.context.get('request').user
            return Favorite.objects.filter(
                user=user,
                recipe=obj
            ).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        if self.context.get('request').user.is_authenticated:
            user = self.context.get('request').user
            return ShoppingList.objects.filter(
                user=user,
                recipe=obj
            ).exists()
        return False


class FavoriteSerializer(serializers.ModelSerializer):
    user = UserSerializer
    recipe = GetRecipeSerializer

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        validators = (
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Выбранный рецепт уже в списке избранного.'
            ),
        )


class ShoppingListSerializer(serializers.ModelSerializer):
    user = UserSerializer
    recipe = GetRecipeSerializer

    class Meta:
        model = ShoppingList
        fields = ('user', 'recipe')
        validators = (
            UniqueTogetherValidator(
                queryset=ShoppingList.objects.all(),
                fields=('user', 'recipe'),
                message='Выбранный рецепт уже в списке покупок.'
            ),
        )
