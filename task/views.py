from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'task/home.html')


def register(request):
    if request.method == 'GET':
        return render(request, 'task/register.html', {'form': UserCreationForm()})
    elif request.method == 'POST':
        try:
            u = User.objects.create_user(request.POST['user'], password=request.POST['pass1'])
            u.save()
            login(request, u)
            return redirect('currenttasks')
        except IntegrityError:
            return render(request, 'task/register.html', {'form': UserCreationForm(), 'error': 'That username already exists. Please choose a different username.'})
        

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'task/loginuser.html', {'form': AuthenticationForm()})
    elif request.method == 'POST':
        u = authenticate(request, username=request.POST['user'], password=request.POST['pass'])
        if u is None:
            return render(request, 'task/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username and password wrong.'})
        else:
            login(request, u)
            return redirect('currenttasks')


@login_required
def newtask(request):
    if request.method == 'GET':
        return render(request, 'task/newtask.html', {'form': TaskForm()})
    elif request.method == 'POST':
        try:
            form = TaskForm(request.POST)
            newTask = form.save(commit=False)
            newTask.user = request.user
            newTask.save()
            return redirect('currenttasks')
        except ValueError:
            return render(request, 'task/newtask.html', {'form': TaskForm(), 'error': TaskForm(request.POST)})


@login_required
def currenttasks(request):
    task_list = Task.objects.filter(user=request.user, completiondate__isnull=True)
    return render(request, 'task/currenttasks.html', {'tasks': task_list})

@login_required
def importanttasks(request):
    task_list = Task.objects.filter(user=request.user, priority=True, completiondate__isnull=True)
    return render(request, 'task/importanttasks.html', {'tasks': task_list})

@login_required
def completedtasks(request):
    task_list = Task.objects.filter(user=request.user, completiondate__isnull=False).order_by('-completiondate')
    return render(request, 'task/completedtasks.html', {'tasks': task_list})


@login_required
def updatetask(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if request.method == 'GET':
        f = TaskForm(instance=task)
        return render(request, 'task/update.html', {'task': task, 'form': f})
    elif request.method == 'POST':
        try:
            f = TaskForm(request.POST, instance=task)
            f.save()
            return redirect('currenttasks')
        except ValueError:
            return render(request, 'task/update.html', {'task': task, 'form': f, 'error': 'Try again.'})


@login_required
def completetask(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if request.method == 'POST':
        task.completiondate = timezone.now()
        task.save()
        return redirect('currenttasks')


@login_required
def deletetask(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('currenttasks')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')