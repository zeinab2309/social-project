from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.filters import DateFieldListFilter
# Register your models here.

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display=['username', 'phone','first_name','last_name']
    fieldsets=UserAdmin.fieldsets+(('imformaiton',{'fields':('date_of_birth', 'bio', 'photo','job','phone')}),)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author','created']
    ordering = ['created']
    search_fields = ['description']

class CommentInline(admin.TabularInline):
    model=Comment
    extra = 0


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'name', 'created', 'active']
    list_filter = ['active',('created',DateFieldListFilter),('update',DateFieldListFilter)]
    search_fields = ['name','body']
    list_editable = ['active']
