from django import template

from ..models import Post, Category, Tag

register = template.Library()

# takes_context 设置为True时告诉Django，在渲染_recent_posts.html模板时，不仅传入
# show_recent_posts返回的模板变量，同时传入父模板（即使用{% show_recent_posts %}模板标签的模板）上下文
@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num],
    }

@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    # 这里Post.objects.dates方法会返回一个列表。列表中打元素为每一篇文章Post的创建时间，且是Python的date对象，
    #　精确到月份，降序排列．
    return {
        'date_list': Post.objects.dates('created_time', 'month', order='DESC'),
    }

@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    return {
        'category_list': Category.objects.all(),
    }

@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    return {
        'tag_list': Tag.objects.all(),
    }