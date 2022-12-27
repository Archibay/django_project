from django.contrib import admin
from.models import Post, Comments


class PostAdmin(admin.ModelAdmin):
    list_display = ['text']
    list_filter = ['published']
    list_per_page = 20
    fields = ['text', 'published']
    save_as = True


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['text', 'published']
    list_filter = ['published']
    list_per_page = 20
    fields = ['text', 'published']
    save_as = True


admin.site.register(Post, PostAdmin)
admin.site.register(Comments, CommentsAdmin)
