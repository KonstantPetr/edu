from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import Http404
from .models import Post
from .filters import NewsFilter, ArticlesFilter
from .forms import NewsForm, ArticlesForm


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
        return context


class ArticleDetail(DetailView):
    queryset = Post.objects.filter(section='AR')
    template_name = 'article.html'
    context_object_name = 'article'


class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.section = 'NW'
        return super().form_valid(form)


class ArticleCreate(CreateView):
    form_class = ArticlesForm
    model = Post
    template_name = 'articles_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.section = 'AR'
        return super().form_valid(form)


class NewsUpdate(UpdateView):

    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    check_section = 'AR'

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.section == 'AR':
            raise Http404
        return super().form_valid(form)


class ArticleUpdate(UpdateView):
    form_class = ArticlesForm
    model = Post
    template_name = 'articles_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.section == 'NW':
            raise Http404
        return super().form_valid(form)


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.section == 'AR':
            raise Http404
        return super().form_valid(form)


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('articles_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.section == 'NW':
            raise Http404
        return super().form_valid(form)
