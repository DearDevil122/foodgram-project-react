from django.urls import include, path
from recipes.views import IngredientsViewSet, RecipesViewSet, TagsViewSet
from rest_framework.routers import DefaultRouter

app_name = 'recipes'

v1_router = DefaultRouter()
v1_router.register('ingredients', IngredientsViewSet, basename='ingredients')
v1_router.register('tags', TagsViewSet, basename='tags')
v1_router.register('recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('api/', include(v1_router.urls)),
]
