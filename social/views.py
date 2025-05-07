from django.shortcuts import render
from django.contrib.auth import logout,authenticate,login
from django.shortcuts import render,get_object_or_404 ,redirect
from django.http import HttpResponse
from pyexpat.errors import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import *
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q

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
    sent = False
    if request.method=="POST":
        form=TicketForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            message=f"{cd['name']}\n{cd['email']}\n{cd['phone']}\n\n{cd['message']}"
            send_mail(cd['subject'],message,'poormoosavie0@gmail.com',['mfrey2211@gmail.com'],fail_silently=False)
            sent=True
    else:
        form=TicketForm()
    return render(request , "forms/ticket.html",{'form':form,'sent':sent})


def post_list(request,tag_slug=None):
    posts=Post.objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        posts=Post.objects.filter(tags__in=[tag])
    context={
        'posts':posts,
        'tag':tag,
    }
    return render(request,"social/list.html",context)

@login_required
def create_post(request):
    if request.method=="POST":
        form=CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.save()
            form.save_m2m()
            return redirect('social:profile')
    else:
        form=CreatePostForm()
    return render(request, 'forms/create-post.html',{'form':form})



def post_detail(request , pk):
    post=get_object_or_404(Post, id=pk)
    post_tags_ids=post.tags.values_list('id',flat=True)
    similar_post=Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_post=similar_post.annotate(same_tags=Count('tags')).order_by('-same_tags','-created')[:2]
    context={
        'post':post,
        'similar_post':similar_post
    }
    return render(request,"social/detail.html",context)



def post_search(request):
    query=None
    results=[]
    if 'query' in request.GET:
        form=SearchForm(data=request.GET)
        if form.is_valid():
            query=form.cleaned_data['query']
            results = Post.objects.filter(
            Q(description__contains=query)|Q(tags__name__contains=query)).distinct()

        context={
           'query':query,
           'results':results
        }
    return render(request,'social/search.html',context)



