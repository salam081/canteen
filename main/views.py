from django.shortcuts import render,redirect,get_object_or_404
from accounts.models import *
from django.contrib import messages
from datetime import datetime
from django.db.models.functions import Cast
from django.db.models import DateField
import json
import ast
from django.utils import timezone
from django.utils.timezone import localtime
from .models import *
from .forms import *

# Create your views here.


def index(request):
    departments = Department.objects.all()
    units = Unit.objects.all()
    genders = Gender.objects.all()
    context = {'departments':departments,'units':units,'genders':genders}
    return render(request, 'main/index.html', context)



def admin_page(request):
    current_user = request.user
    current_date = timezone.now().date()

    dates_selected = Roster.objects.filter(user=current_user, date=current_date).exists()
    users = User.objects.none()
    if current_user.department: #and current_user.unit:
        users = User.objects.filter(department=current_user.department,group__title = 'User' )#unit=current_user.unit
    
    users_with_status = []
    for user in users:
        has_dates_selected = Roster.objects.filter(user=user, date=current_date).exists()
        users_with_status.append({'user': user,'has_dates_selected': has_dates_selected})
    context = {'users_with_status': users_with_status, 'dates_selected': dates_selected}
    
    return render(request, 'main/admin_page.html', context)


    
def canteen_manager(request):
    meals = Meal.objects.all()
    category = Category.objects.all()  

    if request.method == 'POST':
        meal_id = request.POST.get('meal_id')

        title = request.POST.get('title')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        # available logic
        if 'availability' in request.POST:
            meal = get_object_or_404(Meal, id=meal_id)
            meal.available = not meal.available
            meal.save()
            messages.success(request, 'Meal  updated successfully')
            return redirect('canteen_manager')

        # Editing  meal logic
        if meal_id:  
            meal = get_object_or_404(Meal, id=meal_id)
            meal.title = title
            meal.price = price
            meal.category_id = category_id
            meal.save()
        # Creating  meal logic    
        else:  
            meal = Meal.objects.create(title=title,price=price,category_id=category_id,available=True)
            meal.save()
        meal.save()
        messages.success(request, 'Meal updated successfully' if meal_id else 'Meal added successfully')
        return redirect('canteen_manager')

    context = {'meals': meals, 'category': category}
    return render(request, 'main/canteen_manager.html', context)


def delete_meal(request,id):
    delete_meal = Meal.objects.get(id=id)
    delete_meal.delete()
    messages.success(request,'Meal Deleted  successfully')
    return redirect('canteen_manager')


def meal_request(request):
    user = request.user
    today = timezone.now().date()
    weekday = today.weekday()
    
    on_call = Roster.objects.filter(user=user, date=today).exists()
    

    if request.method == 'POST':
        if not on_call:
            messages.error(request, 'You are not on call today')
            return redirect('meal_request')

        meal_Obj = request.POST.getlist('meal_id')
        if meal_Obj:
            requests_today = Request.objects.filter(user=user, date_created__date=today)
            # Monday to Friday
            if weekday < 5:  
                if requests_today.exists():
                    messages.error(request, 'You can only make one meal request per day .')
                    return redirect('meal_request')
            else:  # Saturday and Sunday
                if requests_today.count() >= 2:
                    messages.error(request, 'You can only make two meal requests per day on Saturday and Sunday.')
                    return redirect('meal_request')

            new_request = Request.objects.create(user=user)
            try:
                for meal_id in meal_Obj:
                    meal = Meal.objects.get(id=meal_id)
                    RequestDetails.objects.create(request=new_request, meal=meal)
                messages.success(request, 'Meal request successful.')
                return redirect('meal_request')
            except Meal.DoesNotExist:
                messages.error(request, 'meals do not exist.')
                new_request.delete()
                return redirect('meal_request')
        else:
            messages.error(request, 'Invalid meal selection.')
    meals = Meal.objects.all()
    food_meal = Meal.objects.filter(category__title='Food')
    protein_meal = Meal.objects.filter(category__title='Protein')
    drink_meal = Meal.objects.filter(category__title='Drink')

    context = {
        'meals': meals,
        'food_meal': food_meal , 
        'protein_meal': protein_meal,
        'drink_meal': drink_meal,
        'on_call': on_call , 
        # 'user_request': user_request , 
    }
    return render(request, 'main/meal_request.html', context)


def add_staff_on_call(request):
    if request.method == 'POST':
        user_id = request.POST.get('user')
        user = User.objects.get(id=user_id)
        get_dates = request.POST.get('date_id')  
            # Convert the string  of the list into an actual list
        date_list = ast.literal_eval(get_dates)
        
        success_dates = []
        warning_dates = []

        for date_str in date_list:
            if date_str:
                try:
                    date_obj = datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
                    if Roster.objects.filter(user=user, date__year=date_obj.year, date__month=date_obj.month, date__day=date_obj.day).exists():
                        warning_dates.append(date_obj.strftime('%Y-%m-%d'))
                    else:
                        Roster.objects.create(user=user, date=date_obj)
                        success_dates.append(date_obj.strftime('%Y-%m-%d'))
                except ValueError as e:
                    print(f"ValueError for date: {date_str}. Error: {str(e)}")  # Debug log
                    messages.error(request, f'Invalid date format: {date_str}')
                    return redirect('admin_page')

        if warning_dates:
            messages.warning(request, f"Dates  already exist for: {', '.join(warning_dates)}")
        if success_dates:
            messages.success(request, f"Dates  added successful for {user.firstname}")
        return redirect('admin_page')

    return redirect('admin_page')

def user_roster(request):
    current_month = timezone.now().month
    current_year = timezone.now().year
    user_call_dates = Roster.objects.filter(user=request.user, date__month=current_month, date__year=current_year).values_list('date', flat=True)
    
    return render(request, 'main/user_roster.html', {'user_call_dates': user_call_dates})    


def edit_meal_request(request, id):
    meal_request = get_object_or_404(RequestDetails, id=id)
    form = EditRequestForm(instance=meal_request)
    
    if request.method == 'POST':
        form = EditRequestForm(request.POST, instance=meal_request)
        if form.is_valid():   
            form.save()  
            return redirect('meal_request_details')    
    context = {'form': form}
    return render(request, 'main/edit_meal_request.html', context)


def meal_request_details(request):
    form = EditRequestForm()
    user = request.user
    current_day = timezone.now().date()
    user_request = Request.objects.annotate(date_only=Cast('date_created', DateField())).filter(user=request.user, date_only=current_day)
    
    user_request_details = RequestDetails.objects.filter(request__in=user_request)
    context={'user_request_details': user_request_details,'form':form}
    return render(request,'main/user_request_details.html',context)


def delete_meal_request(request, id):
    user = request.user
    requestObj = RequestDetails.objects.get(id=id)
    requestObj.delete()
    messages.success(request,'Meal Deleted Successfully')
    return redirect('meal_request_details')


def meal_request_list(request):
    requests = Request.objects.all()
    context = {'requests': requests}
    return render(request, 'main/pending_meal_requests.html',context)



def pending_meal_requests(request):
    requests = Request.objects.filter(status='Pending')
    context = {'requests': requests}
    return render(request, 'main/pending_meal_requests.html', context)


def approve_meal_request(request, id):
    user_request = Request.objects.get( id=id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            if user_request.status != 'Pending':
                messages.error(request, "This request cannot be approved.")
                return redirect('pending_meal_requests')
            
            user_request.status = 'Approved'
            messages.success(request, "Request approved successfully.")
        
        elif action == 'decline':
            if user_request.status != 'Pending':
                messages.error(request, "This request cannot be declined.")
                return redirect('pending_meal_requests')
            
            user_request.status = 'Decline'
            messages.success(request, "Request declined successfully.")
        
        else:
            messages.error(request, "Invalid action.")
            return redirect('pending_meal_requests')
        
        user_request.save()
        return redirect('pending_meal_requests')  
    return redirect('pending_meal_requests')

def update_user_roster(request, id):
    current_month = timezone.now().month
    current_year = timezone.now().year

    user = User.objects.get(id=id)
    user_on_call_dates = list(Roster.objects.filter(user=user, date__month=current_month, date__year=current_year).values_list('date', flat=True))
    date_to_remove = request.GET.get('remove_date')
    if date_to_remove:
        try:
            date_to_remove = timezone.datetime.strptime(date_to_remove, '%Y-%m-%d').date()
            if date_to_remove in user_on_call_dates:
                user_on_call_dates.remove(date_to_remove)
               
                Roster.objects.filter(user=user, date=date_to_remove).delete()
        except ValueError:
            pass
        messages.success(request, f"Dates  remove successful for {user.firstname}")
        return redirect('admin_page')
    formatted_dates = [date.strftime('%Y-%m-%d') for date in user_on_call_dates]
    return render(request, 'main/update_user_roster.html', {'user': user, 'user_on_call_dates': formatted_dates})