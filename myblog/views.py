from django.shortcuts import render,get_object_or_404
from .models import Post, Profile, comments, Upvotes
from django.contrib import auth
from django.http import HttpResponseRedirect
from .forms import loginForm, postForm, SignUpForm, DpForm
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
import os
import re
from django.contrib.auth.models import User
def myposts(request):
	post = Post.objects.filter(author = request.user).order_by('publish_date')
	return render(request,'blog/posts.html', {'posts':post, 'num_posts':len(post)})
def deletepost(request):
	if request.method == 'POST':
		ids = request.POST.getlist('checks')
		for idd in ids:
			Post.objects.filter(id = idd).delete()
		return redirect('post_list')
	mypost = Post.objects.filter(author = request.user).order_by('publish_date')
	return render(request,'blog/deletepost.html', {'posts':mypost})
def post_list(request):
	upvoted_post_list = []
	post = Post.objects.order_by('publish_date')
	comm = comments.objects.all()
	user_upvotes = Upvotes.objects.filter(user=request.user)
	for upvote in user_upvotes:
		upvoted_post_list.append(upvote.post)
	return render(request,'blog/posts.html',{'posts':post, 'comments':comm,'upvoted_post_list':upvoted_post_list})
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
            myprofile = Profile()
            myprofile.user = user
            myprofile.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})

def profile_view(request,pk):
	user = get_object_or_404(User,pk=pk)
	profile = get_object_or_404(Profile,user=user)
	posts = Post.objects.filter(author = user)
	count = 0
	for post in posts:
		count += post.like
	if 'default_dp.png' in str(profile.dp):
		dp_name = "profilepic/default/default_dp.png"
	else:
		dp_name = "profilepic/"+str(request.user)+"/"+str(profile.dp)
	return render(request,'blog/profile.html',{'profile':profile,'dp_name':str(dp_name),'num_posts':len(posts),'user':user})

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
	upvote_posts = []
	upvote_users = []
	post = get_object_or_404(Post,pk=pk)
	comment = comments.objects.filter(post=post)
	user_upvotes = Upvotes.objects.filter(user=request.user)
	upvote_list = Upvotes.objects.filter(post=post)
	for upvote in upvote_list:
		upvote_users.append(upvote.user)
	for upvote in user_upvotes:
		upvote_posts.append(upvote.post)
	return render(request, 'blog/post_details.html',{'post':post, 'comments':comment,'upvote_posts':upvote_posts,'num_users':len(upvote_users)})

def comment(request,pk):
	post = get_object_or_404(Post,pk=pk)
	profile = Profile.objects.get(user = request.user)
	if request.method == 'POST':
		comment_obj = comments()
		comment_obj.post = post
		post.commentcount = post.commentcount + 1
		comment_obj.dp = profile.dp
		comment_obj.author = request.user
		comment_obj.comment = request.POST['mycomment']
		comment_obj.save()
		post.save()
		return redirect('post_details',pk=pk)

def edit(request,pk):
	comm = get_object_or_404(comments,pk=pk)
	if comm.author == request.user:
		comm.comment = request.POST['comment']
		comm.save()
	p_pk = comm.post.pk
	return redirect('post_details',pk=p_pk)


def delete(request,pk):
	comment = get_object_or_404(comments,pk=pk)
	post = comment.post
	post_pk = comment.post.pk
	if comment.author == request.user:
		post.commentcount = post.commentcount - 1
		post.save()
		comment.delete()
	return redirect('post_details',pk=post_pk)

def profileupdate(request,pk):
	profile = get_object_or_404(Profile,pk=pk)
	user = profile.user
	if request.method == 'POST':
		profile.phone = request.POST['phone']
		profile.birth = request.POST['birth']
		user.first_name = request.POST['fname']
		user.last_name = request.POST['lname']
		user.email = request.POST['email']
		user.save()
		profile.save()
		return redirect('profile_view',pk=request.user.pk)
	return render(request, 'blog/updateprofile.html', {'profile':profile})

def upvotes(request,pk):
	upv_obj = Upvotes.objects.filter(post = pk,user = request.user)
	post = get_object_or_404(Post,pk=pk)
	if upv_obj:
		for u_obj in upv_obj:
			if u_obj.user == request.user:
				post.like = post.like - 1
				post.save()
				upv_obj.delete()
	else:
		upv_obj = Upvotes()
		post.like = post.like + 1
		upv_obj.post = post
		upv_obj.user = request.user
		upv_obj.upvote = True
		post.save()
		upv_obj.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def upvoted_users(request,pk):
	up_list = []
	post = get_object_or_404(Post,pk=pk)
	upvotes = Upvotes.objects.filter(post=post)
	for upvote in upvotes:
		up_list.append(get_object_or_404(Profile,user=upvote.user))
	return render(request,'blog/upvoted_users.html',{'up_users':up_list})

def editpost(request,pk):
	post = get_object_or_404(Post,pk=pk)
	if request.method == "POST":
		post.title = request.POST['title']
		post.text = request.POST['content']
		post.save()
		return redirect('post_details',pk=pk)
	return render(request,'blog/edit_post.html',{'post':post})

def updateDp(request):
	profile = get_object_or_404(Profile,user=request.user)
	if request.method == 'POST':
		profile.dp = request.FILES.get('mydp')
		profile.save()
		return redirect('profile_view',pk=request.user.pk)
	return render(request,'blog/updateDp.html',{'profile':profile})