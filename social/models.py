from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager
from  django.urls import  reverse
# Create your models here.

class User(AbstractUser):
    date_of_birth=models.DateTimeField(verbose_name="تاریخ تولد", blank=True, null=True)
    bio=models.TextField(verbose_name=" بایو ", blank=True, null=True )
    photo=models.ImageField(verbose_name="تصاویر",upload_to="account_images/",null=True, blank=True)
    job=models.CharField(max_length=250,verbose_name="شغل", blank=True, null=True)
    phone=models.CharField(verbose_name="شماره تلفن",max_length=11, blank=True, null=True)



# Create your models here.
class Post(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_posts",verbose_name="نویسنده")
    description=models.TextField(verbose_name="توضیحات")
    created=models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags=TaggableManager()
    class Meta:
        ordering=['-created']
        indexes=[
            models.Index(fields=['-created'])
        ]
        verbose_name="پست"
        verbose_name_plural = "پست ها"

    def __str__(self):
        return self.author.first_name

    def get_absolute_url(self):
        return reverse('social:post_detail', args=[self.id])


class Ticket(models.Model):
    message=models.TextField(verbose_name="پیام")
    name=models.CharField(max_length=250 , verbose_name="نام")
    email=models.EmailField(verbose_name="ایمیل")
    phone=models.CharField(max_length=11,verbose_name="شماره تلفن")
    subject=models.CharField(max_length=250,verbose_name="موضوع")


    class Meta:
        verbose_name="تیکت"
        verbose_name_plural = "تیکت ها"
    def __str__(self):
        return self.subject



class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments",verbose_name="پست")
    name=models.CharField(max_length=250,verbose_name="نام")
    body=models.TextField(verbose_name="متن کامنت")
    created=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)

    class Meta:
        ordering=['-created']
        indexes=[
            models.Index(fields=['-created'])
        ]
        verbose_name="کامنت"
        verbose_name_plural = "کامنت ها"
    def __str__(self):
        return f"{self.name}:{self.post}"

