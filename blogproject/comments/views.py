from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms import CommentForm
# Create your views here.

# 装饰器require_POST 限定表单提交为POST请求
@require_POST
def comment(request, post_pk):
    # 先获取需要被评论打文章，然后将评论和文章关联起来
    # django提供打快捷函数get_object_or_404
    # 这个函数的作用是如果文章(Post )存在时，则获取；不存在，则返回404
    post = get_object_or_404(Post, pk=post_pk)
    # django将用户提交的数据封装在request.POST中，这是一个类字典对象
    # 我们利用这些数据构造一个CommentForm的实例，这样就生成了一个绑定了用户提交数据打表单
    form = CommentForm(request.POST)
    # 当调用is_valid()方法时，ｄｊａｎｇｏ会自动帮我们检查表单的数据是否符合格式要求
    if form.is_valid():
        # 检查数据合法，调用表单save方法保存数据到数据库
        # commit=False的作用仅仅是利用表单打数据生成一个Comment模型类的实例，但还不保存评论数据到数据库
        comment = form.save(commit=False)
        # 将评论和被评论的文章关联起来
        comment.post = post
        # 最终将评论数据保存进数据库，调用模型实例的save方法
        comment.save()
        # 重定向到ｐｏｓｔ的详情页，实际上当redirect函数接收一个模型的实例时，它会调用这个模型实例打get_absolute_url
        # 然后重定向到get_absolute_url方法返回的URL

        messages.add_message(request, messages.SUCCESS, '评论发表成功', extra_tags='success')
        return redirect(post)

    # 检查到数据不合法，我们渲染一个预览页面，用于展示表单的错误
    # 注意这里被评论打文章post也要传给模板，因为我们需要根基ｐｏｓｔ来生成表单的提交地址
    context = {
        'post': post,
        'form': form,
    }
    messages.add_message(request, messages.ERROR, '评论发表失败', extra_tags='danger')
    return render(request, 'comments/preview.html', context=context)
