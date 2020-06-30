from django import forms
from .models import Comment


# 要使用django的表单功能，需要导入forms模块．
# django的表单类鼻息继承自forms.Form类或者form.ModelForm类．
class CommentForm(forms.ModelForm):
    class Meta:
        # 指定了这个表单对应打数据库模型Comment
        model = Comment
        # 指定了表单需要显示打字段
        fields = ['name', 'email', 'url', 'text']
