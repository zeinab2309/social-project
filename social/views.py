from django.shortcuts import render
from django.contrib.auth import logout,authenticate,login
from django.shortcuts import render,get_object_or_404 ,redirect
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def log_out(request):
    logout(request)
    return HttpResponse("شما خراج شدید")

def profile(request):
    return HttpResponse("شما وارد شدید")


def register(request):
    if request.method=='POST':
        form =UserRegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'registration/register_done.html', {'user':user})
    else:
        form=UserRegisterForm()
    return render(request, 'registration/register.html', {'form':form})



@login_required
def edit_user(request):
    if request.method=="POST":
        user_form=UserEditForm(request.POST, instance=request.user, files=request.FILES)
        if  user_form.is_valid():
            user_form.save()
            context = {
                'user_form': user_form
            }
            return render(request, 'registration/edit_account_done.html', context)
    else:
        user_form=UserEditForm(instance=request.user)

    context={
        'user_form':user_form
    }
    return render(request, 'registration/edit_user.html',context)



def ticket(request):

    if request.method=="POST":
        form=TicketForm(request.POST)
        if form.is_valid():
            ticket_obj =Ticket.objects.create()
            cd=form.cleaned_data
            ticket_obj.message=cd['message']
            ticket_obj.name = cd['name']
            ticket_obj.email = cd['email']
            ticket_obj.phone = cd['phone']
            ticket_obj.subject = cd['subject']
            ticket_obj.save()
            return redirect("blog:index")
    else:
        form=TicketForm()
    return render(request , "forms/ticket.html",{'form':form})
