from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):

	title = models.CharField(max_length=100)
	author = models.ForeignKey(User,on_delete=models.CASCADE)
	content = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_on']

	def __str__(self):
		return self.title


class UserProfile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	profile = models.ImageField(upload_to='profile',null=True,blank=True)		

	def __str__(self):
		return self.user.first_name + ' profile'