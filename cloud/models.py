from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Member(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(blank=False, null=True)
    phone = models.CharField(blank=False, max_length=32)

    class Meta:
        verbose_name_plural = "Member"



class File(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=50)  #文件名
    file_loc = models.FileField(upload_to='upload_folder')   #文件位置
    file_size = models.CharField(max_length=50)   #文件大小
    file_type = models.CharField(max_length=50)   #文件类型
    upload_time = models.DateTimeField()       #上传时间

    def __unicode__(self):
        return self.file_name


