from django.db.models import query
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.forms import SignupForm, TaskModelForm, UserUpdateForm, ProfileUdateForm
from app.models import TaskModel


def signin(request):
    if not request.user.is_authenticated:
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
    else:
        return redirect('home')

def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            signup_form = SignupForm(request.POST)
            if signup_form.is_valid():
                signup_form.save()
                messages.success(request, 'Your accout has been created! You are now able to log in')
            return redirect('signin')
        else:
            signup_form = SignupForm()
        return render(request, 'app/signup.html', {'forms': signup_form})
    else:
        return redirect('home')

@login_required(login_url='signin')
def signout(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('signin')

@login_required(login_url='signin')
def home(request):
    model_form = TaskModelForm()
    tasks = TaskModel.objects.filter(user=request.user).order_by('status')
    print('inc_count: ', TaskModel.objects.filter(user=request.user, status=False).count())
    inc_count = TaskModel.objects.filter(user=request.user, status=False).count()
    return render(request, 'app/home.html', context={'form': model_form, 'tasks': tasks, 'inc_count': inc_count})

@login_required(login_url='signin')
def addTask(request):
    print('User: ', request.user)
    form = TaskModelForm(request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        save_todo = form.save(commit=False)
        save_todo.user = request.user
        save_todo.save()
        print(save_todo.user, save_todo)
        messages.success(request, 'Task Added Successfully')
        return redirect('home')
    else:
        return render(request, 'app/addTask.html', context={'form': form})

@login_required(login_url='signin')
def updateTask(request, pk):
    print('User: ', request.user)
    task = TaskModel.objects.get(pk=pk)
    print('task: ', task)
    form = TaskModelForm(instance=task)
    # print('form: ', form)
    if request.method == 'POST':
        form = TaskModelForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task Updated Successfully')
            # print(form.user, form)  -->  AttributeError: 'TaskModelForm' object has no attribute 'user'
        return redirect('home')
    else:
        return render(request, 'app/updateTask.html', context={'form': form})

@login_required(login_url='signin')
def deleteTask(request, pk):
    print('Delete ID: ', pk)
    task = TaskModel.objects.get(pk=pk)
    title = task.title
    task.delete()
    messages.success(request, f'Task ({title}) Deleted Successfully')
    return redirect('home')

@login_required(login_url='signin')
def changeStatus(request, pk, status):
    print('ID STATUS : ', pk, status)
    task = TaskModel.objects.get(pk=pk)
    if status == 'False':
        task.status = True
    else:
        task.status = False
    task.save()
    return redirect('home')

@login_required(login_url='signin')
def searchTask(request):
    if request.method == 'GET':
        q = request.GET.get('q')
        print('q: ', q)
        results = TaskModel.objects.all().filter(user=request.user, title__icontains=q)
        print('results: ', results)
        return render(request, 'app/searched.html', context={'results': results})
    else:
        return redirect('home')

@login_required(login_url='signin')
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUdateForm(request.POST, request.FILES, instance=request.user.profilemodel)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUdateForm(instance=request.user.profilemodel)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'app/profile.html', context)

# Change password with OLD password
@login_required(login_url='signin')
def changePassword(request):
    if request.method == 'POST':
        pcf = PasswordChangeForm(user=request.user, data=request.POST)
        if pcf.is_valid():
            pcf.save()
            update_session_auth_hash(request, pcf.user)
            messages.success(request, 'Password Changed Successfully')
            return redirect('profile')
    else:
        pcf = PasswordChangeForm(user=request.user)
    # print(pcf)
    return render(request, 'app/changePassword.html', {'pcf': pcf})
