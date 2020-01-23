from __future__ import unicode_literals
from django.db import models
import datetime
import bcrypt
import re

# Create your models here.
class UserManager(models.Manager):
    def login_validator(self, postData):
        errors = {}
        # Regex checks the format of the input.
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email address!"
        # a list of emails.  Should only ever go to one
        emailCheck = User.objects.filter(email=postData['email'])
        

        # define checks here
        # Checks for any matching emails.  We need one in order to get through
        if len(emailCheck) < 1:
            errors['email'] = "Email doesn't match any found in our records."
            print('email is bad')
        # if TU != None prevents exceptions in the case that an email is no good.
        target_user = emailCheck.first()
        if target_user != None:
            # compares hashed PWORDS
            if bcrypt.checkpw(postData['password'].encode(), target_user.password.encode()):
                pass
            else:
                errors['bad'] = "Your password was incorrect."
                print("the password is bad")
        return(errors)
        

    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['f_name']) < 2:
            errors['f_name'] = "First name too short!"
        if len(postData['l_name']) < 2:
            errors['l_name'] = "Last name too short!"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email address!"
        if len(postData['password']) < 8:
            errors['password'] = "Your password is too short dude!"
        if postData['password'] != postData['password_conf']:
            errors['password_conf'] = "Your password must match the confirmation!"
        return errors
    pass

class TripManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        
        dest = postData['dest']
        plan = postData['plan']
        start_date = postData['start_date']
        end_date = postData['end_date']
        today = int(datetime.date.today().strftime("%Y%m%d"))
        print(today)

        startNum = ""
        endNum = ""

        for char in start_date:
            if char != "-":
                startNum += char

        endNum = ""
        for char in end_date:
            if char != "-":
                endNum += char
        startNum = int(startNum)
        endNum = int(endNum)

        if start_date == "":
            errors['start_date'] = "You must enter a start date!"
        elif startNum < today:
            errors['time_travel1'] = "You can't time travel"

        print(startNum)
        print(endNum)
        if end_date == "":
            errors['end_date'] = "You must enter a end date!"
        elif endNum < startNum:
            errors['time_travel2'] = "Even if you wanted to, you can't time travel"

        if len(dest) < 3:
            errors['dest'] = "Your destination must have more than 3 letters."
        if len(plan) < 3:
            errors['plan'] = "Your plan must have more than 3 letters."
        return errors
        

### Models here
class User(models.Model):
    f_name = models.CharField(max_length=45)
    l_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    dest = models.CharField(max_length=45)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField()
    made_by = models.ForeignKey(User, related_name="trips_made", on_delete=models.CASCADE)
    joined_by = models.ManyToManyField(User, related_name="trips_joined")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()