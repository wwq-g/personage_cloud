from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Member


class MemberInline(admin.TabularInline):
    model = Member
    can_delete = True
    verbose_name_plural = 'Member'

class UserAdmin(BaseUserAdmin):
    inlines = (MemberInline, )

admin.site.unregister(User)
admin.site.register(User,UserAdmin)


