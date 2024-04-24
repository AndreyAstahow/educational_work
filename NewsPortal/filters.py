from django_filters import FilterSet, ModelMultipleChoiceFilter
from .models import Post, Category, POST_CATEGORY

class PostFilter(FilterSet):
    category = ModelMultipleChoiceFilter(
        field_name = 'postcategory__category',
        queryset = Category.objects.all(),
        label = 'Categories',
        conjoined = True
    )

    class Meta:
        model = Post
        fields = {
           'headline': ['icontains'],
           'rating': ['gt'],
           'time_create': ['hour__gt'],
           'post_class': ['exact']
       }