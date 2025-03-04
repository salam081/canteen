from django.shortcuts import render,redirect,get_object_or_404
from accounts.models import *
from django.contrib import messages
from datetime import datetime
from django.db.models.functions import Cast
from django.db.models import DateField
import ast
from django.utils import timezone
from django.utils.timezone import localtime
import holidays
from decimal import Decimal
from django.db.models import Sum
from .models import *
from .forms import *
from .decorators import group_required
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    departments = Department.objects.all()
    units = Unit.objects.all()
    genders = Gender.objects.all()
    roles = Role.objects.all()
    context = {'departments':departments,'units':units,'genders':genders, 'roles':roles}
    return render(request, 'main/index.html', context)


def about(request):
    context = {
        'departments':Department.objects.all(),
        'units':Unit.objects.all(),
        'genders':Gender.objects.all(),
        'roles':Role.objects.all()
    }
    return render(request,'main/about.html',context)

def contact(request):
    context = {
        'departments':Department.objects.all(),
        'units':Unit.objects.all(),
        'genders':Gender.objects.all(),
        'roles':Role.objects.all()
    }
    return render(request,'main/contact.html',context)


@login_required
@group_required(['Admin Officer', 'Support','Developer'])
def admin_page(request):
    current_user = request.user
    current_date = timezone.now().date()
    current_month = timezone.now().month
    current_year = timezone.now().year

    dates_selected = Roster.objects.filter(user=current_user, date=current_date).exists()

    users_with_status = []

    # Allow 'Admin Officer' to see users in their department, 
    if current_user.group.title == 'Admin Officer' and current_user.department:
        users = User.objects.filter(department=current_user.department, group__title='User')
    elif current_user.group.title in ['Support','Developer']:
         # Allow Support and developer to see  all users
        users = User.objects.filter(group__title='User') 
    else:
        users = User.objects.none()
    for user in users:
        has_dates_selected = Roster.objects.filter(user=user, date__month=current_month, date__year=current_year).exists()
        users_with_status.append({'user': user, 'has_dates_selected': has_dates_selected})

    context = {'users_with_status': users_with_status,'dates_selected': dates_selected}

    return render(request, 'main/admin_page.html', context)


@login_required
@group_required(['Canteen manager','Support','Developer'])    
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
            messages.success(request, 'Meal updated successfully')
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

@login_required
@group_required('Canteen manager')   
def delete_meal(request,id):
    delete_meal = Meal.objects.get(id=id)
    delete_meal.delete()
    messages.success(request,'Meal deleted successfully')
    return redirect('canteen_manager')

def is_puplic_holiday(today):
    ng_holidays = holidays.Nigeria(years=today.year)
    return today in ng_holidays


@login_required
@group_required('User') 
def meal_request(request):
    user = request.user
    today = timezone.now().date()
    weekday = today.weekday()
    
    on_call = Roster.objects.filter(user=user, date=today).exists()
    is_holiday = is_puplic_holiday(today)
    if request.method == 'POST':
        if not on_call:
            messages.error(request, 'You are not on call today')
            return redirect('meal_request')

        meal_Obj = request.POST.getlist('meal_id')
        if meal_Obj:
            requests_today = Request.objects.filter(user=user, date_created__date=today)
            if weekday < 5 and not is_holiday: 
                # Weekdays that are not public holidays allow only one request
                if requests_today.exists():
                    messages.error(request, 'You can only make one meal request per day on weekdays.')
                    return redirect('meal_request')
            else:
                # Weekend Saturday, Sunday or public holiday  Allow  two meal requests  
                if requests_today.count() >= 2:
                    messages.error(request, 'You can only make two meal requests on weekends or public holidays.')
                    return redirect('meal_request')

            new_request = Request.objects.create(user=user)
            try:
                total_price = 0 

                for meal_id in meal_Obj:
                    meal = Meal.objects.get(id=meal_id)

                    if not meal.price:
                        messages.error(request, f'Meal {meal.title} does not have a price set.')
                        new_request.delete()  # Clean up the request
                        return redirect('meal_request') 
                    
                    meal_price = float(meal.price) 
                    total_price += meal_price
                    RequestDetails.objects.create(request=new_request, meal=meal, meal_price=meal_price)

                new_request.total_price = total_price
                new_request.save()         
                messages.success(request, 'Meal request successful.')
                return redirect('meal_request')
            
            except Meal.DoesNotExist:
                messages.error(request, f'Meal with ID {meal_id} does not exist.')
                new_request.delete()  # Clean up the request
                return redirect('meal_request')   

            except Exception as e:
                messages.error(request, f'An unexpected error occurred: {str(e)}')
                new_request.delete()  # Clean up the request
                return redirect('meal_request')

    meals = Meal.objects.all()
    food_meal = Meal.objects.filter(category__title='Food')
    protein_meal = Meal.objects.filter(category__title='Protein')
    drink_meal = Meal.objects.filter(category__title='Drink')

    context = {'meals': meals, 'food_meal': food_meal, 'protein_meal': protein_meal,
               'drink_meal': drink_meal, 'on_call': on_call, 'is_holiday': is_holiday}
    return render(request, 'main/meal_request.html', context)


@login_required
@group_required(['User','Canteen manager'])  
def meal_request_details(request):
    meals = Meal.objects.all().order_by('title')
    user = request.user
    current_day = timezone.now().date()
  
    user_requests = Request.objects.filter(user=user, date_created__date=current_day)
    total_price = user_requests.aggregate(total=Sum('requestdetails__meal__price'))['total'] or 0

    user_request_details = RequestDetails.objects.filter(request__in=user_requests)
    
    context = {
        'user_request_details': user_request_details,
        'meals': meals,
        'total_price': total_price,
    }
    
    return render(request, 'main/user_request_details.html', context)


@login_required
@group_required('User')  
def edit_meal_request(request, id):
    meal_request = get_object_or_404(RequestDetails, id=id)
    meals = Meal.objects.all().order_by('title')

    if request.method == 'POST':
        meal_id = request.POST.get('meal')
        if meal_id:
            meal = Meal.objects.filter(id=meal_id).first()
            if meal:
                current_request = meal_request.request
                existing_request = RequestDetails.objects.filter(request=current_request)
                current_total_price = sum(Decimal(req.meal.price)for req in existing_request if req.meal)

                current_meal_price = Decimal(meal_request.meal.price)
                new_total_price = current_total_price - current_meal_price + Decimal(meal.price)

                if new_total_price <= Decimal(1700.00):
                    meal_request.meal = meal
                    meal_request.save()
                    current_request.calculate_total_price()
                    messages.success(request, 'Updated successfully.')
                    return redirect('meal_request_details')
                else:
                    messages.error(request, 'Total meal does not exist.')
                    return redirect('meal_request_details')
            else:
                messages.error(request, 'Selected meal does not exist.')
                return redirect('meal_request_details') 
        else:
            messages.error(request, 'No meal Selected.')
            return redirect('meal_request_details') 
    context = {'meal_request':meal_request,'meal':meal}          
    return render(request, 'main/edit_meal_request.html', context)


@login_required    
@group_required(['Admin Officer','Support'])  
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

@login_required
@group_required(['Admin Officer', 'User'])
def user_roster(request):
    user = request.user
    current_month = timezone.now().month
    current_year = timezone.now().year
    user_call_dates = Roster.objects.filter(user=request.user, date__month=current_month, date__year=current_year).values_list('date', flat=True)
    
    return render(request, 'main/user_roster.html', {'user_call_dates': user_call_dates})    

@login_required
def delete_meal_request(request, id):
    user = request.user
    requestObj = RequestDetails.objects.get(id=id)
    requestObj.delete()
    messages.success(request,'Meal deleted successfully')
    return redirect('meal_request_details')

@login_required
@group_required('Canteen manager')  
def pending_meal_requests(request):
    today = timezone.now().date()
    requests = Request.objects.filter(date_created__date=today, status='Pending')
    context = {'requests': requests,'today':today}
    return render(request, 'main/pending_meal_requests.html', context)

@login_required
@group_required('Canteen manager')  
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

@login_required
@group_required(['Admin Officer','User','Support'])  
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
        messages.success(request, f"Date removed successfully for {user.firstname}")
        return redirect('admin_page')
    formatted_dates = [date.strftime('%Y-%m-%d') for date in user_on_call_dates]
    return render(request, 'main/update_user_roster.html', {'user': user, 'user_on_call_dates': formatted_dates})





