from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.sites.AdminSite.site_header="پنل مدیریت جنگو"
admin.sites.AdminSite.site_title="پنل "
admin.sites.AdminSite.index_title="پنل مدیریت"


class ImageInline(admin.TabularInline):
    model=Image
    extra = 1
class CommentInline(admin.TabularInline):
    model=Comment
    extra = 0


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display=['username', 'phone','first_name','last_name']
    fieldsets=UserAdmin.fieldsets+(('imformaiton',{'fields':('date_of_birth', 'bio', 'photo','job','phone')}),)

def make_deactivation(modeladmin,request,queryset):
    result=queryset.update(active=False)
    modeladmin.message_user(request,f"{result}Posts were rejected")
make_deactivation.short_description="رد پست"

def make_activation(modeladmin,request,queryset):
    result=queryset.update(active=True)
    modeladmin.message_user(request,f"{result}Posts were accepted")
make_activation.short_description="تایید پست"

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['description','author','created']
    ordering = ['created']
    search_fields = ['description']
    inlines = [ImageInline,CommentInline]
    actions = [make_deactivation,make_activation]
# admin.sites.register(Contact)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'name', 'created', 'active']
    list_filter = ['active',('created',DateFieldListFilter),('update',DateFieldListFilter)]
    search_fields = ['name','body']
    list_editable = ['active']

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'title', 'created']
