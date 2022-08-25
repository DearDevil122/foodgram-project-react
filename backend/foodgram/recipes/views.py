from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from recipes.filters import IngredientFilter, RecipeFilter
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)
from recipes.pagination import CustomPagination
from recipes.permissions import IsAuthorOrAdminOrReadOnly
from recipes.serializers import (IngredientSerializer, RecipesReadSerializer,
                                 RecipesWriteSerializer, TagSerializer)
from recipes.utils import post_delete_favorite_shopping_cart, recipe_formation
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


class TagsViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer
    filter_class = IngredientFilter


class RecipesViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipesReadSerializer
        return RecipesWriteSerializer

    @action(
        detail=False,
        methods=('post', 'delete'),
        url_path=r'(?P<id>[\d]+)/favorite',
        url_name='favorite',
        pagination_class=None,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, id):
        return post_delete_favorite_shopping_cart(
            request.user, request.method, Favorite, id
        )

    @action(
        detail=False,
        methods=('post', 'delete'),
        url_path=r'(?P<id>[\d]+)/shopping_cart',
        url_name='shopping_cart',
        pagination_class=None,
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, id):
        return post_delete_favorite_shopping_cart(
            request.user, request.method, ShoppingCart, id
        )

    @action(
        detail=False,
        methods=('get',),
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
        pagination_class=None,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = IngredientRecipe.objects.filter(
            recipe__shopping_carts__user=user
        ).order_by(
            'ingredient__name'
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit',
        ).annotate(sum_amount=Sum('amount'))
        shopping_cart = recipe_formation(ingredients)
        filename = 'shopping_cart.txt'
        response = HttpResponse(shopping_cart, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


#        filename = 'shopping_cart.pdf'
#        response = FileResponse(shopping_cart, content_type='application/pdf')
#        response['Content-Disposition'] = f'attachment; filename={filename}'
#        return FileResponse(
#            shopping_cart,
#            as_attachment=True,
#            filename='shopping_cart.pdf'
#        )
