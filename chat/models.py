from random import randrange
from django import forms
from django.db import models
# Create your models here.
class groupName(models.Model):
    groupname = models.CharField(max_length=200,null=False,blank=False)
    username1 = models.CharField(max_length=200,null=True)
    username2 = models.CharField(max_length=200,null=True)
    used = models.BooleanField(default=False)
    def __str__(self):
        return self.groupname

class privateChat(models.Model):
    groupname = models.CharField(max_length=200,null=False,blank=False)
    password = models.CharField(max_length=30,null=False,blank=False)
    noOfUsers = models.IntegerField(null=False,default=1)
    def __str__(self):
        return self.groupname



