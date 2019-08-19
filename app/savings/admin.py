from django.contrib import admin
from .models import GroupAccount,MemberAccount

@admin.register(GroupAccount)
class GroupAccountAdmin(admin.ModelAdmin):
    list_display = ('group_admin','name','description','id')

@admin.register(MemberAccount)
class MemberAccountAdmin(admin.ModelAdmin):
    list_display = ('member','group','amount','id')