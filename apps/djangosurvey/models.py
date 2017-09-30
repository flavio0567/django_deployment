from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import bcrypt
import re

# Create your models here.
passwd_regex = re.compile(r'^[a-zA-Z]+$')
name_regex = re.compile(r'^[a-zA-Z0-9_]+( [a-zA-Z0-9_]+)*$')


class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        # name and username validation
        if len(postData['name']) < 3: 
            errors["name"] = "Please enter a valid name - at least 3 characters."
        if not name_regex.match(postData['name']):
            errors["name"] = "Name must contain at least characters."
        if len(postData['username']) < 3: # or not name_regex.match(postData['username']):
            errors["username"] = "Please enter a valid username - at least 3 characters."
        # username validation
        valid_username = User.objects.filter(username = postData['username'])
        if len(valid_username):
            errors["username"] = "There is already an account created with this username. Please either login in using this username, or create an account with a different one."
        # password validation
        if len(postData['passwd1']) < 8:
            errors["password"] = "Please enter a valid name - at least 3 characters."
        if not passwd_regex.match(postData['passwd1']):
            errors["password"] = "Password must contain at least characters."
        else:
            if postData['passwd1'] != postData['passwd2']:
                errors["password"] = "Password did not match. Please try again."
        # return error messages
        return errors


    def login_validator(self, postData):
        context = {'errors' : {}, 'user_name': {}, 'user_id': {}}
        errors = {}
        # validate username
        if postData['username']  == "":
            errors["username"] = "Please enter a valid username"
        if len(postData['username'])  < 3:
            errors["username"] = "Please enter a valid username"
        # validate password
        if postData['passwd']  == "":
            errors["password"] = "Please enter a valid password"
        if len(postData['passwd'])  < 8:
            errors["password"] = "Invalid password, please try again"
            context['errors'] = errors
            return context
        else:
            # user validation
            try:
                user = User.objects.get(username = postData['username'])
            except:
                errors["username"] = "Username not registered, try again."
                context['errors'] = errors
                return context
            if not bcrypt.checkpw(postData['passwd'].encode(), user.password.encode()):
                errors["username"] = "Authentication failed, try again."
                context['errors'] = errors
                return context
            else:
                context['user_name'] = User.objects.get(username = postData['username']).name
                context['user_id'] = User.objects.get(username = postData['username']).id
        # return error messages
        return context


class ItemManager(models.Manager):
    def item_validator(self, postData):
        errors = {}
        # description validation
        if postData['description'] == "":
            errors["description"] = "Please enter a valid description - not a empty field"
        if len(postData['description']) < 3: # or
            errors["description"] = "Please enter a valid description - at least 3 characters."
        if not name_regex.match(postData['description']):
            errors["description"] = "Description must contain at least characters."
        # return error messages
        return errors


class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    dt_hired = models.DateTimeField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return "id: {} name: {} username: {} dt_hired {}".format(
            self.id,
            self.name,
            self.username,
            self.dt_hired)


class Item(models.Model):
    description = models.CharField(max_length=255)
    item_dt_added = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, related_name = 'wish')
    added_by = models.ForeignKey(User, related_name = 'user')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ItemManager()
    def __str__(self):
        return "{} {} {} {} {}".format(
            self.description,
            self.item_dt_added,
            self.added_by)
