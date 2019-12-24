from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,AuthenticationForm
from django.db import models
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

# 验证码
class Custlogin(AuthenticationForm):
    capthca=CaptchaField()

# 编辑表单
class Editforms(UserChangeForm):
    birthday = forms.DateField(required=False)
    phone = forms.CharField(required=False)

    class Meta:
        model=User
        fields=('username','password','email','birthday','phone')


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].error_messages={'unique':'用户名已存在！！！'}

# 创建注册表单
class Custforms(UserCreationForm):
    birthday = forms.DateField(required=False)
    phone = forms.CharField(required=False)
    capthca=CaptchaField()

    class Meta:
        model=User
        fields=('username','password1','password2','email','birthday','phone')


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].error_messages={'unique':'用户名已存在！！！'}


#文件选择
class FileForm(forms.Form):
    file_loc = forms.FileField()
    file_name = forms.CharField(max_length=50)


#    file_size = forms.CharField(label='文件大小', max_length=50)
#    file_type = forms.CharField(label='文件类型', max_length=50)
# def handle_uploaded_file(f):
#     with open('upload_folder/name.txt', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

