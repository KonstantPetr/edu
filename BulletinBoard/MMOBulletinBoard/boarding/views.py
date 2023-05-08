from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Post, Response
from .filters import PostFilter, ResponseFilter
from .forms import PostForm, ResponseForm


class IndexView(TemplateView):
    template_name = 'index.html'


class PostsList(ListView):
    queryset = Post.objects
    ordering = '-cre_dt'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(LoginRequiredMixin, CreateView):

    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.sender = self.request.user
        post.save()
        # send_email_task.delay(post.pk)
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):

    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form):
        form.save(commit=False)
        return super().form_valid(form)


class PostDelete(LoginRequiredMixin, DeleteView):

    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')


class ResponsesList(LoginRequiredMixin, FilterView):
    form_class = ResponseForm
    model = Response
    ordering = '-cre_dt'
    template_name = 'responses.html'
    context_object_name = 'responses'
    filterset_class = ResponseFilter
    paginate_by = 10

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['user'] = self.request.user
        return kwargs


class ResponseCreate(LoginRequiredMixin, CreateView):

    form_class = ResponseForm
    model = Response
    template_name = 'response_edit.html'
    success_url = reverse_lazy('posts_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def form_valid(self, form):
        response = form.save(commit=False)
        pk = self.request.path.split('/')[-2]
        response.sender = self.request.user
        response.post = Post.objects.get(id=pk)
        response.save()
        # send_email_task.delay(post.pk)
        return super().form_valid(form)


@login_required
def response_apply(request, pk):
    response = Response.objects.get(id=pk)
    response.apply()
    messages.success(request, 'Вы приняли отклик!')
    # message = f'Вы приняли отклик!'
    return redirect('responses_list')
    # return render(request, 'response_apply.html', {'message': message})


@login_required
def response_deny(request, pk):
    response = Response.objects.get(id=pk)
    response.delete()
    messages.success(request, 'Вы отклонили отклик, он будет удалён!')

    return redirect('responses_list')
