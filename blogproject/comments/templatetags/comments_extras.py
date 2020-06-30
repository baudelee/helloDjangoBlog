from django import template
from ..forms import CommentForm

register = template.Library()


@register.inclusion_tag('comments/inclusions/_form.html', takes_context=True)
def show_comment_form(context, post, form=None):
    if form is None:
        form = CommentForm()
    return {
        'form': form,
        'post': post,
    }

@register.inclusion_tag('comments/inclusions/_list.html', takes_context=True)
def show_comments(context, post):
    # post.comment_set.all()来获取post对应打全部评论，
    # Comment　与　Post通过ForeignKey关联的．
    # 这里post.comment_set.all()等价于Comment.objects.filter(post=post),根据post来获取post下的全部评论
    comment_list = post.comment_set.all().order_by('-created_time')
    comment_count = comment_list.count()

    return {
        'comment_count': comment_count,
        'comment_list': comment_list,
    }