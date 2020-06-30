from django.db import models
from django.utils import timezone

# Create your models here.


class Comment(models.Model):
    name = models.CharField('名字', max_length=50)
    email = models.EmailField('邮箱')
    url = models.URLField('网址', blank=True)
    text = models.TextField('内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    # 一个评论只能属于一篇文章，一个篇文章可以有多个评论，是一对多打关系．
    # 因此这里使用的是ＦｏｒｅｉｇｎＫｅｙ

    # 所有模型的字段都接受一个verbose_name参数（大部分时第一个位置参数)，
    # django在根据模型打定义自动生成表单时，会使用这个参数的值作为表单字段打ｌａｂｅｌ，

    post = models.ForeignKey('blog.Post', verbose_name='文章', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}: {}'.format(self.name, self.text[:20])

