from django.shortcuts import render
from django.contrib.auth import logout,login
# Create your views here.
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import models
import BBS
import datetime
from django.http import HttpResponseRedirect,HttpResponse
from BBS import models
from django_comments.models import Comment
from django.contrib.auth.admin import User
from django import forms
from django.forms import ModelForm



def index2(request):
    perms = request.user.get_all_permissions()
    bbs_list= models.BBS.objects.all()
    bbs_cate=models.Category.objects.all()
    return render_to_response('http1.html',{'aa':bbs_list,
                                          "user":request.user,
                                          "cate":bbs_cate,
                                            "perms":perms
                                          })
def index(request,id):
    perms = request.user.get_all_permissions()
    bbs_list= models.BBS.objects.all()
    bbs_cate=models.Category.objects.all()
    return render_to_response('http1.html',{'aa':bbs_list,
                                          "user":request.user,
                                          "cate":bbs_cate,
                                          "cate_id": int(id),
                                            "perms": perms
                                          })

def ind(request,id):
    perms = request.user.get_all_permissions()
    bbs_list= models.BBS.objects.filter(cate__id=id)
    bbs_cate=models.Category.objects.all()
    return render_to_response('http1.html',{'aa':bbs_list,
                                          "user":request.user,
                                          "cate":bbs_cate,
                                          "cate_id":int(id),
                                            "perms": perms
                                          })


def bbs_detail(request,bbs_id):
    perms = request.user.get_all_permissions()
    bbs_cate = models.Category.objects.all()
    bbs = models.BBS.objects.get(id=bbs_id)
    return render_to_response('test.html',{'bbs_obj':bbs,"user":request.user,"perms": perms,"cate":bbs_cate})

def subcom(request):
    bbs_id=request.POST.get('bbs_id')
    user_comment=request.POST.get("comment")
    Comment.objects.create(
        content_type_id=10,
        object_pk=bbs_id,
        site_id=1,
        user_id=request.user.id,
        comment=user_comment,
        submit_date=datetime.datetime.now(),
    )
    return HttpResponseRedirect("/detail/%s" % bbs_id)

class UserForm(forms.Form):
    name = forms.CharField(max_length=20,help_text="as many as 20 words")
    pwd=forms.CharField(widget=forms.PasswordInput,min_length=8,help_text="as least 8 words")

def delCate(requset):
    for number in requset.POST.keys():
        cate = BBS.models.Category.objects.get(id=number).delete()
    return HttpResponseRedirect("/MagCate/")

class regi(UserForm):
    def clean_name(self):
        data = self.cleaned_data["name"]
        name = []
        alls = models.BBS_user.objects.all()
        for user in alls:
            name.append(user.user.username)
        if data in name:
            raise forms.ValidationError("user exists")
        return data

class lgn(UserForm):
    def clean(self):
        name = self.cleaned_data["name"]
        pwd = self.cleaned_data["pwd"]
        names = []
        alls = models.BBS_user.objects.all()
        for user in alls:
            names.append(user.user.username)
        if name not in names:
            raise forms.ValidationError("user or password is wrong")
        else:
            username = User.objects.get(username=name)

            if not username.check_password(pwd):
                raise forms.ValidationError("user or password is wrong")
        return self.cleaned_data


def Login(request):
    if ("name" or "pwd") not in request.POST:
        lf = lgn()
        return render_to_response("login.html", {"lf": lgn})
    bond = lgn(request.POST)
    if not bond.is_valid():
        return render_to_response("login.html",{"lf":bond})
    name = bond.data['name']
    pwd = bond.data['pwd']
    user = auth.authenticate(username=name,password=pwd)
    auth.login(request,user)
    return HttpResponseRedirect("/")


def register(request):
    if ("name" or "pwd") not in request.POST:
        re = regi()
        return render_to_response("register.html",{"re":re})
    bond = regi(request.POST)
    username = bond.data["name"]
    pwd = bond.data["pwd"]
    if not bond.is_valid():
        return render_to_response("register.html",{"re":bond})
    user = User()
    user.username=username
    user.set_password(pwd)
    user.save()
    user1 = models.BBS_user()
    user1.user=User.objects.get(username=username)
    user1.save()
    return HttpResponseRedirect("/")

def Logout(request):
    user=request.user
    auth.logout(request)
    return HttpResponseRedirect("/")
class CateForm(ModelForm):
    class Meta:
        model=models.Category
        fields = ['name','administrator']

@login_required(login_url="/login/")
def Cate(request):
    if ("name" or "administrator") not in request.POST:
        form = CateForm()
        cate = models.Category.objects.all()
        perms = request.user.get_all_permissions()
        return render_to_response("cate.html", {"form":form, "user":request.user, "cate":cate,"perms":perms})
    f = CateForm(request.POST)
    name = f.data["name"]
    user_id = f.data["administrator"]
    user = models.BBS_user.objects.get(id=user_id)
    administrator = models.BBS_user.objects.get(user__username=user)
    models.Category.objects.create(
        name=name,
        administrator=administrator,
    )
    return HttpResponseRedirect("/MagCate/")

def MagCate(request):
    perms = request.user.get_all_permissions()
    user = User.objects.get(username=request.user)
    cate = models.Category.objects.all()
    return render_to_response("MagCate.html",{"user":user,"cate":cate,"perms":perms})


class BBSForm(ModelForm):
    class Meta:
        model=models.BBS
        fields = ['cate','title','summary','content']

@login_required(login_url="/login/")
def pub(request):
    if ("title" or "content") not in request.POST:
        form = BBSForm()
        cate = models.Category.objects.all()
        try:
            user = User.objects.get(username=request.user)
        except User.DoesNotExist:
            pass
        return render_to_response("pub.html", {"form":form, "user":request.user, "cate":cate})
    f = BBSForm(request.POST)
    cat = f.data["cate"]
    cate = models.Category.objects.get(id=cat)
    title = f.data["title"]
    content = f.data["content"]
    summary = f.data["summary"]
    aut = models.BBS_user.objects.get(user__username=request.user)
    models.BBS.objects.create(
        cate=cate,
        title=title,
        summary=summary,
        content=content,
        author=aut,
        view_count=1,
        ranking=1,
    )
    return HttpResponseRedirect("/")

def modify_bbs(request,bb_id):
    if not request.POST:
        perms = request.user.get_all_permissions()
        cate = models.Category.objects.all()
        bbs = models.BBS.objects.get(id=bb_id)
        form = BBSForm(instance=bbs)
        return render_to_response("modify.html",{"user":request.user,"form":form,"cate":cate,"perms":perms})
    else:
        bbs = models.BBS.objects.get(id=bb_id)
        form=BBSForm(request.POST,instance=bbs)
        form.save()
        return HttpResponseRedirect("/search/")

def search(request):
    perms = request.user.get_all_permissions()
    if request.user.has_perm("BBS.chang_bbs"):
        my_pub=models.BBS.objects.all()
    else:
        my_pub = models.BBS.objects.filter(author__user__username=request.user)
    cate = models.Category.objects.all()
    return render_to_response("my_pub.html",{"my_pub":my_pub,"user":request.user,"cate":cate,"perms":perms})

def MagBBS(request):
    for number in request.POST.keys():
        BBS = models.BBS.objects.get(id=number).delete()
    return HttpResponseRedirect("/search")

















