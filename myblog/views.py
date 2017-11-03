from django.shortcuts import render,get_object_or_404
from .models import Post, Profile, comments, Upvotes,Categories
from django.contrib import auth
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from .forms import loginForm, postForm, SignUpForm, DpForm
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime
import requests
from rest_framework import generics
from rest_framework.response import Response
from .serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework import status,permissions
from django.http import HttpResponse, Http404
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
	categories = Categories.objects.all()
	comm = comments.objects.all()
	url = 'http://api.openweathermap.org/data/2.5/weather?zip=560029,IN&appid=dd9a522daa52cc8af21aafd326bff6c8'
	req = requests.get(url)
	### if json response is coming
	response = req.json()
	user_upvotes = Upvotes.objects.filter(user=request.user)
	for upvote in user_upvotes:
		upvoted_post_list.append(upvote.post)
	return render(request,'blog/posts.html',{'posts':post, 'comments':comm,'upvoted_post_list':upvoted_post_list,'response':response,'categories':categories})
def post_new(request):
	categories = Categories.objects.all()
	if request.method == "POST":
		form = postForm(request.POST,request.FILES)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.image = request.FILES.get('image')
			post.publish_date = timezone.now()
			post.save()
			return redirect('post_list')
	else:
	    form = postForm()
	return render(request, 'blog/newpost.html', {'form': form,'categories':categories})
def welcome(request):
	return render(request,'blog/welcome.html')
def login_view(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username = username, password = password)
		if user :
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
	return render(request,'blog/profile.html',{'profile':profile,'num_posts':len(posts),'user':user})

def searchresult(request):
	option = 0
	profile_list = []
	if request.method == 'POST':
		search = request.POST['searchtext']
		posts = Post.objects.filter(title__icontains = search).order_by('publish_date')
		users = User.objects.filter(first_name__icontains = search)
		if users:
			for user in users:
				profile_list.append(Profile.objects.get(user=user))
		if request.POST['search'] == 'all':
			option = 1
			return render(request,'blog/search_results.html',{'profile_list':profile_list,'posts':posts,'option':option})
		elif request.POST['search'] == 'title':
			option = 2
			return render(request,'blog/search_results.html',{'posts':posts,'option':option})
		else :
			option = 3
			return render(request,'blog/search_results.html',{'profile_list':profile_list,'option':option})

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
		comment_obj.authorprofile = profile
		comment_obj.comment = request.POST['mycomment']
		comment_obj.save()
		post.save()
		return redirect('post_details',pk=pk)

def edit(request,pk):
	comm = get_object_or_404(comments,pk=pk)
	if comm.authorprofile.user == request.user:
		comm.comment = request.POST['comment']
		comm.save()
	p_pk = comm.post.pk
	return redirect('post_details',pk=p_pk)


def delete(request,pk):
	comment = get_object_or_404(comments,pk=pk)
	post = comment.post
	post_pk = comment.post.pk
	if comment.authorprofile.user == request.user:
		post.commentcount = post.commentcount - 1
		post.save()
		comment.delete()
	return redirect('post_details',pk=post_pk)

def profileupdate(request,pk):
	profile = get_object_or_404(Profile,pk=pk)
	birthday = profile.birth
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
	return render(request, 'blog/updateprofile.html', {'profile':profile},{'birthday':birthday})

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
	return HttpResponseRedirect('')

def upvoted_users(request,pk):
	up_list = []
	post = get_object_or_404(Post,pk=pk)
	upvotes = Upvotes.objects.filter(post=post)
	for upvote in upvotes:
		up_list.append(get_object_or_404(Profile,user=upvote.user))
	return render(request,'blog/upvoted_users.html',{'up_users':up_list})

def editpost(request,pk):
	post = get_object_or_404(Post,pk=pk)
	categories = Categories.objects.all().order_by('title')
	if request.method == "POST":
		post.title = request.POST['title']
		post.text = request.POST['content']
		post.category = get_object_or_404(Categories,title=request.POST['category']) 
		if request.FILES.get('image'):
			post.image = request.FILES.get('image')
		post.save()
		return redirect('post_details',pk=pk)
	return render(request,'blog/edit_post.html',{'post':post,'categories':categories})

def updateDp(request):
	profile = get_object_or_404(Profile,user=request.user)
	if request.method == 'POST':
		profile.dp = request.FILES.get('mydp')
		profile.save()
		return redirect('profile_view',pk=request.user.pk)
	return render(request,'blog/updateDp.html',{'profile':profile})

def weather(request):
	url = 'http://api.openweathermap.org/data/2.5/weather?zip=560029,IN&appid=dd9a522daa52cc8af21aafd326bff6c8'
	req = requests.get(url)
	### if json response is coming
	response = req.json()
	return render(request,'blog/weather.html',{'response':response})
def filter(request,pk):
	category = Categories.objects.get(pk=pk)
	upvoted_post_list = []
	post = Post.objects.filter(category=category).order_by('publish_date')
	categories = Categories.objects.all()
	comm = comments.objects.all()
	user_upvotes = Upvotes.objects.filter(user=request.user)
	for upvote in user_upvotes:
		upvoted_post_list.append(upvote.post)
	return render(request,'blog/posts.html',{'posts':post, 'comments':comm,'upvoted_post_list':upvoted_post_list,'categories':categories})

class createPost(generics.CreateAPIView):
	serializer_class = PostSerializer
	queryset = Post.objects.all()
	#permission_classes = (permissions.IsAdminUser,)
	def get(self,request):
		queryset = self.get_queryset()
		serializer = PostSerializer(queryset,many=True)
		return Response(serializer.data) 
class removePost(APIView):
	serializer_class = PostSerializer
	queryset = Post.objects.all()
	permission_classes = (permissions.IsAdminUser,)
	def get_object(self, pk):
		try:
			return Post.objects.get(pk=pk)
		except Post.DoesNotExist:
			raise Http404
	def get(self,request,pk):
		queryset = self.get_object(pk)
		serializer = PostSerializer(queryset)
		return Response(serializer.data)
	def delete(self,request,pk):
		post = self.get_object(pk)
		post.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)