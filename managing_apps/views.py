from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import AppType, LawyersCases
from adminapps.models import *
from datetime import date, datetime, timedelta

from django.db.models import Q, Sum, Count

today = date.today()
curr_month = today.month % 12
prev_month = today.month -1
if prev_month == 0:
    prev_month = 12

# Create your views here.
@login_required
def main(request):

    # details

    activitydetails = task_detail.objects.filter(tran_date__year = today.year, tran_date__month = today.month).order_by('-tran_date')
    bill_amount = AccountsReceivable.objects.filter(bill_date__year = today.year, bill_date__month = today.month).aggregate(Sum('bill_amount'))
    bill_amt = bill_amount["bill_amount__sum"]
    prev_bill_amount = AccountsReceivable.objects.filter(bill_date__year = today.year, bill_date__month = prev_month).aggregate(Sum('bill_amount'))
    prev_bill_amt = prev_bill_amount["bill_amount__sum"]

    matters = Matters.objects.filter(filing_date__year = today.year, filing_date__month = today.month)
    prevmatters = Matters.objects.filter(filing_date__year = today.year, filing_date__month = prev_month)
    clients = Client_Data.objects.filter(date_acquired__year = today.year, date_acquired__month = today.month)
    prevclient = Client_Data.objects.filter(date_acquired__year = today.year, date_acquired__month = prev_month)

    lawyer_summary = Matters.objects.values('handling_lawyer').annotate(case_count=Count('handling_lawyer')).filter(filing_date__year = today.year, filing_date__month = today.month)
    prev_lawyer_summary = Matters.objects.values('handling_lawyer').annotate(case_count=Count('handling_lawyer')).filter(filing_date__year = today.year, filing_date__month = prev_month)

    activities = task_detail.objects.all()
#    matters = Matters.objects.all()

    alertmessages = Alert_Messages.objects.filter(messageto = 10)

    clientcount = clients.count()
    activitycount = activities.count()
    matterscount = matters.count()
    prevmonthmatters = prevmatters.count
    prevclientcount = prevclient.count
    lawyerInventory = LawyersCases.objects.all()


    queryset = AppType.objects.all()
    countalert = alertmessages.count()


    context = {
        'activitycount' : activitycount,
        'clientcount' : clientcount,
        'prevclientcount' : prevclientcount,
        'matterscount' : matterscount,
        'prevcount' : prevmonthmatters,
        'ARbills': bill_amt,
        'prev_ARbills' : prev_bill_amt,
        'queryset' : queryset,
        'inventory': lawyerInventory,
        'activitydetails' : activitydetails,
        'alertmessages' : alertmessages,
        'noofalerts' : countalert,

    }
    return render(request, 'managing_apps/index.html', context)

def view_new_clients(request):
    clients = Client_Data.objects.filter(date_acquired__year = today.year, date_acquired__month = today.month).order_by('client_name')
    client_count = clients.count()
    prevclients = Client_Data.objects.filter(date_acquired__year = today.year, date_acquired__month = prev_month).order_by('-date_acquired')
    prevclient_counts = prevclients.count()

    #client_summary = Matters.objects.values('folder__folder_type__folder').annotate(case_count=Count('folder__folder_type__folder')).filter(filing_date__year = today.year, filing_date__month = today.month).order_by('-case_count')
    client_summary_count = Matters.objects.values('folder__client__client_name').annotate(NoOfMatter = Count('folder__client')).filter(filing_date__year = today.year, filing_date__month = today.month).order_by('folder__client__client_name')
    total_numberofmatters = client_summary_count.count()
    context = {

        'clients' : clients,
        'clientcount' : client_count,
        'prevclients': prevclients,
        'prevclientcount': prevclient_counts,
        'clientsummary' : client_summary_count,
        'total_count_matters' : total_numberofmatters
    }

    return render(request, 'managing_apps/view_newclients.html', context)

def view_new_matters(request):
    matters = Matters.objects.filter(filing_date__year = today.year, filing_date__month = today.month ).order_by('-filing_date')
    prevmatters = Matters.objects.filter(filing_date__year = today.year, filing_date__month = prev_month).order_by('-filing_date')

    matter_count = matters.count()
    prevmonthmatters = prevmatters.count

    lawyer_summary = Matters.objects.values('handling_lawyer__lawyer_name').annotate(case_count=Count('handling_lawyer__lawyer_name')).filter(filing_date__year = today.year, filing_date__month = today.month).order_by('-case_count')
    prev_lawyer_summary = Matters.objects.values('handling_lawyer__lawyer_name').annotate(case_count=Count('handling_lawyer__lawyer_name')).filter(filing_date__year = today.year, filing_date__month = prev_month).order_by('-case_count')


    context = {

        'matter' : matters,
        'mattercount' : matter_count,
        'prevmatters' : prevmatters,
        'prevcount' : prevmonthmatters,
        'lawyersummary' : lawyer_summary,
        'prevlawyersummary' : prev_lawyer_summary,

    }

    return render(request, 'managing_apps/view_newmatters.html', context)

def view_matter(request, pk):
    global matter_key
    matter_key = pk
    matter = Matters.objects.get(id=pk)
    stype = matter.apptype
    # to display the lists 
    activities = task_detail.objects.filter(matter_id=pk).order_by("-tran_date")
    listduedates = AppDueDate.objects.filter(matter_id=pk).order_by("-duedate")
    listbillings = AccountsReceivable.objects.filter(matter_id=pk).order_by("-bill_date")
    listofclasses = ClassOfGoods.objects.filter(matter_id=pk)
    # get total amounts
    tbill_amount = listbillings.aggregate(Sum('bill_amount'))
    tpf_amount = listbillings.aggregate(Sum('pf_amount'))
    tofees_amount = listbillings.aggregate(Sum('ofees_amount'))
    tope_amount = listbillings.aggregate(Sum('ope_amount'))

    Tbill_amt = tbill_amount["bill_amount__sum"]
    Tpf_amt = tpf_amount["pf_amount__sum"]
    Tofees_amt = tofees_amount["ofees_amount__sum"]
    Tope_amt = tope_amount["ope_amount__sum"]

    listpayments = Payments.objects.filter(matter_id=pk).order_by("-payment_date")

    context = {
        'matter' : matter,
        'activities' : activities,
        matter_key : matter_key,
        'duedate' : listduedates,
        'bills'   : listbillings,
        'payments': listpayments,
        'Tbill_amt' : Tbill_amt,
        'Tpf_amt' : Tpf_amt,
        'Tofees_amt' : Tofees_amt,
        'Tope_amt' : Tope_amt,
        'Classes' : listofclasses,
        'apptype' : stype,


    }
    return render(request, 'managing_apps/matterinfo.html', context)

def card_view(request):
    return render(request, 'managing_apps/cards.html')

def chartonbillings(request):
    queryset1 = LawyersCases.objects.all()
    queryset2 = AppType.objects.all()

    context = {
        'queryset1': queryset1,
        'queryset2': queryset2,
    }
    return render(request, 'managing_apps/chartview.html', context)

