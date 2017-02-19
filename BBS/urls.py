"""mydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
import views
import BBS
from django.views.decorators.cache import cache_page
urlpatterns = [
    url(r'^$',views.index2),
    url(r'^index/(\d+)',views.index),
    url(r'^detail/(\d+)/',views.bbs_detail),
    url(r'^login/',views.Login),
    url(r'^logout/',views.Logout),
    url(r'^register/',views.register),
    url(r'pub/',views.pub),
    url(r'search/',views.search),
    url(r'MagBBS/',views.MagBBS),
    url(r'modify_bbs/(\d+)/',views.modify_bbs),
    url(r'MagCate/',views.MagCate),
    url(r'cate/',views.Cate),
    url(r'delCate/',views.delCate),
]
























