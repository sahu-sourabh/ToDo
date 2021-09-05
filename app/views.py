from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.forms import SignupForm, TaskModelForm
from app.models import TaskModel


def signin(request):
    if request.method == 'POST':
        auth_form = AuthenticationForm(request=request, data=request.POST)
        if auth_form.is_valid():
            username = auth_form.cleaned_data['username']
            password = auth_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('home')
    else:
        auth_form = AuthenticationForm()
    return render(request, 'app/signin.html', {'forms': auth_form})

def signup(request):
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            messages.success(request, 'Your accout has been created! You are now able to log in')
        return redirect('signin')
    else:
        signup_form = SignupForm()
    return render(request, 'app/signup.html', {'forms': signup_form})

def signout(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('signin')

@login_required(login_url='signin')
def home(request):
    if request.user.is_authenticated:
        model_form = TaskModelForm()
        tasks = TaskModel.objects.filter(user=request.user).order_by('status')
        return render(request, 'app/home.html', context={'form': model_form, 'tasks': tasks})
    else:
        return redirect('signin')

@login_required(login_url='signin')
def addTodo(request):
    if request.user.is_authenticated:
        print('User: ', request.user)
        form = TaskModelForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            save_todo = form.save(commit=False)
            save_todo.user = request.user
            save_todo.save()
            print(save_todo.user, save_todo)
            return redirect('home')
        else:
            return render(request, 'app/home.html', context={'form': form})

def deleteTodo(request, pk):
    print('Delete ID: ', pk)
    TaskModel.objects.get(pk=pk).delete()
    return redirect('home')

def changeStatus(request, pk, status):
    print('ID STATUS : ', pk, status)
    task = TaskModel.objects.get(pk=pk)
    if status == 'False':
        task.status = True
    else:
        task.status = False
    task.save()
    return redirect('home')
