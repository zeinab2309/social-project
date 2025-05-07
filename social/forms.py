from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *



class LoginForm(AuthenticationForm):
    username=forms.CharField(max_length=250,required=True, widget=forms.TextInput(attrs={'class':'form-cotrol'}))
    password=forms.CharField(max_length=250,required=True, widget=forms.PasswordInput(attrs={'class':'form-cotrol'}))



class UserRegisterForm(forms.ModelForm):
    password=forms.CharField(max_length=20,widget=forms.PasswordInput,label='پسورد')
    password2=forms.CharField(max_length=20,widget=forms.PasswordInput,label='تکرار پسورد')

    class Meta:
        model=User
        fields=['username','first_name','last_name','phone']

    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password']!=cd['password2']:
            raise forms.ValidationError('پسورد ها مطابقت ندارند!')
        return cd['password2']


    def clean_phone(self):
        phone=self.cleaned_data['phone']
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("phone already exists! ")
        return phone

class UserEditForm(forms.ModelForm):

    class Meta:
        model=User
        fields=['username','first_name','last_name','email','phone','date_of_birth','photo','job']


    def clean_phone(self):
        phone=self.cleaned_data['phone']
        if User.objects.exclude(id=self.instance.id).filter(phone=phone).exists():
            raise forms.ValidationError("phone already exists! ")
        return phone


    def clean_username(self):
        username=self.cleaned_data['username']
        if User.objects.exclude(id=self.instance.id).filter(username=username).exists():
            raise forms.ValidationError("username alreadu exists!")
        return username



class TicketForm(forms.Form):
    SUBJECT_CHOICES=(
        ('پیشنهاد','پیشنهاد'),
        ('انتقاد','انتقاد'),
        ('گزارش','گزارش'),
    )
    message=forms.CharField(widget=forms.Textarea, required=True ,label=" پیام")#تورو بودن یعنی این فیلد اجباری هست
    name=forms.CharField(max_length=250, required=True, label="اسم ")
    email=forms.EmailField(label=" ایمیل")
    phone=forms.CharField(max_length=11, required=True, label="شماره تلفن")
    subject=forms.ChoiceField(choices=SUBJECT_CHOICES, label="موضوع ")

    def clean_phone(self):
        phone=self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError("شماره تلفن عددی نیست!!")
            else:
                return phone


class CreatePostForm(forms.ModelForm):

    class Meta:
        model= Post
        fields=['description','tags']

class SearchForm(forms.Form):
    query=forms.CharField()
