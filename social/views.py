from django.contrib.auth import logout
from django.shortcuts import render,get_object_or_404 ,redirect
from django.http import HttpResponse, JsonResponse
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import *
from taggit.models import Tag
from django.db.models import Count
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.views.decorators.http import require_POST
# Create your views here.
def log_out(request):
    logout(request)
    return HttpResponse("شما خارج شدید")
@login_required
def profile(request):
    posts = Post.objects.filter(author=request.user).order_by('-created')
    return render(request, "social/profile.html",{'posts':posts})


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
    paginator=Paginator(posts,2)
    page_number=request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = []
    except PageNotAnInteger:
        posts = paginator.page(1)

    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        return render(request,'social/list_ajax.html',{'posts':posts})

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
            Image.objects.create(image_file=form.cleaned_data['image1'],post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'],post=post)
            return redirect('social:profile')
    else:
        form=CreatePostForm()
    return render(request, 'forms/create-post.html',{'form':form})



def post_detail(request , pk):
    post=get_object_or_404(Post, id=pk)
    comments = post.comments.filter(active=True)
    post_tags_ids=post.tags.values_list('id',flat=True)
    similar_post=Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_post=similar_post.annotate(same_tags=Count('tags')).order_by('-same_tags','-created')[:2]
    context={
        'post':post,
        'similar_post':similar_post,
        'comments': comments
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



def post_comment(request, post_id):
    post=get_object_or_404(Post, id=post_id)
    comment=None
    form=CommentForm(data=request.POST)
    if form.is_valid():
        comment=form.save(commit=False)
        comment.post=post
        comment.save()
    context={
        'post':post,
        'form':form,
        'comment':comment

    }
    return render(request, "forms/comment.html", context)


@login_required
def edit_post(request,post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            return redirect('social:profile')
    else:
        form = CreatePostForm(instance=post)
    return render(request, 'forms/create-post.html', {'form': form, 'post':post})

@login_required
def delete_post(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    if request.method=="POST":
        post.delete()
        return redirect('social:profile')
    return render(request,'forms/delete-post.html',{'post':post})

@login_required
def delete_image(request,image_id):
    image=get_object_or_404(Image,id=image_id)
    image.delete()
    return redirect('social:profile')

@login_required
@require_POST
def like_post(request):
    post_id=request.POST.get('post_id')
    if post_id is not None:
        post=get_object_or_404(Post,id=post_id)
        user=request.user

        if user in post.likes.all():
            post.likes.remove(user)
            liked=False
        else:
            post.likes.add(user)
            liked=True

        post_likes_count=post.likes.count()
        response_data={
            'liked':liked,
            'likes_count':post_likes_count,
        }
    else:
        response_data={'error':'Invalid post_id'}
    return JsonResponse(response_data)