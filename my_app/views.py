from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages

# Create your views here.
#render the main page
def index(request):
    return render(request,'Pies.html')

#check if the user not in session can't tgo to success page
def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': get_user(request.session),
            'pies':all_pies(),
            'users':User.objects.all()
        }
        return render(request,'dashboard.html',context)

#handel request post to registration, and pass data to the method to it there are an error shown a msg and redirect to registration page, else create the data and go to the success
def registration(request):
    if request.method == 'POST':
        errors = User.objects.basic_register(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():   
                messages.error(request, value)    
            return redirect('/')
        else:
            user = create_user(request.POST)
            request.session['user_id'] = user.id
            messages.success(request, "Successfully Registered")
            return redirect('/dashboard')
    return redirect('/')


#handel request post to login by user email, and pass data to the method if there are an error display a msg and redirect to main page, else create the data and go to the success page
def login(request):
    if request.method == 'POST':
        errors = User.objects.basic_login(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        
        user = check_email(request.POST)  
        if user: 
            logged_user = user[0] 
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/dashboard')
        messages.success(request, "Successfully logged in")
        return redirect('/dashboard')
    else:
        return redirect('/')

# clear the session of user to logout
def logout(request):
    if request.method=='POST':
        request.session.clear()
        return redirect('/')
    

#__________ Pie

#handel request post to add a pi by user , and pass data to the table to shown  if there are an error display a msg and redirect to dashboard page, else create the data 
def add_pie(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == 'POST':
        errors = Pie.objects.basic_form_pie(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():   
                messages.error(request, value)    
            return redirect('/dashboard')
        else:
            create_pie(request.POST,request.session)
            return redirect('/dashboard')
### editPage


    
# # handel request post to edit by information base in database of pie edit pie with recall post request form models and validate
def edit_pie(request,id):
    context={
    'pie':pie(id),
    'user': get_user(request.session)
    }    
    if request.method == 'POST':
        errors = Pie.objects.basic_form_pie(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():   
                messages.error(request, value)    
            return redirect(f'/pies/edit/{id}')
        else:
            update_pie(request.POST,id)
            return redirect(f'/dashboard')
    else:
        return render(request,'edit.html',context)

#remove pie from the user session
def remove_pie(request):
    if request.method =='POST':
        delete_pie(request.POST)
        return redirect('/dashboard')
    
# table show all pies from all users
def show_pies(request):
    context={
        'pies':all_pies(),
        'user': get_user(request.session)

    }
    return render(request,'show_pies.html',context)
# add vote and count it in html
def vote(request,id):
    context={
    'pie':pie(id),
    'user': get_user(request.session)

    }
    return render(request,'vote.html',context)

# add delicaious
def add_delicious(request, id):
    if request.method == 'POST':
        like(request.session, id)
        messages.success(request, "Vote!")
        return redirect('/pies')

#remove delicious

def remove_delicious(request, id):
    if request.method == 'POST':
        unlike(request.session, id)
        messages.success(request, "Remove Vote!")
        return redirect('/pies')