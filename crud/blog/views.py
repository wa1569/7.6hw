from django.http import request
from .forms import PostForm, UserInformationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Hashtag, Post
from django.utils import timezone
from blog.forms import PostForm, CommentForm, HashtagForm
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


#메인페이지
def main(request):
    posts = Post.objects
    hashtags = Hashtag.objects
    return render(request, 'blog/main.html', {'posts':posts, 'hashtags':hashtags})

#글쓰기페이지
def write(request):
    return render(request, 'blog/create.html')

#글쓰기 함수
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form= form.save(commit=False)
            form.pub_date = timezone.now()
            form.save()
            return redirect('read')

    else:
        form=PostForm
        return render(request, 'blog/write.html', {'form':form})

#읽기페이지
def read(request):
    posts = Post.objects
    return render(request, 'blog/read.html', {'posts':posts})


#수정페이지
def edit(request):
    return render(request, 'blog/edit.html')

#수정 함수
def edit(request, id):
    post = get_object_or_404(Post, id = id)
    if request.method =="POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            return redirect('read')
        
    else:
        form= PostForm(instance=post)
        return render(request, 'blog/edit.html', {'form':form})


def delete(request, id):
    post = get_object_or_404(Post, id = id)
    post.delete()
    return redirect('read')

def detail(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = post
            comment.text = form.cleaned_data['text']
            comment.save()
            return redirect('detail', id)

    else:
        form = CommentForm()
        return render(request, "blog/detail.html", {'post':post, 'form':form})

def hashtagform(request, hashtag=None):
    if request.method == 'POST':
        form = HashtagForm(request.POST, instance=hashtag)
        if form.is_valid():
            hashtag = form.save(commit=False)
            if Hashtag.objects.filter(name=form.cleaned_data['name']):
                form = HashtagForm()
                error_message = "이미 존재하는 해시태그 입니다."
                return render(request, 'blog/hashtag.html', {'form':form, "error_message":error_message})
            else:
                hashtag.name = form.cleaned_data['name']
                hashtag.save()
            return redirect('main')
    else:
        form = HashtagForm(instance=hashtag)
        return render(request, 'blog/hashtag.html', {'form':form})

def search(request, hashtag_id):
    hashtag=get_object_or_404(Hashtag, pk=hashtag_id)
    return render(request, 'blog/search.html', {'hashtag':hashtag})

def signup(request):
    if request.method =='POST':
        form1 = UserCreationForm(request.POST)
        form2 = UserInformationForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user_information = form2.save(commit = False)
            user_information.user = user
            user_information.save()
            auth.login(request, user)
            return redirect('main')
        else:
            return render(request, 'blog/signup.html', {'form1':form1, 'form2':form2})
    else:
        form1 = UserCreationForm()
        form2 = UserInformationForm()
        return render(request, 'blog/signup.html', {'form1':form1, 'form2': form2})

def login(request):
    if request.method =='POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect('main')
        else:
            form = AuthenticationForm()
            return render(request, 'blog/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'blog/login.html', {'form':form})

def logout(request):
    auth.logout(request)
    return redirect('main')

