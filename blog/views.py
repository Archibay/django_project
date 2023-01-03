from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comments
from django.contrib.auth.models import User
from .forms import PostForm, CommentForm, ContactUsForm
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.contrib import messages
from .tasks import send_mail as celery_send_mail
from django.template.loader import render_to_string
from django.http import JsonResponse


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published_date = timezone.now()
            post.save()
            subject = 'New post'
            message = 'New post was added'
            from_email = 'no_reply@somecompany.com'
            to_email = ['admin@somecompany.com']
            celery_send_mail.delay(subject, message, from_email, to_email)
            return redirect('blog:posts_all')
    else:
        form = PostForm()
    return render(request, 'post_new.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_l = post.comments_set.filter(published=True).all()
    paginator = Paginator(comment_l, 2)
    page = request.GET.get('page')
    comment_p = paginator.get_page(page)
    return render(request, 'post_detail.html', {'post': post, 'comment': comment_p})


# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'post_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(PostDetailView, self).get_context_data(**kwargs)
#         post = self.get_object()
#         comment = post.comments_set.filter(published=True).all()
#         paginator = Paginator(comment, 2)
#         context['comments'] = paginator.get_page(comment)
#         return context

    # def get_context_data(self):
    #     context = super(PostDetailView, self).get_context_data()
    #     _list = Comment.objects.filter(post=self.kwargs.get('pk'))
    #     paginator = Paginator(_list, 25) # Show 25 contacts per page
    #     page = request.GET.get('page')
    #     context['comments'] = paginator.get_page(page)
    #     return context


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
        subject = 'New comment'
        message = 'New comment was added'
        from_email = 'no_reply@somecompany.com'
        to_email = ['admin@somecompany.com']
        celery_send_mail.delay(subject, message, from_email, to_email)
        return super().form_valid(form)
    success_url = reverse_lazy('blog:posts_all')


def contact_us_view(request):
    data = dict()
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True

            data['html_contact_us'] = render_to_string('contact_us.html', {'form': form})
            return redirect('blog:posts_all')
        else:
            data['form_is_valid'] = False
    else:
        form = ContactUsForm()
    context = {'form': form}
    data['html_form'] = render_to_string('contact_us.html', context, request=request)
    return JsonResponse(data)


# def contact_us_view(request):
#     if request.method == "POST":
#         form = ContactUsForm(request.POST)
#         if form.is_valid():
#             subject = form.cleaned_data['subject']
#             message = form.cleaned_data['message']
#             from_email = form.cleaned_data['from_email']
#             to_email = ['admin@somecompany.com']
#             celery_send_mail.delay(subject, message, from_email, to_email)
#             messages.add_message(request, messages.SUCCESS, 'Message sent')
#             return redirect('blog:posts_all')
#     else:
#         form = ContactUsForm()
#     return render(request, "contact_us.html", context={"form": form})
