from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    username = request.user.username  # Get the username of the logged-in user
    return render(request, 'recipe.html', {'username': username})

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def admin_page(request):
    if request.user.is_superuser:
        users = User.objects.all()
        return render(request, 'admin.html', {'users': users})
    else:
        return HttpResponse("You do not have permission to access this page.")

def delete_user(request, user_id):
    if request.user.is_superuser:
        user = User.objects.get(pk=user_id)
        user.delete()
        return redirect('admin')
    else:
        return HttpResponse("You do not have permission to delete users.")