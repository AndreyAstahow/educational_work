import pytz

from django.views.generic import (
        ListView, DetailView, CreateView, DeleteView, UpdateView, View
    )
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.cache import cache
from django.utils import timezone
from django.utils.translation import gettext as _ #!!!!
from django.http import HttpResponse

from .models import Post, Category
from .filters import  PostFilter
from .forms import PostForm
from .tasks import new_post_send_email

class PostList(ListView):
    model = Post
    ordering = 'time_create'
    template_name = 'flatpages/news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
       queryset = super().get_queryset()
       self.filterset = PostFilter(self.request.GET, queryset)
       return self.filterset.qs
    
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['filterset'] = self.filterset
       context['current_time'] = timezone.localtime(timezone.now())
       context['timezones'] = pytz.common_timezones
       return context
    
    def post(self, request, *args, **kwargs):
        if self.request.method == 'POST':
            request.session['django_timezone'] = request.POST['timezone']
        return redirect('news_list')

class PostDetail(DetailView):
    model = Post
    ordering = 'author_id'
    template_name = 'flatpages/news_split.html'
    context_object_name = 'news'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('NewsPortal.add_post')
    form_class = PostForm
    model = Post
    template_name = 'flatpages/news_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_class = 'news'
        news.save()
        new_post_send_email.delay(form.instance.pk)
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsPortal.change_post')
    form_class = PostForm
    model = Post
    template_name = 'flatpages/news_edit.html'

class NewsDelete(DeleteView):
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('news_list')

class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('NewsPortal.add_post')
    form_class = PostForm
    model = Post
    template_name = 'flatpages/articles_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_class = 'article'
        news.save()
        new_post_send_email.delay(form.instance.pk)
        return super().form_valid(form)
    
class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsPortal.change_post')
    form_class = PostForm
    model = Post
    template_name = 'flatpages/articles_edit.html'

class ArticlesDelete(DeleteView):
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('news_list')

class CategoryList(ListView):
    model = Category
    template_name = 'flatpages/category.html'
    ordering = 'id'
    context_object_name = 'category'

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    category.subscribers.add(user)
    return redirect('category_list')

@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    category.subscribers.remove(user)
    return redirect('category_list')
