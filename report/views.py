from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from datetime import datetime
from main.models import *
from accounts.models import *
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils.dateparse import parse_datetime
from django.contrib.auth.decorators import login_required



def filter_requests(datefrom, dateto, status):
    # filtered_requests = Request.objects.exclude(status='Decline').prefetch_related('requestdetails_set__meal')
    filtered_requests = Request.objects.all() 

    if datefrom:
        filtered_requests = filtered_requests.filter(date_created__gte=datefrom)
    if dateto:
        filtered_requests = filtered_requests.filter(date_created__lte=dateto)
    if status:
        filtered_requests = filtered_requests.filter(status=status)

    return filtered_requests  


@login_required
def meal_report_and_search(request):
    datefrom = request.GET.get('datefrom')
    dateto = request.GET.get('dateto')
    status = request.GET.get('status')
    
    filtered_requests = filter_requests(datefrom, dateto, status)

    # Calculate total price
    total_price = sum(req.calculate_total_price() for req in filtered_requests)
    user_request_details = RequestDetails.objects.filter(request__in=filtered_requests)

   
    report = filtered_requests

    context = {
        'report': report,
        'total_price': total_price,
        'user_request_details': user_request_details,
        'status': status,
        'datefrom': datefrom,
        'dateto': dateto,
       
    }

    return render(request, 'report/meal_report.html', context)

@login_required
def generate_pdf(request):
    datefrom = request.GET.get('datefrom')
    dateto = request.GET.get('dateto')
    status = request.GET.get('status')

    if datefrom:
        datefrom = parse_datetime(datefrom)
        if not datefrom:
            return HttpResponse("Invalid 'datefrom' format. It must be in YYYY-MM-DD HH:MM format.", status=400)
    if dateto:
        dateto = parse_datetime(dateto)
        if not dateto:
            return HttpResponse("Invalid 'dateto' format. It must be in YYYY-MM-DD HH:MM format.", status=400)

    filtered_requests = filter_requests(datefrom, dateto, status)
    total_price = sum(req.calculate_total_price() for req in filtered_requests)

    template_path = 'report/report_meal_pdf.html'
    context = {
        'report': filtered_requests,
        'total_price': total_price,
        'datefrom': datefrom,
        'dateto': dateto,
        'status': status,
    }

    # Render the template to HTML
    template = get_template(template_path)
    html = template.render(context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="meal_report.pdf"'

    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Check for errors
    if pisa_status.err:
        return HttpResponse('An error occurred while generating the PDF.')

    return response


@login_required
def user_report_details(request):
    user = request.user  
    datefrom = request.GET.get('datefrom')
    dateto = request.GET.get('dateto')
    status = request.GET.get('status')
    
   
    filtered_requests = filter_requests(datefrom, dateto, status).filter(user=user)

    # Calculate total price for the user's requests
    total_price = sum(req.calculate_total_price() for req in filtered_requests)
    
    user_request_details = RequestDetails.objects.filter(request__in=filtered_requests)

    context = {
        'report': filtered_requests,
        'total_price': total_price,
        'user_request_details': user_request_details,
        'status': status,
        'datefrom': datefrom,
        'dateto': dateto,
    }
    return render(request, 'report/user_report.html', context)