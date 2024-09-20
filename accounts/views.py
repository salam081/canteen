from django.shortcuts import render, redirect
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from .models import *

def registerPage(request):
    departments = Department.objects.all()
    units = Unit.objects.all()
    genders = Gender.objects.all() 
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        othername = request.POST.get('othername')
        username = request.POST.get('username')
        file_no = request.POST.get('file_no')
        phone_number = request.POST.get('phone_number')
        department = request.POST.get('department')
        unit = request.POST.get('unit')
        gender = request.POST.get('gender')
        is_intern = request.POST.get('is_intern') == 'on'
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'index.html', {'departments': departments, 'units': units})

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'index.html', {'departments': departments, 'units': units})
        
        if User.objects.filter(file_no=file_no).exists():
            messages.error(request, 'File No. already exists')
            return render(request, 'index.html', {'departments': departments, 'units': units})

        user_group = UserGroup.objects.get(title='user')

        user = User.objects.create(
            firstname=firstname,lastname=lastname,othername=othername,
            username=username,file_no=file_no,phone_number=phone_number,
            department_id=department,unit_id=unit,gender_id=gender,group=user_group,
            is_intern=is_intern,password=make_password(password1)
        )
        
        messages.success(request, 'User registration successful')
        return redirect('/')
   
    context = {'departments':departments,'units':units,'genders':genders}
    return render(request, 'account/user_register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.group and user.group.title == 'Admin Officer':
                messages.success(request,f'Welcome back {user.username} ')
                return redirect('admin_page')
            
            elif user.group and user.group.title == 'Canteen manager':
                messages.success(request,f'Welcome back {user.username} ')
                return redirect('canteen_manager')
            
            elif user.group and user.group.title == 'Developer':
                messages.success(request,f'Welcome back {user.username} ')
                return redirect('developer_home')
            
            elif user.group and user.group.title == 'Support':
                messages.success(request,f'Welcome back {user.username} ')
                return redirect('developer_home')

            elif user.group and user.group.title == 'User':
                messages.success(request,f'Welcome back {user.username} ')
                return redirect('meal_request')
            
            else:
                return redirect('main/index.html')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'main/index.html')


def logoutPage(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('/')


def add_user_to_group(request, id):
    user = User.objects.get(id=id)
    groups = UserGroup.objects.all().order_by('title')
    if request.method == 'POST':
        User.objects.filter(id=id).update(
            group=request.POST.get('group'))
        messages.success(request, "Updated Successfully!")
        return redirect('index')
    context = {"user": user, "groups": groups}
    return render(request, 'account/add_user_to_group.html', context)


def search_user(request):
    groups = UserGroup.objects.all()
    q = request.GET.get('q', '')

    if q:
        users = User.objects.filter(
            Q(firstname__icontains=q) |
            Q(lastname__icontains=q) |
            Q(file_no__icontains=q) |
            Q(phone_number__icontains=q)
        )
        a = None  
    else:
        users = User.objects.none()  
        a = "Please enter a search parameter!"

    context = {'users': users, 'message': a,"groups": groups}
    return render(request, 'account/search.html', context)


def changePassword(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if not request.user.check_password(old_password):
            messages.error(request, 'Old password is incorrect')
        elif new_password1 != new_password2:
            messages.error(request, 'New passwords do not match')
        else:
            request.user.set_password(new_password1)
            request.user.save()
            # update_session_auth_hash(request, request.user)  # Important to prevent logout
            messages.success(request, 'Password successfully changed')
            return redirect('index')

    return render(request, 'account/change_password.html')


def resetPassword(request,id):
	user = User.objects.get(id=id)
	user.set_password("pass")
	user.save()
	messages.success(request, "Password reset successful!")
	return redirect('index')


def staff_biodata(requuest,id):
    user = requuest.user
    user_id = User.objects.get(id=id)
    return render(requuest,'account/staff_biodata.html',{'user_id':user_id,'user':user})
