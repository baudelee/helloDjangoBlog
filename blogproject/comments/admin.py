from django.contrib import admin
from .models import Comment
# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'url', 'post', 'created_time']
    fields = ['name', 'email', 'url', 'text', 'post']


# 将创建的模型注册到ｄｊａｎｇｏ　ａｄｍｉｎ后台，方便管理员用户对评论进行管理
admin.site.register(Comment, CommentAdmin)