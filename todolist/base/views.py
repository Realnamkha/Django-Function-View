from email.policy import default
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from django.contrib import messages
from django.db.models import Q
# Create your views here.


# def register(request):
#     form = UserCreationForm()
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.username = user.username.lower()
#             user.save()
#             login(request,user)
#             return redirect('home')
#         else:
#             messages.error(request, 'An error occured')
#     context = {'form':form}
#     return render(request,'base/register.html',context)


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        name = request.POST.get('username')
        passcode = request.POST.get('password')
        user = authenticate(request, username=name, password=passcode)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist.')
    return render(request, 'base/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')

def userProfile(request):
    context = {}
    return render(request,'base/profile.html',context)

@login_required(login_url=('login'))
def home(request):
    user = request.user
    tasks = user.task_set.all()
    q = request.GET.get('q') or ''
    if q:
        tasks = tasks.filter(
        Q(title__icontains=q) |
        Q(desc__icontains=q)
        )
    task_count = tasks.filter(complete=False).count()
    context = {'tasks': tasks,'task_count':task_count}
    return render(request, 'base/home.html', context)

@login_required(login_url=('login'))
def createTask(request):
    form = TaskForm()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/task_form.html', context)

@login_required(login_url=('login'))
def updateTask(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/task_form.html', context)

@login_required(login_url=('login'))
def deleteTask(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('home')
    context = {'task': task}
    return render(request, 'base/delete.html', context)
