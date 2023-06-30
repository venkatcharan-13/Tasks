from django.shortcuts import render, redirect
from .models import *

from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response


from django.contrib.auth.forms import UserCreationForm

from .forms import CreateUserForm ,CreateAdminUserForm, uploadAdmin ,uploadUserSS
from django.contrib.auth import authenticate, login,logout

from django.contrib.auth.decorators import login_required,user_passes_test

from django.contrib.auth.models import User

from django.contrib import messages

# Create your views here.

def startapp(request):
    return render(request,'start.html')


def adminregisterPage(request):
    form= CreateAdminUserForm()    
    if request.method == "POST":
        form=CreateAdminUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('New Admin Login')
    context={'form':form}
    return render(request,'adminregister.html',context)

def UserregisterPage(request):
    form= CreateUserForm()    
    if request.method == "POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context={'form':form}
    return render(request,'register.html',context)


def UserlogInPage(request):
    if request.method=="POST":
        username=request.POST['emailIdHtml']
        password=request.POST['passwordIdHtml']
        user= authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('user')
    return render(request,'login.html')


def adminLogInPage(request):
    if request.method=="POST":
        username=request.POST['emailIdHtml']
        password=request.POST['passwordIdHtml']
        user= authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('New Admin Page')
    return render(request,'adminlogin.html')


@login_required
def newAdminPage(request):
    if not request.user.is_superuser:
        return HttpResponse('user is not a Superuser')
    else:
        form= uploadAdmin()
        if request.method == 'POST':
            form=uploadAdmin(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request,'|** App was Uploaded Successfully **| ')
    
        context={
            'form':form
            }
        return render(request,'admin.html',context)
 


@login_required(login_url='login')
def newUserPage(request):
    uid=User.objects.get(pk = request.user.id)
    name=uid.username
    form=uploadUserSS()
    if request.method == "POST":
        form=uploadUserSS(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'|** ScreenShot was Uploaded Successfully **| ')
        
    context={
        'form':form,
        'userId':name
        }  
    return render(request,'user.html',context)



class appInfo(APIView):
    def get(self, request, format=None):
        uid=User.objects.get(pk = request.user.id)
        ob=adminAddApp.objects.filter(userId=uid).values()
        appInfoResponse=[]
        for i in ob:
            temp={
                'user_apps_id':i['userId_id'],
                "user_app_name":i['appName'],
                "user_app_points":i['adminAppPoints'],
                "user_app_image":i['adminAppImage'],
                "app_id":i['id']
            }
            appInfoResponse.append(temp)
        
        return Response(appInfoResponse)


@login_required(login_url='login')
def taskPage(request):
    uid=User.objects.get(pk = request.user.id)
    name=uid.username
    context={
        'userId':name
    }
    return render(request,'task.html',context)



@login_required(login_url='login')
def profilePage(request):
    ob=User.objects.get(pk = request.user.id)
    context={
        'first_name':ob.first_name,
        'last_name': ob.last_name,
        'email':ob.email,
        'user_name':ob.username,
        'userId':ob.username
    }
    print(context)
    return render(request,'profile.html',context)



class tpInfo(APIView):
    def get(self, request, format=None):
        ob=userAppTask.objects.filter(userappid=request.user.id).exclude(userAppImage='').values()
        taskinfo=[]
        total_app_points=0
        for i in ob:
            temp={
                "app_id":i['id'],
                "user_app_name":i['userAppName'],
                "user_app_points":i['userAppPoints'],
                "task_completed":' Task Completed '
            }
            total_app_points+=i['userAppPoints']
            taskinfo.append(temp)
        taskinfo.append(total_app_points)
        return Response(taskinfo)
    
    
@login_required(login_url='login')
def pointsPage(request):
    uid=User.objects.get(pk = request.user.id)
    name=uid.username
    context={
        'userId':name
    }
    return render(request,'points.html',context)



def logOutPage(request):
    logout(request)
    return redirect('login')