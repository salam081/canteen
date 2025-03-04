from django.shortcuts import render
from django.db.models import Prefetch, Sum
from main.models import *
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import render_to_string

# def meal_list(request):
#     report = Request.objects.exclude(status='Decline').prefetch_related('requestdetails_set__meal')
#     total_price = sum(req.calculate_total_price() for req in report)
#     user_request_details = RequestDetails.objects.filter(request__in=report)
#     all_user_req = [
#         {'user_req':user_req,'all_req':user_request_details}
#         for user_req in user_request_details
#     ]
#     context = {'report': report,'total_price': total_price,
#                'all_user_req':all_user_req,
#                 'user_request_details': user_request_details,
#                 # 'datefrom': datefrom,'dateto': dateto,
#                 }
#     return render(request,'report/meal_list.html',context)


# def search(request):
#     datefrom = request.GET.get('datefrom')
#     dateto = request.GET.get('dateto')
#     status = request.GET.get('status')

#     report = Request.objects.exclude(status='Decline').prefetch_related('requestdetails_set__meal')

#     if status:
#         report = report.filter(status=status)
#     #  filter by dates   
#     if datefrom:
#         report = report.filter(date_created__gte=datefrom)
#     if dateto:
#         report = report.filter(date_created__lte=dateto)

#     total_price = sum(req.calculate_total_price() for req in report)
#     user_request_details = RequestDetails.objects.filter(request__in=report)
#     all_user_req = [
#         {'user_req':user_req,'all_req':user_request_details}
#         for user_req in user_request_details
#     ]
#     context = {'report': report,'total_price': total_price,
#                'all_user_req':all_user_req,'status': status,
#                 'user_request_details': user_request_details,
#                 'datefrom': datefrom,'dateto': dateto,
#                 }
    
#      # Check if the request is for generating a PDF
#     if 'pdf' in request.GET:
#         # Render the table content for PDF
#         html_content = render_to_string('report/meal_report_table.html', context)

#         # Create the PDF response
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="meal_list.pdf"'

#         # Convert HTML to PDF
#         pisa_status = pisa.CreatePDF(html_content, dest=response)

#         if pisa_status.err:
#             return HttpResponse('Error generating PDF', status=500)

#         return response
#     return render(request,'report/search.html',context)

#////////////////////////////////////

# def meal_report(request):
#     datefrom = request.GET.get('datefrom')
#     dateto = request.GET.get('dateto')
#     status = request.GET.get('status')

#     report = Request.objects.exclude(status='Decline').prefetch_related('requestdetails_set__meal')

#     if status:
#         report = report.filter(status=status)
#     #  filter by dates   
#     if datefrom:
#         report = report.filter(date_created__gte=datefrom)
#     if dateto:
#         report = report.filter(date_created__lte=dateto)

#     # calculate total meal request
#     total_price = sum(req.calculate_total_price() for req in report)
#     user_request_details = RequestDetails.objects.filter(request__in=report)
#     all_user_req = [
#         {'user_req':user_req,'all_req':user_request_details}
#         for user_req in user_request_details
#     ]
#     context = {'report': report,'total_price': total_price,
#                'all_user_req':all_user_req,'status': status,
#                 'user_request_details': user_request_details,
#                 'datefrom': datefrom,'dateto': dateto,
#                 }
    
#     # Check if the request is for generating a PDF
#     if 'pdf' in request.GET:
#         # Render the table content for PDF
#         html_content = render_to_string('report/meal_report_table.html', context)

#         # Create the PDF response
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="meal_report.pdf"'

#         # Convert HTML to PDF
#         pisa_status = pisa.CreatePDF(html_content, dest=response)

#         if pisa_status.err:
#             return HttpResponse('Error generating PDF', status=500)

#         return response
#     return render(request,'report/report2.html',context)

#/////////////////////////////

# def report(request):
#     datefrom = request.GET.get('datefrom')
#     dateto = request.GET.get('dateto')
#     status = request.GET.get('status')

#     all_requests = Request.objects.exclude(status='Decline').prefetch_related('requestdetails_set__meal')
#     if status:
#         all_requests = all_requests.filter(status=status)

#     #  filter by dates
#     if datefrom:
#         all_requests = all_requests.filter(date_created__gte=datefrom)
#     if dateto:
#         all_requests = all_requests.filter(date_created__lte=dateto)

#     total_price = all_requests.aggregate(total=Sum('total_price'))['total'] #or 0

#     user_requested_meals = []
#     for req in all_requests:
#         user_meals = {
#             'user': req.user.username if req.user else "Unknown User",
#             'meals': [
#                 {'meal_title': detail.meal.title, 'meal_price': detail.meal.price}
#                 for detail in req.requestdetails_set.all()
#             ],
#             'total_price': req.total_price,
#             'status': req.status,
#         }
#         user_requested_meals.append(user_meals)

#     context = {'user_requested_meals': user_requested_meals,
#                 'total_price': total_price,'status': status,
#                 'datefrom': datefrom,'dateto': dateto,}

#     return render(request, 'report/report.html', context)

'''
def meal_report(request):
    # Get parameters from the GET request
    datefrom = request.GET.get('datefrom')
    dateto = request.GET.get('dateto')
    status = request.GET.get('status')

    # Fetch report data, excluding 'Decline' status
    report = Request.objects.exclude(status='Decline').prefetch_related('requestdetails_set__meal')

    if status:
        report = report.filter(status=status)
    if datefrom:
        report = report.filter(date_created__gte=datefrom)
    if dateto:
        report = report.filter(date_created__lte=dateto)

    # Calculate total price for meal requests
    total_price = sum(req.calculate_total_price() for req in report)
    user_requested_meals = [
        {'user': req.user, 'meals': req.requestdetails_set.all(), 'total_price': req.calculate_total_price(), 'status': req.status, 'date_created': req.date_created}
        for req in report
    ]

    context = {'report': report,'total_price': total_price,
               'all_user_req':all_user_req,'status': status,
                'user_request_details': user_request_details,
                'datefrom': datefrom,'dateto': dateto,}
    

    # Check if the request is for generating a PDF
    if 'pdf' in request.GET:
        # Render the table content for PDF
        html_content = render_to_string('report/meal_report_table.html', context)

        # Create the PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="meal_report.pdf"'

        # Convert HTML to PDF
        pisa_status = pisa.CreatePDF(html_content, dest=response)

        if pisa_status.err:
            return HttpResponse('Error generating PDF', status=500)

        return response

    # Render the full report page as an HTML page if not requesting PDF
    return render(request, 'report/report2.html', context)
'''



# def meal_report(request):
#     # Get parameters from the GET request
#     datefrom = request.GET.get('datefrom')
#     dateto = request.GET.get('dateto')
#     status = request.GET.get('status')

#     # Fetch report data, excluding 'Decline' status
#     report = Request.objects.exclude(status='Decline').prefetch_related('requestdetails_set__meal')

#     if status:
#         report = report.filter(status=status)
#     if datefrom:
#         report = report.filter(date_created__gte=datefrom)
#     if dateto:
#         report = report.filter(date_created__lte=dateto)

#     # Calculate total price for meal requests
#     total_price = sum(req.calculate_total_price() for req in report)
#     user_request_details = RequestDetails.objects.filter(request__in=report)

#     context = {
#         'report': report,
#         'total_price': total_price,
#         'all_user_req': [
#             {'user_req': user_req, 'all_req': user_request_details} 
#             for user_req in user_request_details
#         ],
#         'status': status,
#         'user_request_details': user_request_details,
#         'datefrom': datefrom,
#         'dateto': dateto,
#     }

#     # Check if the request is for generating a PDF
#     if 'pdf' in request.GET:
#         # Generate PDF content
#         html_content = render_to_string('report/report2.html', context)

#         # Create the PDF response
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="meal_report.pdf"'

#         # Convert HTML to PDF
#         pisa_status = pisa.CreatePDF(html_content, dest=response)

#         if pisa_status.err:
#             return HttpResponse('Error generating PDF', status=500)

#         return response

#     # Render the report as an HTML page if not requesting PDF
#     return render(request, 'report/report2.html', context)