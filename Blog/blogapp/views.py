from django.shortcuts import render
from .forms import UserSignupForm, UserLoginForm, CreateBlogForm, UserProfileForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Blog, UserProfile

def home(request):
	keyword = request.GET.get('keyword','')
	search_results = ''
	if keyword:
		search_results = Blog.objects.filter(title__icontains=keyword)

	blogs = Blog.objects.all()
	return render(request,'home.html',{'blogs':blogs,'search_results':search_results})

def user_signup(request):
	if request.method == 'POST':
		user_form = UserSignupForm(request.POST)
		profile_form = UserProfileForm(request.POST,request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save(commit=False)
			user.set_password(user_form.cleaned_data['password'])
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			profile.save()
			messages.success(request,'!! Signup Successfull Please Login !!')
			return HttpResponseRedirect(reverse('login'))
		else:
			return render(request,'signup.html',{'user_form':user_form,'profile_form':profile_form})

	user_form = UserSignupForm()
	profile_form = UserProfileForm()
	return render(request,'signup.html',{'user_form':user_form,'profile_form':profile_form})


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
				return HttpResponseRedirect(reverse('show_blogs'))	
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
	user_profile = UserProfile.objects.get(user=user)
	return render(request,'show_blogs.html',{'blogs':blogs,'user_profile':user_profile})


@login_required
def create_blog(request):
	if request.method == 'POST':
		form = CreateBlogForm(request.POST)
		if form.is_valid():
			blog = form.save(commit=False)
			blog.author = request.user
			blog.save()
			messages.success(request,'You Created a New Blog')
			return HttpResponseRedirect(reverse('show_blogs'))

	form = CreateBlogForm()
	return render(request,'create_blog.html',{'form':form})	
