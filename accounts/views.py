from django.shortcuts import render, redirect
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.db.models import Q
from .models import *
from django.contrib.auth.decorators import login_required



def registerPage(request):
    departments = Department.objects.all()
    units = Unit.objects.all()
    genders = Gender.objects.all()
    roles = Role.objects.all() 
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
        role = request.POST.get('role')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'main/index.html', {'departments': departments, 'units': units,'genders':genders,'roles':roles})

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'main/index.html', {'departments': departments, 'units': units,'genders':genders,'roles':roles})
        
        if User.objects.filter(file_no=file_no).exists():
            messages.error(request, 'File No. already exists')
            return render(request, 'main/index.html', {'departments': departments, 'units': units,'genders':genders,'roles':roles})

        user_group = UserGroup.objects.get(title='User')

        user = User.objects.create(
            firstname=firstname,lastname=lastname,othername=othername,
            username=username,file_no=file_no,phone_number=phone_number,
            department_id=department,unit_id=unit,gender_id=gender,group=user_group,
            role_id=role,password=make_password(password1)

        )
        
        messages.success(request, 'User registration successful')
        return redirect('/')
   
    context = {'departments':departments,'units':units,'genders':genders,'roles':roles}
    return render(request, 'account/user_register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome Back {user.username}')

            if user.group and user.group.title == 'Admin Officer':
                return redirect('admin_page')
            
            elif user.group and user.group.title == 'Canteen manager':
                return redirect('pending_meal_requests')
            
            elif user.group and user.group.title == 'User':
                return redirect('meal_request')
            
            elif user.group and user.group.title == 'Developer':
                return redirect('admin_page')
            
            elif user.group and user.group.title == 'Support':
                return redirect('admin_page')
            else:
                return redirect('main/index.html')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('index') 

    return render(request, 'main/index.html')
       
def logoutPage(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('/')


@login_required
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



@login_required
def search_user(request):
    groups = UserGroup.objects.all()
    q = request.GET.get('q', '')

    if q:
        users = User.objects.filter(Q(firstname__icontains=q) | Q(lastname__icontains=q) |
            Q(file_no__icontains=q) |
            Q(phone_number__icontains=q)
        )
        a = None  
    else:
        users = User.objects.none()  
        a = "Please enter a search parameter!"

    context = {'users': users, 'message': a,"groups": groups}
    return render(request, 'account/search.html', context)


@login_required
def changePassword(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if not request.user.check_password(old_password):
            messages.error(request, 'Old password is incorrect')
            return redirect('index')
        elif new_password1 != new_password2:
            messages.error(request, 'New passwords do not match')
            return redirect('index')
        else:
            request.user.set_password(new_password1)
            request.user.save()
            messages.success(request, 'Password successfully changed')
            return redirect('index')

    return render(request, 'account/change_password.html')


@login_required
def resetPassword(request,id):
	user = User.objects.get(id=id)
	user.set_password("pass")
	user.save()
	messages.success(request, "Password reset successful!")
	return redirect('index')


@login_required
def staff_biodata(requuest,id):
    user = requuest.user
    user_id = User.objects.get(id=id)
    return render(requuest,'account/staff_biodata.html',{'user_id':user_id,'user':user})


@login_required
def update_department(request):
    user=User.objects.get(id=request.user.id)
    departments = Department.objects.all().order_by('title')
    # units=Unit.objects.filter(department_id=user.department.id).order_by('title')
    if request.method=='POST':
        # User.objects.filter(id=request.user.id).update(unit_id=request.POST.get('unit'))
        User.objects.filter(id=request.user.id).update(department_id=request.POST.get('department'))
        messages.success(request,"Thanks, your day is blessed!")
        return redirect('update_department')
    context={"user":user,'departments':departments}#"units":units
    return render(request,'account/update_department.html',context)