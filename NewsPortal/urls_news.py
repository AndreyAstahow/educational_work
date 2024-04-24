from django.urls import path
from django.views.decorators.cache import cache_page

from .views import PostList, PostDetail, NewsCreate, NewsUpdate, NewsDelete, CategoryList
from .views import subscribe, unsubscribe

urlpatterns = [
    path('', PostList.as_view(), name='news_list'),
    path('<int:pk>', PostDetail.as_view(), name='news_detail'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('categories/', CategoryList.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('categories/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
]