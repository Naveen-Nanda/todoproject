# Create your models here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Category(models.Model): # The Category table name that inherits models.Model
	name = models.CharField(max_length=100) #Like a varchar

	class Meta:
		verbose_name = ("Category")
		verbose_name_plural = ("Categories")

	def __str__(self):
		return self.name #name to be shown when called

class Todolist(models.Model): #Todolist able name that inherits models.Model
	title = models.CharField(max_length=250) # a varchar
	content = models.TextField(blank=True) # a text field 
	created = models.DateField(default=timezone.now().strftime("%Y-%m-%d")) # a date
	due_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d")) # a date
	category = models.OneToOneField(Category, on_delete=models.CASCADE, default="general") # a foreignkey
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		ordering = ["-created"] #ordering by the created field

	def __str__(self):
		return self.title #name to be shown when called