from django.urls import path
from .views import PostList, ArticlesCreate, ArticleUpdate, ArticlesDelete

urlpatterns = [
    path('', PostList.as_view(), name='news_list'),
    path('create/', ArticlesCreate.as_view(), name='aricles_create'),
    path('<int:pk>/update/', ArticleUpdate.as_view(), name='articles_update'),
    path('<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete')
]