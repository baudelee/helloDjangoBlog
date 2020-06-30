from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    # 实际视图调用  detail(request, pk=244)
    path('posts/<int:pk>/', views.detail, name='detail'),
    # ｄｊａｎｇｏ会从用户访问打ＵＲＬ中自动提取ＵＲＬ路径参数转换器<type:name>规则捕获打值
    # 然后传递给其对应打视图函数．
    # archive视图函数打实际调用为：archive(request, year=2017, month=3)
    path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    path('categories/<int:pk>/', views.category, name='category'),
    path('tags/<int:pk>', views.tag, name='tag'),

]