from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _ 
from django.urls import reverse
from django.core.cache import cache


class Author(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts = Post.objects.get.filter(self.id)


class Category(models.Model):
    name = models.CharField(max_length=24, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.name.title()

article = 'article'
news = 'news'

POST_CATEGORY = [
    (article, 'Статья'),
    (news, 'Новость')
]

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_class = models.CharField(max_length=24, choices=POST_CATEGORY, default=article)
    time_create = models.DateTimeField(auto_now_add=True)
    headline = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)
    rating = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -= 1
        self.save()
    
    def prewiew(self):
        return print(self.text[0:123] + '...')
    
    def __str__(self):
        return f'{self.headline.title()}, {self.text}'
    
    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 

class Comment(models.Model):
    rating = models.IntegerField(default=0)
    text = models.TextField(max_length=1000)
    time_create = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -= 1
        self.save()
