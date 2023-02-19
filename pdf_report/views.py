from django.shortcuts import render
from adminapps.models import *
from datetime import date, datetime, timedelta
from django.db.models import Q, Sum, Count
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


today = date.today()
curr_month = today.month % 12
prev_month = today.month - 1
if prev_month == 0:
    prev_month = 12

def pdf_report_create_newmatter(request):
    inifile = sysinifile.objects.first()
    ndays = int(1)
    svalue1 = ("+"+str(ndays))
    ndays = int(35)
    svalue2 = ("+"+str(ndays))
    sdate = today - relativedelta(days=int(5))
    d1 = sdate
    d2 = sdate + relativedelta(days=int(svalue2))
    daterange = "Date Covered : "+d1.strftime('%m/%d/%Y') + " To "+d2.strftime('%m/%d/%Y')
    access_code = request.user.user_profile.userid
    user_id = User.id
    user_message_id = request.user.user_profile.id
    srank = request.user.user_profile.rank
    username = request.user.username
    lawyers = request.user.user_profile.supporto
    listoflawyers = lawyers.split(',')
    code1 = ""
    code2 = ""
    code3 = ""
    code4 = ""
    code5 = ""
    code6 = ""
    code7 = ""

    for i in range(0, len(listoflawyers)):
        if i == 0:
            code1 = listoflawyers[i]
        elif i == 1:
            code2 = listoflawyers[i]
        elif i == 2:
            code3 = listoflawyers[i]
        elif i == 3:
            code4 = listoflawyers[i]
        elif i == 4:
            code5 = listoflawyers[i]
        elif i == 5:
            code6 = listoflawyers[i]
        elif i == 6:
            code7 = listoflawyers[i]


    handlingLawyer_q = Q(Q(handling_lawyer__access_code=code1) | Q(handling_lawyer__access_code=code2) | Q(handling_lawyer__access_code=code3) | Q(handling_lawyer__access_code=code4) | Q(handling_lawyer__access_code=code5) | Q(handling_lawyer__access_code=code6) | Q(handling_lawyer__access_code=code7))

    recentmatters = Matters.objects.filter(handlingLawyer_q, created_at__gte=d1, created_at__lte=d2).order_by('-created_at')

    recentmatters_count = recentmatters.count()

    template_path = 'pdf_reports/pdfreport_newmatters.html'
    context = {
        'recentmatters':recentmatters,
        'recentmatters_count':recentmatters_count,
        'inifile':inifile,
        'daterange':daterange,

    }

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'attachment; filename="newmatters.pdf"'
    # find the template and render it.
    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def pdf_report_create_duedatelist(request):
    inifile = sysinifile.objects.first()
    inifile = inifile.company
    ndays = int(1)
    svalue1 = ("+"+str(ndays))
    ndays = int(35)
    svalue2 = ("+"+str(ndays))
    sdate = today - relativedelta(days=int(5))
    d1 = sdate
    d2 = sdate + relativedelta(days=int(svalue2))
    daterange = "Date Covered : "+d1.strftime('%m/%d/%Y') + " To "+d2.strftime('%m/%d/%Y')
    access_code = request.user.user_profile.userid
    user_id = User.id
    srank = request.user.user_profile.rank
    username = request.user.username
    lawyers = request.user.user_profile.supporto
    listoflawyers = lawyers.split(',')
    code1 = ""
    code2 = ""
    code3 = ""
    code4 = ""
    code5 = ""
    code6 = ""
    code7 = ""

    for i in range(0, len(listoflawyers)):
        if i == 0:
            code1 = listoflawyers[i]
        elif i == 1:
            code2 = listoflawyers[i]
        elif i == 2:
            code3 = listoflawyers[i]
        elif i == 3:
            code4 = listoflawyers[i]
        elif i == 4:
            code5 = listoflawyers[i]
        elif i == 5:
            code6 = listoflawyers[i]
        elif i == 6:
            code7 = listoflawyers[i]

    multiple_q = Q(Q(matter__handling_lawyer__access_code=code1) | Q(matter__handling_lawyer__access_code=code2) | Q(matter__handling_lawyer__access_code=code3) | Q(
        matter__handling_lawyer__access_code=code4) | Q(matter__handling_lawyer__access_code=code5) | Q(matter__handling_lawyer__access_code=code6) | Q(matter__handling_lawyer__access_code=code7))


    #print(multiple_q)
    handlingLawyer_q = Q(Q(handling_lawyer__access_code=code1) | Q(handling_lawyer__access_code=code2) | Q(handling_lawyer__access_code=code3) | Q(handling_lawyer__access_code=code4) | Q(handling_lawyer__access_code=code5) | Q(handling_lawyer__access_code=code6) | Q(handling_lawyer__access_code=code7))

    duedates = AppDueDate.objects.filter(
        multiple_q, duedate__gte=d1, duedate__lte=d2, date_complied__isnull=True).order_by('-duedate')
    
    duedates_count = duedates.count()

    template_path = 'pdf_reports/pdfreport_duedatelist.html'
    context = {
        'duedates': duedates,
        'duedates_count': duedates_count,
        'inifile':inifile,
        'daterange':daterange,

    }

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'attachment; filename="duedatelist.pdf"'
    # find the template and render it.
    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response






# Create your views here.
