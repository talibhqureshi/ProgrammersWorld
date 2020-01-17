from django.shortcuts import render
from .forms import UserSignupForm, UserLoginForm, CreateBlogForm, UpdateProfileForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Blog

def home(request):
	keyword = request.GET.get('keyword','')
	search_results = ''
	if keyword:
		search_results = Blog.objects.filter(title__icontains=keyword)

	blogs = Blog.objects.all()
	return render(request,'home.html',{'blogs':blogs,'search_results':search_results})

def user_signup(request):
	if request.method == 'POST':
		form = UserSignupForm(request.POST)
		if form.is_valid():
			clean_data = form.cleaned_data
			username = clean_data['username']
			first_name = clean_data['first_name']
			last_name = clean_data['last_name']
			email = clean_data['email']
			password = clean_data['password']
			user = User.objects.create(username=username,first_name=first_name,last_name=last_name,email=email)
			user.set_password(password)
			user.save()
			messages.success(request,'!! Signup Successfull Please Login !!')
			return HttpResponseRedirect(reverse('login'))
		else:
			return render(request,'signup.html',{'form':form})

	form = UserSignupForm()
	return render(request,'signup.html',{'form':form})


def user_login(request):
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			username = User.objects.get(email=email).username
			user = authenticate(username=username,password=password)
			if user:
				login(request,user)
				return HttpResponseRedirect(reverse('create_blog'))	
		else:
			return render(request,'login.html',{'form':form})

	form = UserLoginForm()
	return render(request,'login.html',{'form':form})


@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('home'))


@login_required
def show_blogs(request):
	user = request.user
	blogs = Blog.objects.filter(author=user)
	return render(request,'show_blogs.html',{'blogs':blogs})


@login_required
def create_blog(request):
	if request.method == 'POST':
		form = CreateBlogForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			content = form.cleaned_data['content']
			Blog.objects.create(title=title,content=content,author=request.user)
			messages.success(request,'You Created a New Blog')
			return HttpResponseRedirect(reverse('show_blogs'))

	form = CreateBlogForm()
	return render(request,'create_blog.html',{'form':form})


@login_required
def user_profile(request):
	user_form = UserSignupForm()
	profile_form = UpdateProfileForm()
	return render(request,'user_profile.html',{'user_form':user_form,'profile_form':profile_form})
	
