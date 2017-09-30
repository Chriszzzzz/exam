from __future__ import unicode_literals
from django.db import models
import bcrypt
from datetime import datetime

class UserManager(models.Manager):
	def reg_validator(self,postData):
		errors = {}
		if "name" not in postData or len(postData['name'])<3:
			errors['name'] = "Please enter a valid name"
		if "username" not in postData or len(postData['username'])<3:
			errors['username'] = "Please enter a valid username"
		if 'password' not in postData or len(postData['password'])<8:
			errors['password'] = "Password must have at least 8 characters"
		elif "confirm" not in postData or postData['password'] != postData['confirm']:
			errors['password'] = "Please enter your password again"
		if not len(errors):
			user = User.objects.filter(username = postData['username'])
			if len(user):
				errors['username'] = "Please enter a valid username"
		return errors

	def login_check(self,postData):
		error = {}
		user = User.objects.filter(username = postData['username'])
		if not user or not bcrypt.checkpw(postData['password'].encode(),user[0].password.encode()):
			error['login'] = "Username and password not match"
		return error

	def password_crypt(self,password):
		return bcrypt.hashpw(password.encode(),bcrypt.gensalt())

class ListManager(models.Manager):
	def additem(self, postData, request):
		errors = []
		if len(postData['item']) < 4:
			errors.append('item name should be more than 3 characters')

		if errors:
			return {'status': False, 'errors': errors}
		else:
			user = User.objects.get(id=request.session['user_id'])
			Wishlists.objects.create(item=postData['item'], user=user, author=user)
			return {'status': True, 'errors': errors}

class User(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()


class Wishlists(models.Model):
	item = models.CharField(max_length=45)
	user = models.ForeignKey(User, related_name='AddedBy')
	author = models.ForeignKey(User, related_name='author')
	createdAt = models.DateTimeField(auto_now_add=True)
	updatedAt = models.DateTimeField(auto_now=True)
	objects = ListManager()