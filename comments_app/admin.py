from django.contrib import admin

from comments_app.models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'parent')
    search_fields = ('user__username', 'text')
    list_filter = ('user', 'parent')


admin.site.register(Comment, CommentAdmin)
