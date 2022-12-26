from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comments
from .forms import PostForm, CommentForm
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


def index_view(request):
    return render(request, 'index.html', {})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:posts_all')
    else:
        form = PostForm()
    return render(request, 'post_new.html', {'form': form})


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super(PostDetailView, self).get_context_data(**kwargs)
    #     context['post_comments'] = self.get_object().
    #     return context


class PostsListView(ListView):
    model = Post
    queryset = Post.objects.filter(published=True)
    paginate_by = 10
    template_name = 'posts_all.html'

    def get_object(self, **kwargs):
        user = self.request.user
        return user

    def get_context_data(self, **kwargs):
        context = super(PostsListView, self).get_context_data(**kwargs)
        context['post_comments'] = Comments.objects.filter(username=self.request.user)
        context['comments_quantity'] = Comments.objects.filter(username=self.request.user).count()
        return context


class CommentAddView(CreateView):
    model = Comments
    form_class = CommentForm
    template_name = 'comment_add.html'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('blog:posts_all')

# def comment_add(request):
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comments = form.save(commit=False)
#             comments.username = request.user
#             comments.post = request.comment_set.id
#             comments.save()
#             return redirect('blog:posts_all')
#     else:
#         form = CommentForm()
#     return render(request, 'comment_add.html', {'form': form})


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'text', 'published']
    template_name = 'post_update.html'
    success_url = reverse_lazy('blog:posts_all')


