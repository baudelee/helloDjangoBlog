import re
import markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.shortcuts import render, HttpResponse, get_object_or_404


from .models import Post, Category, Tag
# Create your views here.

def index(request):
    # Post.objects.all()获取全部文章，而在归档和分类视图中，我们不再用ａｌｌ方法获取全部文章．
    #　而是使用ｆｉｌｔｅｒ来根基调剂过滤
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
    # return render(request, 'blog/index.html', context={
    #     'title': 'my blog site',
    #     'welcome': 'welcome to my blog.'
    # })
    # return HttpResponse('Welcome to  this blog!@')


def archive(request, year, month):
    # python中调用属性的方式是通过created_time.year的方式调用，由于这里作为方法打参数列表，
    #　所以ｄｊａｎｇｏ要求ｗ我们把点替换成两个下划线，即created_time__year
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html',
                  context={'post_list': post_list})


def category(request, pk):
    # pk参数，就是被访问的分类的ｉｄ，
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')

    return render(request, 'blog/index.html', context={'post_list': post_list})


def tag(request, pk):
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')

    return render(request, 'blog/index.html', context={'post_list': post_list})

# 从URL中获取文章id（也就是pk，这里pk和id时等价打）获取数据库中文章id为该值的记录，
# 然后传递给模板
def detail(request, pk):
    # get_object_or_404 如果传入打pk存在时返回对应打post，如果不存在时，返回一个404 error
    post = get_object_or_404(Post, pk=pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 记得引入TocExtension 和 slugify
        TocExtension(slugify=slugify),
    ])

    # 阅读量 +1
    post.increase_views()

    # 使用convert方法将markdown文档转换成HTML文本，而一旦调用该方法md就会多出一个toc属性，
    # 这个属性的值就是内容打目录，然后把md.toc的值复制给post.toc
    # 然而post本身没有toc属性，但是可以动态添加这个属性，这就是python动态语言的好处
    post.body = md.convert(post.body)
    # post.toc = md.toc
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    return render(request, 'blog/detail.html', context={'post': post})