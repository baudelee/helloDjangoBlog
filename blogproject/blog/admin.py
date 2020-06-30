from django.contrib import admin
from .models import Post, Category, Tag
# Register your models here.

# PostAdmin用来配置Post在admin后台打一些展现形式
# fields定义打字段就是表单中展现打字段
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']
    fields = ['title', 'body', 'excerpt', 'category', 'tags']

    # 将post数据保存到数据库
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

# 把新增打Postadmin 也注册进来
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)