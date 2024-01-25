from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm,ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages

# Create your views here.


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
            username = cd['username'],
            password = cd['password']
            )

        if user is not None:
            if user.is_active:
                login(request, user)

                return HttpResponse('Authenticated Successfully')

            else:
                return HttpResponse('Account Disabled')
        return HttpResponse('Invalid Login')

    else:
        form = LoginForm()
    return render(request, 'accounts/login.html',{'form':form})

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html',{'section':'dashboard'})


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # creating a new user
            new_user = user_form.save(commit=False)

            #set the chosen password to enable hashing
            new_user.set_password(
                user_form.cleaned_data['password'])
            #save the user object
            new_user.save()
            #create user profile
            Profile.objects.create(user=new_user)
            return render(request,'accounts/register_done.html',{'new_user':new_user})

    else:
        user_form = UserRegistrationForm()
    return render(request, 'accounts/register.html',{'user_form':user_form})


@login_required
def edit(request):
    if request.method =="POST":
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST)

        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'profile updated successfully')
        else:
            messages.error(request,'Error updating your profile')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)


    return render(request,
    'accounts/edit.html',{'user_form':user_form, 'profile_form':profile_form})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,'accounts/user/list.html',{'users':users})


@login_required
def user_detail(request,username):
    user = get_object_or_404(User,username=username,is_active=True)
    return render(request,'accounts/user/detail.html',{'section':'people','user':user})