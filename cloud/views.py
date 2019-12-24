import MySQLdb
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.contrib.auth.models import User
from .forms import Custforms, Editforms, Custlogin,FileForm
from .models import Member,File
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .ftp import get_data,readFile
from django.http import FileResponse
from django.utils.http import urlquote
from django.http import HttpResponse,StreamingHttpResponse
import re


def home(request):
    username = request.COOKIES.get('username', '')
    if not username:
        return render(request, "home.html")
    else:
        id=User.objects.get(username=username).id
        sql = "select * from cloud_file where username_id="+str(id)  # t为表名
        m_data = get_data(sql)
        return render(request, "home.html",{'order':m_data})



# 登录
def login_cloud(request):
    if request.method == 'POST':
        custlogin = Custlogin(data=request.POST)
        if custlogin.is_valid():
            user = authenticate(request, username=custlogin.cleaned_data['username'],
                                password=custlogin.cleaned_data['password'])
            login(request, user)
            response = redirect("templates:home")

            response.set_cookie('username', custlogin.cleaned_data['username'])

            return response

    else:
        custlogin = Custlogin()
    content = {'custlogin': custlogin}
    return render(request, "login.html", content)

# 登出
def logout_cloud(request):
    logout(request)
    return redirect("templates:home")

# 注册
def register_cloud(request):
    if request.method == 'POST':
        usercreateform = Custforms(request.POST)
        if usercreateform.is_valid():
            usercreateform.save()
            user = authenticate(request, username=usercreateform.cleaned_data['username'],
                                password=usercreateform.cleaned_data['password1'])
            user.email = usercreateform.cleaned_data['email']
            Member(username=user, birthday=usercreateform.cleaned_data['birthday'],
                   phone=usercreateform.cleaned_data['phone']).save()
            login(request, user)
            return redirect("templates:home")
    else:
        usercreateform = Custforms()
    content = {'usercreateform': usercreateform}

    return render(request, "register.html", content)

# 个人中心
@login_required(login_url='templates:login')
def center(request):
    content = {'user': request.user}
    return render(request, 'user_center.html', content)

# 编辑信息
@login_required(login_url='templates:login')
def edit_profile(request):
    if request.method == 'POST':
        usercreateform = Editforms(request.POST, instance=request.user)
        if usercreateform.is_valid():
            usercreateform.save()
            birthday = usercreateform.cleaned_data['birthday']
            phone = usercreateform.cleaned_data['phone']
            Member(username=request.user,birthday=birthday,phone=phone).save()
            return redirect("templates:center")
    else:
        usercreateform = Editforms(instance=request.user)
    content = {'usercreateform': usercreateform, 'user': request.user}
    return render(request, "edit_profile.html", content)

# 修改密码
@login_required(login_url='templates:login')
def change_password(request):
    if request.method == 'POST':
        changepasswordform = PasswordChangeForm(data=request.POST, user=request.user)
        if changepasswordform.is_valid():
            changepasswordform.save()
            return redirect("templates:center")
    else:
        changepasswordform = PasswordChangeForm(user=request.user)
    content = {'changepasswordform': changepasswordform, 'user': request.user}
    return render(request, "change_password.html", content)


#文件
def upload(request):
    if request.method == "POST":
        ff=FileForm(request.POST,request.FILES)
        username = request.COOKIES.get('username', '')
        b='Byte'

        file_handel=request.FILES.get('file_loc')

        file_name = str(file_handel.name)
        file_type_split1 = str(file_handel.name)
        file_type_split2 = file_type_split1.split('.')
        file_type = file_type_split2[1]
        # instance = handle_uploaded_file(f=)

            # # file_name = FileForm.cleaned_data['file_name']
        file_size = str(file_handel.size) + b

        user=User.objects.get(username=username)
        # #写入数据库
        upload_time=timezone.now()
        File(username=user,file_name=file_name, file_loc=file_handel,file_size=file_size, file_type=file_type,upload_time=upload_time).save()
        return redirect("templates:home")

    else:
        ff=FileForm()
    return render(request,'upload_files.html',{"ff":ff})


def del_file(request,foo_0):
    if request.method == 'POST':
        sql = "delete  from cloud_file where id=" + foo_0  # t为表名
        get_data(sql)
        return redirect('templates:home')

def download(request, foo_1):
 if request.method == 'POST':
     # download_name = request.GET["file"]
     # the_file_name = str(foo_1).split("/")[-1]  # 显示在弹出对话框中的默认的下载文件名
     filename = 'upload_folder/{}'.format(foo_1)  # 要下载的文件路径
     response = FileResponse(readFile(filename))
     # response = StreamingHttpResponse(readFile(filename))
     response['Content-Type'] = 'application/octet-stream'
     response['Content-Disposition'] = 'attachment;filename="{0}"'.format(foo_1)
     return response








#
# filename = request.GET.get('file')
#  filepath = os.path.join(settings.MEDIA_ROOT, filename)
#  fp = open(filepath, 'rb')
#  response = StreamingHttpResponse(fp)
#  # response = FileResponse(fp)
#  response['Content-Type'] = 'application/octet-stream'
#  response['Content-Disposition'] = 'attachment;filename="%s"' % filename
#  return response
# #  fp.close()



# filename = request.GET.get(u'file')
#     name=filename.split('/')[1]
#     file = open(filename,mode='rb')
#     response=FileResponse(file)
#     response['Content-Type']='application/octet-stream'
#     response['Content-Disposition']='attachment;filename="%s'%name
#     return response
