from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comments
from django.contrib.auth.models import User
from .forms import PostForm, CommentForm
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.core.mail import send_mail
from .forms import ContactUsForm
from django.core.mail import send_mail
from .tasks import django_send_mail
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


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


@method_decorator(cache_page(10), 'dispatch')
class PostsListView(ListView):
    model = Post
    fields = ['title', 'text']
    queryset = Post.objects.filter(published=True)
    paginate_by = 10
    template_name = 'posts_all.html'

    def get_object(self, **kwargs):
        user = self.request.user
        return user


class LoginUserPostsAllView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 10
    template_name = 'user_posts.html'

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

    def get_object(self, **kwargs):
        user = self.request.user
        return user


class UserPostDetailView(DetailView):
    model = Post
    template_name = 'user_post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(UserPostDetailView, self).get_context_data(**kwargs)
        post = self.get_object()
        context['comment'] = post.comments_set.filter(published=True).all()
        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'text', 'published']
    template_name = 'post_update.html'
    success_url = reverse_lazy('blog:user_posts')

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('blog:user_posts')
    login_url = reverse_lazy('user_management:login')


class CommentAddView(CreateView):
    model = Comments
    form_class = CommentForm
    template_name = 'comment_add.html'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        send_mail('New comment', 'New comment was added', 'no_reply@somecompany.com', ['admin@somecompany.com'])
        return super().form_valid(form)
    success_url = reverse_lazy('blog:posts_all')


def contact_us_view(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            django_send_mail(subject, message, from_email, ['admin@somecompany.com'])
            return redirect('blog:contact_us')
    else:
        form = ContactUsForm()
    return render(request, "contact_us.html", context={"form": form})
