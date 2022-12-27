from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comments
from django.contrib.auth.models import User
from .forms import PostForm, CommentForm
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.core.mail import send_mail


def index_view(request):
    return render(request, 'index.html', {})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published_date = timezone.now()
            post.save()
            send_mail('New post', 'New post was added', 'no_reply@somecompany.com', ['admin_email@somecompany.com'])
            return redirect('blog:posts_all')
    else:
        form = PostForm()
    return render(request, 'post_new.html', {'form': form})


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        post = self.get_object()
        context['comment'] = post.comments_set.filter(published=True).all()
        return context


class PostsListView(ListView):
    model = Post
    fields = ['title', 'text']
    queryset = Post.objects.filter(published=True)
    paginate_by = 10
    template_name = 'posts_all.html'

    def get_object(self, **kwargs):
        user = self.request.user
        return user

    # def get_context_data(self, **kwargs):
    #     context = super(PostsListView, self).get_context_data(**kwargs)
    #     context['post_comments'] = Comments.objects.filter(username=self.request.user)
    #     context['comments_quantity'] = Comments.objects.filter(username=self.request.user).count()
    #     return context

    # send_mail('New comment', 'New comment was added', 'no_reply@somecompany.com', ['admin_email@somecompany.com'])

    # link = get_current_site(request).domain
    # sent_to = 'fsljd@fsl.com'
    # send_mail('New comment', f'Hey, You received new comment to your post! Go to the link to check it {link}',
    #           'no_reply@somecompany.com', [sent_to])

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


class LoginUserPostsAllView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 10
    template_name = 'user_posts.html'

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

    def get_object(self, **kwargs):
        user = self.request.user
        return user

    def get_context_data(self, **kwargs):
        context = super(LoginUserPostsAllView, self).get_context_data(**kwargs)
        context['post_comments'] = Comments.objects.filter(username=self.request.user)
        context['comments_quantity'] = Comments.objects.filter(username=self.request.user).count()
        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'text', 'published']
    template_name = 'post_update.html'
    success_url = reverse_lazy('blog:user_posts')

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class CommentAddView(CreateView):
    model = Comments
    form_class = CommentForm
    template_name = 'comment_add.html'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    success_url = reverse_lazy('blog:posts_all')
