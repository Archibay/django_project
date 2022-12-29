from django.db import models
from django.utils import timezone
from django_lifecycle import LifecycleModel, hook, AFTER_UPDATE
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Comments(LifecycleModel):
    username = models.CharField(max_length=200)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    published = models.BooleanField(default=False)

    @hook(AFTER_UPDATE, when='published', was=False, is_now=True)
    def owner_inform(self):
        post_id = self.post.id
        mail_to = self.post.user.email
        get_url = reverse('blog:post_detail', args=[post_id])
        send_mail(
            'New comment',
            f'New comment was added - {settings.SCHEMA}://{settings.DOMAIN}:{settings.PORT}{get_url}',
            'no_reply@somecompany.com',
            [mail_to]
        )

    def __str__(self):
        return self.text
