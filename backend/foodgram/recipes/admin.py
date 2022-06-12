from django.contrib import admin

from recipes.models import (Recipe, Ingredient, Tag, Favorite,
                            TagRecipe, IngredientRecipe, ShoppingList
                            )
from users.models import User, Follow


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')
    list_filter = ('user',)
    search_fields = ('following',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    list_filter = ('email', 'username')
    search_fields = ('username',)


class TagRecipeInline(admin.TabularInline):
    model = TagRecipe
    extra = 1


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1


class RecipeAdmin(admin.ModelAdmin):

    def total_in_favorites(self, obj):
        return obj.favorites.count()

    readonly_fields = ('total_in_favorites',)
    list_display = ('name', 'author')
    search_fields = ('author__username', 'author__email', 'name',)
    list_filter = ('tags',)
    empty_value_display = '-empty-'
    inlines = (IngredientRecipeInline, TagRecipeInline)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('measurement_unit',)
    empty_value_display = '-empty-'
    inlines = (IngredientRecipeInline,)


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color')
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-empty-'
    inlines = (TagRecipeInline,)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'user')
    search_fields = ('recipe__name',     'user__username', 'user__email')
    list_filter = ('recipe__tags__name',)
    empty_value_display = '-empty-'


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'user')
    search_fields = ('recipe__name', 'user__username', 'user__email')
    empty_value_display = '-empty-'


class IngredientRecipeAdmin(admin.ModelAdmin):
    search_fields = ('recipe__name', 'ingredient__name')


class TagRecipeAdmin(admin.ModelAdmin):
    search_fields = ('tag__name', 'recipe__name')
    list_filter = ('tag',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(TagRecipe, TagRecipeAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
