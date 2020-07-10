import markdown
from django.utils.html import strip_tags

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField('标题', max_length=78)
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')

    excerpt = models.CharField('摘要', max_length=200, blank=True)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)

    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    # step 10
    body = models.TextField()

    # step 20
    # 新增ｖｉｅｗｓ字段记录阅读量
    # PositiveIntegerField类型，该类型只允许为正整数或０，因为阅读量不可能为负值．
    # edutable为False表示，该字段不允许通过django admin后台编辑．
    views = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        # ordering用来指定文章排序方式，
        # ['-created_time']　这里指定按照文章发布时间排序，负号表示逆序排列
        # 列表中可以有多个项　
        # ordering = ['-created_time', 'title']，表示首先依据时间排序，如果时间相同，则按照title排序
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    # 因为每次保存模型时，都需要修改modified_time打值，
    # 每一个Model都有一个save方法，这个方法包含了将model数据保存到数据库中打逻辑。、
    # 在指定完modified_time的值后，别忘记调用父类打save方法以执行数据保存回数据库打逻辑
    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        # 首先实例化一个Markdown类，用于渲染body的文本
        # 由于摘要并不需要生成文章目录，所以去掉了目录扩展
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        # 先将Markdown文本渲染成HTML文本
        # strip_tags去掉HTML文本打全班HTML标签
        # 从文本中摘取前54个字符赋值给excerpt
        self.excerpt = strip_tags(md.convert(self.body))[:54]

        super().save(*args, **kwargs)

    # 自定义方法
    # 从django.urls导入reverse方法
    def get_absolute_url(self):
        # blog:detail 意思就是blog应用下打name=detail的函数
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        # update_field告诉数据库只更新views字段
        self.save(update_fields=['views'])
