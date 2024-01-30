from django.urls import path
from . import views
app_name = 'chinese_food_recipes'
urlpatterns = [
    # chinese_food_recipes views
    path('', views.recipes_index_page, name='recipes_index_page'),
    path('home/<str:tag>', views.recipes_home_page, name='recipes_home_page'),
    path('list/<str:category>', views.recipes_list_page, name='recipes_list_page'),
    path('detail/<int:recipe_id>/', views.recipes_detail_page, name='recipes_detail_page'),
    path('add/', views.recipes_add_page, name='recipes_add_page'),
    path('edit/<int:recipe_id>', views.recipes_edit_page, name='recipes_edit_page'),
    path('delete-recipe/<int:recipe_id>', views.delete_recipe, name='delete_recipe'),
    path('search-recipe', views.search_recipe, name='search_recipe'),
    path('collection-icon-clicked/', views.collection_icon_clicked, name='collection_icon_clicked'),
    path('comment-add/<int:recipe_id>', views.comment_add, name='comment_add'),
    path('comment-delete/', views.comment_delete, name='comment_delete'),
    path('comment-edit/<int:comment_id>', views.comment_edit, name='comment_edit')
]
