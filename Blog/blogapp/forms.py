from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Blog, UserProfile

class UserSignupForm(forms.ModelForm):

    cnf_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password']
        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control'}),
            'first_name' : forms.TextInput(attrs={'class':'form-control'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control'}),
            'email' : forms.EmailInput(attrs={'class':'form-control'}),
            'password' : forms.PasswordInput(attrs={'class':'form-control'})
        }

    def clean_email(self):
    	email = self.cleaned_data['email']
    	user = User.objects.filter(email=email)
    	if user.exists():
    		raise forms.ValidationError("This Email Already Registerd")
    	return email

    def clean_username(self):
    	username = self.cleaned_data['username']
    	user = User.objects.filter(username=username)
    	if user.exists():
    		raise forms.ValidationError('This Username Already Taken')
    	return username

    def clean_password(self):
    	global password
    	password = self.cleaned_data['password']
    	if len(password) == 8 and password.isalnum():
    		return password
    	raise forms.ValidationError('Password must be alpha numeric and has length of 8')

    def clean_cnf_password(self):
    	cnf_password = self.cleaned_data['cnf_password']
    	if password == cnf_password:
    		return cnf_password
    	else:
    		raise forms.ValidationError('Password Not Match')



class UserLoginForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ['email','password']
		widgets = {
            'email' : forms.EmailInput(attrs={'class':'form-control'}),
            'password' : forms.PasswordInput(attrs={'class':'form-control'})
        }

	def clean_email(self):
		global email
		email = self.cleaned_data['email']
		user = User.objects.filter(email=email)
		if user.exists():
			return email
		raise forms.ValidationError('Wrong Email')

	def clean_password(self):
		password = self.cleaned_data['password']
		user_obj = User.objects.filter(email=email)
		if user_obj.exists():
			username = user_obj[0].username
			user = authenticate(username=username,password=password)
			if user:
				return password
			else:
				raise forms.ValidationError('Wrong Password')
		return password			
			

class CreateBlogForm(forms.ModelForm):
	
	class Meta:
		model = Blog
		fields = ['title','content']
		widgets = {
			'title' : forms.TextInput(attrs={'class':'form-control'}),
			'content' : forms.Textarea(attrs={'class':'form-control'})
		}  		


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['profile']
        widgets = {
            'profile' : forms.FileInput(attrs={'class':'form-control'})
        }