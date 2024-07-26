from django.db import models

# Create your models here.
from django.db import models
import re
import bcrypt
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.

class UserManager(models.Manager):
    def basic_register(self, postData): # function for registration 
        errors = {}
        if len(postData['first_name']) < 2:# validated first name
            errors["first_name"] = "First Name should be at least 2 characters"## as list ""if satament
            # errors["first_name"].append=('')
        if len(postData['last_name']) < 2:# validated last name
            errors["last_name"] = "Last Name should be at least 2 characters"
        # validated dob to required in database and age grater than 13      
        #validated format of mail and unique email used
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):             
            errors['email'] = "Invalid email address!"
        if User.objects.filter(email=postData['email']).exists():
            errors['email_used'] = "Email already in use!"
        # validated pass to be greater than 8 char and match with confirm pass 
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirm_pw']:
            errors["confirm_pw"] = "Passwords are not match "
        return errors
    
    def basic_login(self, postData):# function for login 
            errors = {}
            try:
                user = User.objects.get(email=postData['email'])
            except ObjectDoesNotExist:
                errors['email'] = "Email not found."
                return errors
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['password'] = "Invalid password."
            return errors

class PieManager(models.Manager):
    def basic_form_pie(self, postData): # validation for form of  
        errors = {}
        if not postData['name']:# validated name of pie
            errors["name"] = "Please include the name"
        if Pie.objects.filter(name=postData['name']).exists():
            errors['uniq'] = "Name already in use!"
        if not postData['filling']:# validated filling of pie
            errors["filling"] = "Please include the filling"
        if not postData['crust']:# validated crust of pie
            errors["crust"] = "Please include the crust"
        return errors
#table of user
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=225)
    password = models.CharField(max_length=50)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
#table of pie
class Pie(models.Model):
    name = models.CharField(max_length=50)
    filling = models.CharField(max_length=50)
    crust = models.CharField(max_length=50)
    users_who_vote = models.ManyToManyField(User,related_name='vote_pies')
    uploaded_by = models.ForeignKey(User,related_name='pies_uploaded',on_delete=models.CASCADE)
    objects = PieManager()




# session for user
def get_user(session):
    return User.objects.get(id=session['user_id'])
#check user mail
def check_email(POST):
    return User.objects.filter(email=POST['email'])
# create user 
def create_user(POST):
    password = POST['password']
    return User.objects.create(
        first_name=POST['first_name'],
        last_name =POST['last_name'],
        email=POST['email'],
        password= bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(),
        )

#create pie with ForeignKey key for user in session
def create_pie(POST,session):
    return Pie.objects.create(
        name=POST['name'],
        filling =POST['filling'],
        crust =POST['crust'],
        uploaded_by=get_user(session),
        )
#get all pies
def all_pies():
    return Pie.objects.all()

#get pie base on id
def pie(id):
    return Pie.objects.get(id=id)

#get user base in id
def user(id):
    return User.objects.get(id=id)

# update the information about pie
def update_pie(POST,id):
    pie=Pie.objects.get(id=id)
    pie.name=POST['name']
    pie.filling=POST['filling']
    pie.crust=POST['crust']
    pie.save()

# delete the pie
def delete_pie(POST):
    pie_remove=Pie(POST['id_pie'])
    pie_remove.delete()


# add vote with add id of pie to id of user
def like(session,id):
    user = get_user(session)
    pie = Pie.objects.get(id=id)
    pie.users_who_vote.add(user)
    

#remove vote with remove id of pie to id of user
def unlike(session,id):
    user = get_user(session)
    pie = Pie.objects.get(id=id)
    pie.users_who_vote.remove(user)
    