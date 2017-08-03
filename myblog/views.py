from django.shortcuts import render,get_object_or_404
from .models import Post, Profile, comments
from django.contrib import auth
from django.http import HttpResponseRedirect
from .forms import loginForm, postForm, SignUpForm
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
import os
from django.contrib.auth.models import User
def myposts(request):
	post = Post.objects.filter(author = request.user).order_by('publish_date')
	return render(request,'blog/posts.html', {'posts':post})
def deletepost(request):
	if request.method == 'POST':
		ids = request.POST.getlist('checks')
		for idd in ids:
			Post.objects.filter(id = idd).delete()
		return redirect('post_list')
	mypost = Post.objects.filter(author = request.user).order_by('publish_date')
	return render(request,'blog/deletepost.html', {'posts':mypost})
def post_list(request):
	post = Post.objects.order_by('publish_date')
	comm = comments.objects.all()
	return render(request,'blog/posts.html',{'posts':post, 'comments':comm})
def post_new(request):
	if request.method == "POST":
		form = postForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.publish_date = timezone.now()
			post.save()
			return redirect('post_list')
	else:
	    form = postForm()
	return render(request, 'blog/newpost.html', {'form': form})
def welcome(request):
	return render(request,'blog/welcome.html')
def login_view(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username = username, password = password)
		if user is not None :
			login(request,user)
			return redirect('post_list')
		else:
			error = "Invalid Credentials ! please try again !!"
			return render(request, 'blog/login.html',{'error':error})
	return render(request,'blog/login.html')
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('post_list')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})

def profile_view(request):
	profile = Profile.objects.filter(user = request.user)
	return render(request,'blog/profile.html',{'profile':profile})
def searchresult(request):
	option = 0
	if request.method == 'POST':
		search = request.POST['searchtext']
		posts = Post.objects.filter(title__icontains = search).order_by('publish_date')
		users = User.objects.filter(first_name__icontains = search)
		if request.POST['search'] == 'all':
			option = 1
			return render(request,'blog/search_results.html',{'users':users,'posts':posts,'option':option})
		elif request.POST['search'] == 'title':
			option = 2
			return render(request,'blog/search_results.html',{'posts':posts,'option':option})
		else :
			option = 3
			return render(request,'blog/search_results.html',{'users':users,'option':option})

def post_details(request,pk):
	post = get_object_or_404(Post,pk=pk)
	comment = comments.objects.filter(post=post)
	return render(request, 'blog/post_details.html',{'post':post, 'comments':comment})

def comment(request,pk):
	post = get_object_or_404(Post,pk=pk)
	if request.method == 'POST':
		comment_obj = comments()
		comment_obj.post = post
		comment_obj.author = request.POST['author']
		comment_obj.comment = request.POST['mycomment']
		comment_obj.save()
		return redirect('post_details',pk=pk)

def edit(request,pk):
	comm = get_object_or_404(comments,pk=pk)
	comm.comment = request.POST['comment']
	comm.save()
	p_pk = comm.post.pk
	return redirect('post_details',pk=p_pk)


def delete(request,pk):
	comment = get_object_or_404(comments,pk=pk)
	post_pk = comment.post.pk
	comment.delete()
	return redirect('post_details',pk=post_pk)