from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Category
from .filters import NewsFilter, ArticlesFilter
from .forms import NewsForm, ArticlesForm
from .tasks import send_email_task


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class MNewsList(ListView):
    queryset = Post.objects.filter(section='NW')
    ordering = '-creation_dt'
    template_name = 'm_news.html'
    context_object_name = 'm_news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class SNewsDetail(DetailView):
    queryset = Post.objects.filter(section='NW')
    template_name = 's_news.html'
    context_object_name = 's_news'


class ArticlesList(ListView):
    queryset = Post.objects.filter(section='AR')
    ordering = '-creation_dt'
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ArticlesFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class ArticleDetail(DetailView):
    queryset = Post.objects.filter(section='AR')
    template_name = 'article.html'
    context_object_name = 'article'


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)

    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.section = 'NW'
        post.save()
        send_email_task.delay(post.pk)
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)

    form_class = ArticlesForm
    model = Post
    template_name = 'articles_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.section = 'AR'
        post.save()
        send_email_task.delay(post.pk)
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)

    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    check_section = 'AR'

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.section == 'AR':
            raise Http404
        return super().form_valid(form)


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)

    form_class = ArticlesForm
    model = Post
    template_name = 'articles_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.section == 'NW':
            raise Http404
        return super().form_valid(form)


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)

    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = self.get_object().section
        if post == 'AR':
            raise Http404
        return super().form_valid(form)


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)

    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('articles_list')

    def form_valid(self, form):
        post = self.get_object().section
        if post == 'NW':
            raise Http404
        return super().form_valid(form)


class CategoryList(ListView):
    model = Post
    ordering = '-creation_dt'
    template_name = 'category_list.html'
    context_object_name = 'category_list'
    paginate_by = 10

    def get_queryset(self):
        self.categories = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categories=self.categories).order_by('-creation_dt')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.categories.subscribers.all()
        context['category'] = self.categories
        return context


class CategoriesList(ListView):
    model = Category
    ordering = '-name'
    template_name = 'categories_list.html'
    context_object_name = 'categories_list'


@login_required
def initiate_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = f'Вы успешно подписались на рассылку новых публикаций в категории {category}'

    return render(request, 'subscribe.html', {'category': category, 'message': message})


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    message = f'Вы успешно отписались от категории {category}'

    return render(request, 'unsubscribe.html', {'category': category, 'message': message})
