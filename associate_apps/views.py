#from asyncio.windows_events import NULL
#from os import CLD_CONTINUED
from pickletools import read_uint1
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pandas import notnull

from adminapps.models import *
from django.core.paginator import Paginator

from django.contrib.auth import get_user
from django.core import paginator
from django.contrib.auth.models import User

from django.db import connection
from django.forms.widgets import ClearableFileInput
from django.shortcuts import render, redirect
# import adminapps
from userprofile.models import User_Profile
#from django.contrib import messages
from django.core.paginator import Paginator
from datetime import date, datetime, timedelta
from django.db.models import Q, Sum, Count
from adminapps.forms import MailsInwardForm, EntryBillForm, EntryExpensesForm, Non_IPDetailForm, ClassOfGoodsEntry, IPDetailForm, AREntryForm, EntryMatterForm, DocumentEditForm, TaskEntryForm1, TaskEntryForm, FilingDocsEntry, AlertMessageForm, AlertUpdateStatusForm, DueDateEntryForm
from django.core.exceptions import ObjectDoesNotExist
from dateutil.relativedelta import relativedelta
import io


# printing option


today = date.today()
curr_month = today.month % 12
prev_month = today.month - 1
if prev_month == 0:
    prev_month = 12


# Create your views here.
@login_required
# this is the function when lawyers login the page;
# print(access_code)
# alertmessages = Alert_Messages.objects.all()
# multiple_q = Q(Q(matter__handling_lawyer__lawyerID__userid=access_code))
def main(request):
    access_code = request.user.user_profile.userid
    username = request.user.username
    alertmessages = Alert_Messages.objects.filter(messageto=access_code)
    matterlist = Matters.objects.filter(created_at__year=today.year, created_at__month=today.month,
                                        handling_lawyer__lawyerID__userid=access_code).order_by('-filing_date')
    duedates = AppDueDate.objects.filter(duedate__year=today.year, duedate__month=today.month,
                                         matter__handling_lawyer__lawyerID__userid=access_code).order_by('duedate')
    recentdocs = FilingDocs.objects.filter(
        Task_Detail__lawyer__lawyerID__userid=access_code).order_by('-DocDate')
    countalert = alertmessages.count()
    multiple_q = Q(matter__handling_lawyer__lawyerID__userid=access_code)
    recent_billables = TempBills.objects.filter(
        multiple_q, tran_date__year=today.year, tran_date__month=today.month).order_by('-tran_date')

    recenttask = task_detail.objects.filter(
        multiple_q, tran_date__year=today.year, tran_date__month=today.month).order_by('-tran_date')
    number_of_task = recenttask.count()
    number_of_dues = duedates.count()
    number_of_docs = matterlist.count()
    context = {
        'alertmessages': alertmessages,
        'noofalerts': countalert,
        'duedates': duedates,
        'recenttask': recenttask,
        'recentdocs': recentdocs,
        'recent_billables': recent_billables,
        'username': username,
        'matterlist': matterlist,
        'number_of_task': number_of_task,
        'number_of_dues': number_of_dues,
        'number_of_docs': number_of_docs,

    }
    return render(request, 'associates_apps/index.html', context)


def matterlist(request):
    access_code = request.user.user_profile.userid
    if 'q' in request.GET:
        q = request.GET['q']
        multiple_q = Q(Q(matter_title__icontains=q) | Q(folder__client__client_name__icontains=q) | Q(
            folder__folder_description__icontains=q) | Q(referenceno__icontains=q))
        matters = Matters.objects.filter(
            multiple_q, handling_lawyer__lawyerID__userid=access_code).order_by("-filing_date")
#        arlist = AccountsReceivable.objects.filter(multiple_q, matter__handling_lawyer__lawyerID__userid=access_code).order_by("-bill_date")

    else:
        matters = Matters.objects.filter(
            handling_lawyer__lawyerID__userid=access_code).order_by("-filing_date")
#        arlist = AccountsReceivable.objects.filter(matter__handling_lawyer__lawyerID__userid=access_code).order_by("-bill_date")

    # if 'q' in request.GET:
    #     q = request.GET['q']
    #     #matters = Matters.objects.filter(matter_title__icontains=q)
    #     #multiple_q = Q(Q(matter_title__icontains=q) | Q(folder__icontains=q))
    #     #matters = Matters.objects.filter(folder__client__client_name__icontains=q)
    #     multiple_q = Q(Q(matter_title__icontains=q) | Q(folder__client__client_name__icontains=q) | Q(referenceno__icontains=q) | Q(handling_lawyer__lawyer_name__icontains=q) | Q(folder__folder_description__icontains=q))
    #     matters = Matters.objects.filter(multiple_q)
    # else:
    #     matters = Matters.objects.all().order_by("folder__client__client_name")

    noofmatters = matters.count()
    paginator = Paginator(matters, 11)
    page = request.GET.get('page')
    all_matters = paginator.get_page(page)

    context = {
        'page': page,
        'noofmatters': noofmatters,
        'matters': all_matters
    }
    return render(request, 'associates_apps/listmatters.html', context)


def alert_messages(request):
    access_code = request.user.user_profile.userid
    messages = Alert_Messages.objects.filter(
        messageto=access_code).order_by('-date_alert')
#    sentmessages = Alert_Messages.objects.filter(sentby__userid=access_code)
    context = {
        'messages': messages,
        'access_code': access_code,
    }
    return render(request, 'associates_apps/alertmessages.html', context)


def view_sentmessages(request):
    access_code = request.user.user_profile.userid
    sentmessages = Alert_Messages.objects.filter(
        sentby__userid=access_code).order_by('-date_alert')
    context = {
        'sentmessages': sentmessages,


    }
    return render(request, 'associates_apps/sentmessages.html', context)


def edit_statusmessage(request, pk):
    message = Alert_Messages.objects.get(id=pk)
    if request.method == 'POST':
        form = AlertUpdateStatusForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('associate-alert_messages')
        else:
            form = AlertUpdateStatusForm(instance=message)
    else:
        form = AlertUpdateStatusForm(instance=message)

    context = {
        'form': form,
        'message': message,
    }
    return render(request, 'associates_apps/editstatus_msg.html', context)


def edit_alertmessage(request, pk):
    message = Alert_Messages.objects.get(id=pk)
    if request.method == 'POST':
        form = AlertMessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('associate-view_sentmessages')
        else:
            form = AlertMessageForm(instance=message)
    else:
        form = AlertMessageForm(instance=message)

    context = {
        'form': form,
    }
    return render(request, 'associates_apps/edit_msg.html', context)


def new_alertmessage(request):

    if request.method == "POST":
        # Get the posted form
        form = AlertMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('associate-alert_messages')
        else:
            return redirect('associate-new_alertmessage')
    else:
        form = AlertMessageForm()

    context = {
        'form': form,
    }
    return render(request, 'associates_apps/add_new_msg.html', context)


def view_portfolio(request, m_id):
    matter = Matters.objects.get(id=m_id)
    activities = task_detail.objects.filter(matter__id=m_id)
    duedatelist = AppDueDate.objects.filter(matter__id=m_id)
    ardetails = AccountsReceivable.objects.filter(matter__id=m_id)
    payments = Payments.objects.filter(matter__id=m_id)
    filingdocs = FilingDocs.objects.filter(Task_Detail__matter__id=m_id)

    bill_amount = AccountsReceivable.objects.filter(
        matter__id=m_id).aggregate(Sum('bill_amount'))
    if bill_amount["bill_amount__sum"] == None:
        Total_bill_amt = 0
    else:
        Total_bill_amt = bill_amount["bill_amount__sum"]

    pay_amount = Payments.objects.filter(
        matter__id=m_id).aggregate(Sum('pay_amount'))
    if pay_amount["pay_amount__sum"] == None:
        Total_pay_amt = 0
    else:
        Total_pay_amt = pay_amount["pay_amount__sum"]

    Unpaid = Total_bill_amt - Total_pay_amt

    task_summary = task_detail.objects.values('task_code__Activity').annotate(
        task_count=Count('task_code')).filter(matter__id=m_id)

    context = {
        'matter': matter,
        'activities': activities,
        'ardetails': ardetails,
        'payments': payments,
        'Total_bill_amt': Total_bill_amt,
        'Total_pay_amt': Total_pay_amt,
        'Unpaid': Unpaid,
        'task_summary': task_summary,
        'duedatelist': duedatelist,
        'filingdocs': filingdocs,
    }
    return render(request, 'associates_apps/portfolio_review.html', context)


def matter_review(request, pk):
    def validateduedates():
        def computeduedate():
            if basisofcompute == "In Months":
                nmonths = int(terms)
                svalue = ("+"+str(nmonths))
                sduedate = sdate + relativedelta(months=int(svalue))
                duedate = sduedate

            if basisofcompute == "In Years":
                nyears = int(terms)
                svalue = ("+"+str(nyears))
                sduedate = sdate + relativedelta(years=int(svalue))
                duedate = sduedate

            if basisofcompute == "In Days":
                ndays = int(terms)
                svalue = ("+"+str(ndays))
                sduedate = sdate + relativedelta(days=int(svalue))
                duedate = sduedate

            dues = AppDueDate.objects.filter(
                matter_id=matter_id, duedate=duedate)
            if dues.exists():
                pass
            else:
                duedates = AppDueDate(
                    matter_id=matter_id, duedate=duedate, particulars=particulars)
                duedates.save()

#        result = DueCode.objects.filter(folder_type__id = 4)
        result = DueCode.objects.all()
        matter_id = matter.id
        apptype = matter.apptype_id
        lawyer = matter.handling_lawyer_id
        print(apptype)
        for duecodes in result:
            basisofcompute = duecodes.basisofcompute
            terms = duecodes.terms
            particulars = duecodes.Description
            if duecodes.fieldbsis == 'Application Date' and duecodes.apptype_id == apptype:
                appdate = matter.filing_date
                sdate = appdate
                if sdate is None:
                    pass
                else:
                    computeduedate()

    matter = Matters.objects.get(id=pk)
    c_id = matter.folder.client.id
    client = Client_Data.objects.get(id=c_id)
    expenses = TempExpenses.objects.filter(matter__id=pk)
    appduedates = AppDueDate.objects.filter(matter__id=pk)
    if request.method == 'POST':
        form = EntryMatterForm(request.POST, instance=matter)
        if form.is_valid():
            form.save()
#            apptype = request.POST["apptype"]
            apptype = matter.apptype.apptype
#            if apptype == "Trademark":
            validateduedates()
            return redirect('associate-matter-review', pk)
        else:
            form = EntryMatterForm(instance=matter)
    else:
        form = EntryMatterForm(instance=matter)

    activities = task_detail.objects.filter(matter__id=pk)
    duedatelist = AppDueDate.objects.filter(matter__id=pk)
    ardetails = AccountsReceivable.objects.filter(matter__id=pk)
    payments = Payments.objects.filter(bill_number__matter__id=pk)
    filingdocs = FilingDocs.objects.filter(Task_Detail__matter__id=pk)
    #apptype = matter.apptype_id
    apptype = matter.apptype.apptype
    #duelist = DueCode.objects.all()
    # if apptype == 1:
    #duelist = DueCode.objects.all()
    #duelist = DueCode.objects.filter(folder_type__id = 1)

    bill_amount = AccountsReceivable.objects.filter(
        matter__id=pk).aggregate(Sum('bill_amount'))
    if bill_amount["bill_amount__sum"] == None:
        Total_bill_amt = 0
    else:
        Total_bill_amt = bill_amount["bill_amount__sum"]

    pay_amount = Payments.objects.filter(
        bill_number__matter__id=pk).aggregate(Sum('pay_amount'))
    if pay_amount["pay_amount__sum"] == None:
        Total_pay_amt = 0
    else:
        Total_pay_amt = pay_amount["pay_amount__sum"]

    Unpaid = Total_bill_amt - Total_pay_amt

    task_summary = task_detail.objects.values('task_code__Activity').annotate(
        task_count=Count('task_code')).filter(matter__id=pk)

    context = {
        'client': client,
        'matter': matter,
        'tasks': activities,
        'ardetails': ardetails,
        'payments': payments,
        'Total_bill_amt': Total_bill_amt,
        'Total_pay_amt': Total_pay_amt,
        'Unpaid': Unpaid,
        'task_summary': task_summary,
        'duedatelist': duedatelist,
        'filingdocs': filingdocs,
        'form': form,
        'm_id': pk,
        'listofexpenses': expenses,

        'apptype': apptype,
        'duelist': appduedates,

    }

    return render(request, 'associates_apps/openmatter_details.html', context)
    # return render(request, 'associates_apps/seevalues.html', context)


def matter_otherdetails(request, pk, sk):
    def validateduedates():
        def computeduedate():
            if basisofcompute == "In Months":
                nmonths = int(terms)
                svalue = ("+"+str(nmonths))
                duedate = sdate + relativedelta(months=int(svalue))
            if basisofcompute == "In Years":
                nyears = int(terms)
                svalue = ("+"+str(nyears))
                sduedate = sdate + relativedelta(years=int(svalue))
                duedate = sduedate
            if basisofcompute == "In Days":
                ndays = int(terms)
                svalue = ("+"+str(ndays))
                duedate = sdate + relativedelta(days=int(svalue))

            dues = AppDueDate.objects.filter(
                matter_id=matter_id, duedate=duedate)
            if dues.exists():
                pass
            else:
                duedates = AppDueDate(
                    matter_id=matter_id, duedate=duedate, particulars=particulars)
                duedates.save()

        result = DueCode.objects.filter(folder_type__id=4)
        matter_id = matter.id
        apptype = matter.apptype_id
        lawyer = matter.handling_lawyer_id
        for duecodes in result:
            basisofcompute = duecodes.basisofcompute
            terms = duecodes.terms
            particulars = duecodes.Description
            if duecodes.fieldbsis == 'Registration Date' and duecodes.apptype_id == apptype:
                appdate = ip_matters.registration_date
                sdate = appdate
                if sdate is None:
                    pass
                else:
                    computeduedate()
            if duecodes.fieldbsis == 'Publication Date' and duecodes.apptype_id == apptype:
                appdate = ip_matters.publication_date
                sdate = appdate
                if sdate is None:
                    pass
                else:
                    computeduedate()
            if duecodes.fieldbsis == 'Renewal Date' and duecodes.apptype_id == apptype:
                appdate = ip_matters.renewal_date
                sdate = appdate
                if sdate is None:
                    pass
                else:
                    computeduedate()

    matter = Matters.objects.get(id=pk)
    m_id = matter.folder.client.id
    client = Client_Data.objects.get(id=m_id)

    duedates = AppDueDate.objects.filter(matter__id=pk)
    if sk == "IPO":
        try:
            ip_matters = IP_Matters.objects.get(matter__id=pk)
            sw = 1
        except ObjectDoesNotExist:
            sw = 0
        if request.method == 'POST':
            if sw == 0:
                form = IPDetailForm(request.POST)
            else:
                form = IPDetailForm(request.POST, instance=ip_matters)

            if form.is_valid():
                form.save()
                ip_matters = IP_Matters.objects.get(matter__id=pk)
                apptype = matter.apptype.apptype
                validateduedates()

                return redirect('associate-matter-review', pk)
            else:
                return redirect('associate-matter-review', pk)

        else:
            if sw == 0:
                form = IPDetailForm()
            else:
                form = IPDetailForm(instance=ip_matters)

        context = {
            'form': form,
            'matter': matter,
            'duedatelist': duedates,
            'm_id': pk,
            'client': client,

        }
        return render(request, 'associates_apps/ipdetailform.html', context)

    else:

        try:
            casematter = CaseMatter.objects.get(matter__id=pk)
            sw = 1
        except ObjectDoesNotExist:
            sw = 0

        if request.method == 'POST':
            if sw == 0:
                form = Non_IPDetailForm(request.POST)
            else:
                form = Non_IPDetailForm(request.POST, instance=casematter)

            if form.is_valid():
                form.save()
                return redirect('associate-matter-review', pk)
            else:
                return redirect('associate-matter-review', pk)

        else:
            if sw == 0:
                form = Non_IPDetailForm()
            else:
                form = Non_IPDetailForm(instance=casematter)

        context = {
            'form': form,
            'matter': matter,
            'm_id': pk,
            'client': client,
        }
        return render(request, 'associates_apps/nonipdetailform.html', context)


def matter_classofgoods(request, pk, sk):
    matter = Matters.objects.get(id=pk)
    listofgoods = ClassOfGoods.objects.filter(matter__id=pk)
    if sk == "Trademark":
        if request.method == 'POST':
            form = ClassOfGoodsEntry(request.POST)
            if form.is_valid():
                form.save()
                return redirect('associate-matter-clasofgoods', pk, sk)
            else:
                return redirect('associate-matter-clasofgoods', pk, sk)
        else:
            form = ClassOfGoodsEntry()

        context = {
            'form': form,
            'm_id': pk,
            'matter': matter,
            'listofgoods': listofgoods,
        }
        return render(request, 'associates_apps/classofgoods.html', context)


def editclassofgoods(request, pk, cl):
    selected = ClassOfGoods.objects.get(id=cl)
    matter = Matters.objects.get(id=pk)
    listofgoods = ClassOfGoods.objects.filter(matter__id=pk)
    if request.method == "POST":
        form = ClassOfGoodsEntry(request.POST, instance=selected)
        if form.is_valid():
            form.save()
            return redirect('associate-matter-clasofgoods', pk, 'Trademark')
        else:
            return redirect('associate-matter-clasofgoods', pk, 'Trademark')
    else:

        form = ClassOfGoodsEntry(instance=selected)
        context = {
            'form': form,
            'matter': matter,
            'listofgoods': listofgoods,
        }
    return render(request, 'associates_apps/classofgoods.html', context)


def portfolio_new_task(request, m_id):
    matter = Matters.objects.get(id=m_id)
    activities = task_detail.objects.filter(matter__id=m_id)
    duedatelist = AppDueDate.objects.filter(matter__id=m_id)

    if request.method == "POST":
        # Get the posted form
        form = TaskEntryForm1(request.POST)
        if form.is_valid():
            task_det = task_detail()
            task_det.matter = form.cleaned_data['matter']
        #   task_det.matter = matter.id
            task_det.tran_date = form.cleaned_data['tran_date']
            task_det.doc_type = form.cleaned_data['doc_type']
            task_det.task_code = form.cleaned_data['task_code']
            task_det.tran_type = form.cleaned_data['tran_type']
            task_det.preparedby = form.cleaned_data['preparedby']
            task_det.lawyer = form.cleaned_data['lawyer']
            task_det.task = form.cleaned_data['task']
            task_det.save()
            return redirect('associate-view_portfolio', m_id)
        else:
            return redirect('associate-portfolio_new_task', m_id)
    else:
        form = TaskEntryForm1()

    context = {
        'form': form,
        'matter': matter,
        'activities': activities,
        'duedatelist': duedatelist,
        'm_id': m_id,
    }
    return render(request, 'associates_apps/add_porfolio_new_task.html', context)


def add_duedate(request, pk):
    matter = Matters.objects.get(id=pk)
    m_id = matter.folder.client.id
    client = Client_Data.objects.get(id=m_id)

    if request.method == "POST":
        # Get the posted form
        form = DueDateEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('associate-add_duedate', pk)
        else:
            return redirect('associate-add_duedate', pk)
    else:
        form = DueDateEntryForm()

    context = {
        'form': form,
        'matter': matter,
        'm_id': pk,
        'client': client,
    }
    return render(request, 'associates_apps/add_new_duedate.html', context)


def modify_duedate(request, pk, m_id):
    task = AppDueDate.objects.get(id=pk)
    matter = Matters.objects.get(id=m_id)
    activities = task_detail.objects.filter(matter__id=m_id)

    c_id = matter.folder.client.id
    client = Client_Data.objects.get(id=c_id)

    if request.method == 'POST':
        task_form = DueDateEntryForm(request.POST, instance=task)
        if task_form.is_valid():
            task_form.save()
            return redirect('associate-matter-review', m_id)
        else:
            task_form = DueDateEntryForm(instance=task)
    else:
        task_form = DueDateEntryForm(instance=task)

    context = {
        'form': task_form,
        'pk': pk,
        'm_id': m_id,
        'matter': matter,
        'client': client,
        'tasks': activities,
    }
    return render(request, 'associates_apps/modify_duedate.html', context)


def remove_task(request, pk, m_id):
    selected = task_detail.objects.get(id=pk)
    selected.delete()
    return redirect('associate-matter-review', m_id)


def remove_duedate(request, pk, m_id):
    selected = AppDueDate.objects.get(id=pk)
    selected.delete()
    return redirect('associate-matter-review', m_id)


def add_task(request, pk):
    def perform_billable_services():

        def save_to_tempPF():
            #            print("Pumasok sa saving of PF")

            tempbills = TempBills.objects.filter(
                matter_id=matter_id, tran_date=tran_date, bill_service_id=bill_id)
            if tempbills.exists():
                pass
            else:
                # if prate > 0:
                #     pesoamount = (PF_amount * prate)
                # else:
                #     prate = 0
                #     pesoamount = 0

                tempbills = TempBills(
                    matter_id=matter_id,
                    tran_date=tran_date,
                    bill_service_id=bill_id,
                    lawyer_id=lawyer,
                    particulars=bill_description,
                    amount=PF_amount,
                    # pesorate=prate,
                    currency=currency)
                tempbills.save()

        tran_type = request.POST["tran_type"]
        task_code = request.POST["task_code"]
        tran_date = request.POST["tran_date"]
        if tran_type is None:
            pass
        else:
            result = ActivityCodes.objects.filter(id=task_code)
            matter_id = matter.id
            apptype = matter.apptype_id
            lawyer = matter.handling_lawyer_id
            for activitycode in result:
                #                print("pumasok sa result")
                bill_description = activitycode.bill_description
                bill_id = activitycode.id
                PF_amount = activitycode.amount
                prate = activitycode.pesorate
                currency = activitycode.currency
#                print(bill_description, bill_id, PF_amount, pesorate)
                save_to_tempPF()

    matter = Matters.objects.get(id=pk)
    codes = IPTaskCodes.objects.all()
    tasks = task_detail.objects.filter(matter__id=pk)
    if request.method == "POST":
        # Get the posted form
        form = TaskEntryForm(request.POST)
        if form.is_valid():
            form.save()
            perform_billable_services()

            return redirect('associate-matter-review', pk)
        else:
            return redirect('associate-matter-review', pk)
    else:
        form = TaskEntryForm()

    context = {
        'form': form,
        'matter': matter,
        'm_id': pk,
        'codes': codes,
        'tasks': tasks,
    }
    return render(request, 'associates_apps/add_new_task.html', context)


def add_new_task(request, pk, m_id):
    matter = Matters.objects.get(id=m_id)
    if request.method == "POST":
        # Get the posted form
        form = TaskEntryForm(request.POST)
        if form.is_valid():
            form.save()
#         return redirect('associate-matter-review', pk, m_id)
        else:
            return redirect('associate-add_new_task', pk, m_id)
    else:
        form = TaskEntryForm()

    context = {
        'form': form,
        'matter': matter,
        'pk': pk,
        'm_id': m_id,
    }
    return render(request, 'associates_apps/add_new_task.html', context)


def modify_task(request, pk, m_id):
    def perform_billable_services():

        def save_to_tempPF():
            #            print("Pumasok sa saving of PF")

            tempbills = TempBills.objects.filter(
                matter_id=matter_id, tran_date=tran_date, bill_service_id=bill_id)
            if tempbills.exists():
                pass
            else:
                # if prate > 0:
                #     pesoamount = (PF_amount * prate)
                # else:
                #     prate = 0
                #     pesoamount = 0

                tempbills = TempBills(
                    matter_id=matter_id,
                    tran_date=tran_date,
                    bill_service_id=bill_id,
                    lawyer_id=lawyer,
                    particulars=bill_description,
                    amount=PF_amount,
                    # pesorate=prate,
                    currency=currency)
                tempbills.save()

        tran_type = request.POST["tran_type"]
        task_code = request.POST["task_code"]
        tran_date = request.POST["tran_date"]
        if tran_type is None:
            pass
        else:
            result = ActivityCodes.objects.filter(id=task_code)
            matter_id = matter.id
            apptype = matter.apptype_id
            lawyer = matter.handling_lawyer_id
            for activitycode in result:
                #                print("pumasok sa result")
                bill_description = activitycode.bill_description
                bill_id = activitycode.id
                PF_amount = activitycode.amount
                prate = activitycode.pesorate
                currency = activitycode.currency
#                print(bill_description, bill_id, PF_amount, pesorate)
                save_to_tempPF()

    task = task_detail.objects.get(id=pk)
    matter = Matters.objects.get(id=m_id)
    c_id = matter.folder.client.id
    client = Client_Data.objects.get(id=c_id)
    docs = FilingDocs.objects.filter(Task_Detail__id=pk)
    duedates = AppDueDate.objects.filter(matter__id=m_id)

    if request.method == 'POST':
        task_form = TaskEntryForm(request.POST, instance=task)
        if task_form.is_valid():
            task_form.save()
            perform_billable_services()
#            return redirect('associate-matter-review', m_id)
        else:
            task_form = TaskEntryForm(instance=task)
    else:
        task_form = TaskEntryForm(instance=task)

    context = {
        'form': task_form,
        'pk': pk,
        'm_id': m_id,
        'matter': matter,
        'docs': docs,
        'duedates': duedates,
        'client': client
    }
    return render(request, 'associates_apps/modify_task.html', context)


def recent_modify_task(request, pk, d_id):
    task = task_detail.objects.get(id=pk)
    m_id = task.matter.id
    print(m_id)
    matter = Matters.objects.get(id=m_id)
    docs = FilingDocs.objects.filter(Task_Detail__id=pk)
    duedates = AppDueDate.objects.filter(matter__id=m_id)

    if request.method == 'POST':
        task_form = TaskEntryForm(request.POST, instance=task)
        if task_form.is_valid():
            task_form.save()
            return redirect('associate-home')
        else:
            task_form = TaskEntryForm(instance=task)
    else:
        task_form = TaskEntryForm(instance=task)

    context = {
        'form': task_form,
        'pk': pk,
        'm_id': m_id,
        'd_id': d_id,
        'matter': matter,
        'docs': docs,
        'duedates': duedates,
    }
    return render(request, 'associates_apps/recent_modify_task.html', context)


def edit_task(request, m_id, t_id):
    task = task_detail.objects.get(id=t_id)
    matter = Matters.objects.get(id=m_id)
    activities = task_detail.objects.filter(matter__id=m_id)
    duedatelist = AppDueDate.objects.filter(matter__id=m_id)
    if request.method == 'POST':
        task_form = TaskEntryForm(request.POST, instance=task)
        if task_form.is_valid():
            task_form.save()
            return redirect('associate-view_portfolio', m_id)
        else:
            task_form = TaskEntryForm(instance=task)
    else:
        task_form = TaskEntryForm(instance=task)

    context = {
        'form': task_form,
        'matter': matter,
        'm_id': m_id,
        't_id': t_id,
        'activities': activities,
        'duedatelist': duedatelist,
    }
#    return render(request, 'associates_apps/edit_task.html', context)
    return render(request, 'associates_apps/add_porfolio_new_task.html', context)


def newdocs(request, pk, m_id, frm):
    matter = Matters.objects.get(id=m_id)
    task = task_detail.objects.get(id=pk)
    if request.method == "POST":
        # Get the posted form
        form = FilingDocsEntry(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('associate-list_uploaded_docs', pk, m_id)
        else:
            return redirect('associate-add_new_task', pk, m_id)
    else:
        form = FilingDocsEntry()

    context = {
        'form': form,
        'matter': matter,
        'task': task,
        'pk': pk,
        'm_id': m_id,
        't_id': pk
    }
    if frm == 0:
        return render(request, 'associates_apps/add_new_docs.html', context)
    elif frm == 1:
        return render(request, 'associates_apps/add_new_docs_mailsin.html', context)


def upload_new_docs(request, pk, m_id):
    task = task_detail.objects.get(id=pk)
    matter = Matters.objects.get(id=m_id)
    if request.method == "POST":
        form = FilingDocsEntry(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('associate-matter-review', m_id)
        else:
            form = FilingDocsEntry(request.POST, request.FILES)
    else:
        form = FilingDocsEntry(request.POST, request.FILES)

    context = {
        'form': form,
        'matter': matter,
        'task': task,
        'pk': pk,
        'm_id': m_id,
    }

    return render(request, 'associates_apps/add_new_docs.html', context)


def list_uploaded_docs(request, t_id, m_id):
    matter = Matters.objects.get(id=m_id)
    tdetail = task_detail.objects.get(id=t_id)
    uploaded_docs = FilingDocs.objects.filter(Task_Detail__id=t_id)

    context = {
        'uploaded_docs': uploaded_docs,
        'tdetail': tdetail,
        'matter': matter,
        't_id': t_id,
        'm_id': m_id,
    }

    return render(request, 'associates_apps/uploaded_doclist.html', context)


def duedate_entry(request, m_id):
    matter = Matters.objects.get(id=m_id)
    activities = task_detail.objects.filter(matter__id=m_id)
    duedatelist = AppDueDate.objects.filter(matter__id=m_id)

    if request.method == "POST":
        form = DueDateEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('associate-view_portfolio', m_id)
        else:
            return redirect('associate-portfolio_DueDateEntry', m_id)
    else:
        form = DueDateEntryForm()

    context = {
        'form': form,
        'matter': matter,
        'activities': activities,
        'duedatelist': duedatelist,

    }

    return render(request, 'associates_apps/entry_duedate.html', context)


def duedate_modify(request, pk, m_id):
    matter = Matters.objects.get(id=m_id)
    duedate = AppDueDate.objects.get(id=pk)
    activities = task_detail.objects.filter(matter__id=m_id)
    duedatelist = AppDueDate.objects.filter(matter__id=m_id)

    if request.method == 'POST':
        form = DueDateEntryForm(request.POST, instance=duedate)
        if form.is_valid():
            form.save()
            return redirect('associate-view_portfolio', m_id)
        else:
            form = DueDateEntryForm(instance=duedate)
    else:
        form = DueDateEntryForm(instance=duedate)

    context = {
        'form': form,
        'matter': matter,
        'm_id': m_id,
        'pk': pk,
        'activities': activities,
        'duedatelist': duedatelist,

    }
    return render(request, 'associates_apps/entry_duedate.html', context)


def duedate_remove(request, pk, m_id):
    selected = AppDueDate.objects.get(id=pk)
    selected.delete()
    return redirect('associate-view_portfolio', m_id)


def billing_list(request):
    access_code = request.user.user_profile.userid

    if 'q' in request.GET:
        q = request.GET['q']
        multiple_q = Q(Q(matter__matter_title__icontains=q) | Q(matter__folder__client__client_name__icontains=q) | Q(
            matter__folder__folder_description__icontains=q) | Q(bill_number__icontains=q) | Q(matter__referenceno__icontains=q))
        arlist = AccountsReceivable.objects.filter(
            multiple_q, matter__handling_lawyer__lawyerID__userid=access_code).order_by("-bill_date")
    else:
        #matters = Matters.objects.filter(handling_lawyer__lawyerID__userid=access_code).order_by("-filing_date")
        arlist = AccountsReceivable.objects.filter(
            matter__handling_lawyer__lawyerID__userid=access_code).order_by("-bill_date")

        #matters = Matters.objects.filter(multiple_q, handlinglawyer__lawyerID__userid=access_code)

    noofbills = arlist.count()
    page = Paginator(arlist, 11)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    context = {
        'page': page,
        'noofmatters': noofbills,
        #        'matters' : all_matters
    }


#     context = {
#         'page'    : page,
#         'noofmatters': noofbills,
# #        'arlist' : arlist

#     }
    return render(request, 'associates_apps/billinglist.html', context)


def mails_inward(request):
    access_code = request.user.user_profile.userid
    # if 'q' in request.GET:
    #     q = request.GET['q']
    #     multiple_q = Q(Q(client__icontains=q) | Q(folder__client__client_name__icontains=q) | Q(folder__folder_description__icontains=q) | Q(referenceno__icontains=q))
    #     docs = MailsIn.objects.filter(Task_Detail__matter__handling_lawyer__lawyerID__userid=access_code).order_by('-DocDate')
    # else:
#    docs = MailsIn.objects.filter(Task_Detail__matter__handling_lawyer__lawyerID__userid=access_code and Task_Detail.doc_type = "").order_by('-DocDate')
    docs = task_detail.objects.filter(
        matter__handling_lawyer__lawyerID__userid=access_code, doc_type='Incoming').order_by('-tran_date')

    noofmatters = docs.count()
    paginator = Paginator(docs, 11)
    page = request.GET.get('page')
    all_matters = paginator.get_page(page)

    context = {
        'page': page,
        'noofmatters': noofmatters,
        'matters': all_matters,

    }
    return render(request, 'associates_apps/mailsin.html', context)


def mails_inward_update(request, pk, m_id):
    def validateduedates():
        def computeduedate():
            if basisofcompute == "In Months":
                nmonths = int(terms)
                svalue = ("+"+str(nmonths))
                sduedate = sdate + relativedelta(months=int(svalue))
                duedate = sduedate

            if basisofcompute == "In Years":
                nyears = int(terms)
                svalue = ("+"+str(nyears))
                sduedate = sdate + relativedelta(years=int(svalue))
                duedate = sduedate

            if basisofcompute == "In Days":
                ndays = int(terms)
                svalue = ("+"+str(ndays))
                sduedate = sdate + relativedelta(days=int(svalue))
                duedate = sduedate

            dues = AppDueDate.objects.filter(
                matter_id=matter_id, duedate=duedate)
            if dues.exists():
                pass
            else:
                duedates = AppDueDate(
                    matter_id=matter_id, duedate=duedate, particulars=particulars)
                duedates.save()

        foldertype = matter.folder.folder_type
        task = task_detail.objects.get(id=pk)

        duecode = request.POST["duecode"]
        if duecode is None:
            pass
        else:
            result = DueCode.objects.filter(id=duecode)
            matter_id = matter.id
            apptype = matter.apptype_id
            lawyer = matter.handling_lawyer_id
            for duecodes in result:
                basisofcompute = duecodes.basisofcompute
                terms = duecodes.terms

                particulars = duecodes.Description
                if duecodes.fieldbsis == 'OA Mailing Date' and duecodes.apptype_id == apptype:
                    tran_date = task.mailing_date
                    appdate = tran_date
                    sdate = appdate
                    if sdate is None:
                        pass
                    else:
                        computeduedate()
                else:
                    if duecodes.fieldbsis == 'Document Receipt Date' and duecodes.apptype_id == apptype:
                        print("pumasok")
                        tran_date = task.tran_date
                        print(tran_date)
                        appdate = tran_date
                        sdate = appdate
                        if sdate is None:
                            pass
                        else:
                            computeduedate()

    matter = Matters.objects.get(id=m_id)
    task = task_detail.objects.get(id=pk)
    duedates = AppDueDate.objects.filter(matter__id=m_id)
    docs = FilingDocs.objects.filter(Task_Detail__id=pk)

    c_id = task.matter.folder.client.id
    client = Client_Data.objects.get(id=c_id)

    if request.method == 'POST':
        task_form = TaskEntryForm(request.POST, instance=task)
        if task_form.is_valid():
            task_form.save()
            apptype = matter.apptype.apptype
#            if apptype == "Trademark":
            validateduedates()

            return redirect('associate-mails_inward')
        else:
            task_form = TaskEntryForm(instance=task)
    else:
        task_form = TaskEntryForm(instance=task)

    context = {
        'form': task_form,
        'client': client,
        'pk': pk,
        'mails': task,
        'matter': matter,
        'duedates': duedates,
        'docs': docs,
    }
    return render(request, 'associates_apps/mailsinwardet.html', context)


def mails_inward_new(request):
    access_code = request.user.user_profile.userid
    docs = task_detail.objects.filter(
        matter__handling_lawyer__lawyerID__userid=access_code, doc_type='Incoming').order_by('-tran_date')

    if request.method == 'POST':
        task_form = TaskEntryForm(request.POST)
        if task_form.is_valid():
            task_form.save()
            return redirect('associate-mails_inward')
        else:
            task_form = TaskEntryForm()
    else:
        task_form = TaskEntryForm()

    context = {
        'form': task_form,
        'matters': docs,
    }
    return render(request, 'associates_apps/newinward.html', context)


def modifyAR(request, pk, m_id):
    ardetails = AccountsReceivable.objects.get(id=pk)
    bills = Bills.objects.filter()

    matter = Matters.objects.get(id=m_id)
    if request.method == 'POST':
        form = AREntryForm(request.POST, request.FILES, instance=ardetails)
        if form.is_valid():
            form.save()
            return redirect('associate-matter-review', m_id)
        else:
            form = AREntryForm(instance=ardetails)
    else:
        form = AREntryForm(instance=ardetails)

    context = {
        'form': form,
        'matter': matter,
        'm_id': m_id,

    }

    return render(request, 'associates_apps/entry_ar.html', context)


def viewfiled_document(request, pk, m_id, t_id):
    fileddocs = FilingDocs.objects.get(id=pk)
    matter = Matters.objects.get(id=m_id)
    if request.method == 'POST':
        form = DocumentEditForm(
            request.POST, request.FILES, instance=fileddocs)
        if form.is_valid():
            form.save()
            return redirect('associate-list_uploaded_docs', pk, m_id)
        else:
            form = DocumentEditForm(instance=fileddocs)
    else:
        form = DocumentEditForm(instance=fileddocs)

    context = {
        'form': form,
        'matter': matter,
        'docs': fileddocs,
        't_id': t_id,
        'm_id': m_id,

    }

    return render(request, 'associates_apps/editdocument.html', context)

    # return render(request, 'associates_apps/add_new_docsbak.html', context)


@login_required
def arentry(request, m_id):
    matter = Matters.objects.get(id=m_id)
    if request.method == "POST":
        form = AREntryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('associate-matter-review', m_id)
        else:
            return redirect('associate-ar-new', m_id)
    else:
        form = AREntryForm()
        context = {
            'form': form,
            'matter': matter,
            'm_id': m_id,
        }

    return render(request, 'associates_apps/entry_ar.html', context)


def recentviewdocs(request, pk):
    docs = FilingDocs.objects.get(id=pk)
    lawyer = docs.Task_Detail.lawyer
    matterid = docs.Task_Detail.matter.id
    matter = Matters.objects.get(id=matterid)
    form = DocumentEditForm(instance=docs)

    if request.method == 'POST':
        form = DocumentEditForm(request.POST, request.FILES, instance=docs)
        if form.is_valid():
            #            form.save()
            return redirect('associate-home')
        else:
            form = DocumentEditForm(instance=docs)
    else:
        form = DocumentEditForm(instance=docs)

    context = {
        'form': form,
        'lawyer': lawyer,
        'matter': matter,

    }
    return render(request, 'associates_apps/recentdocsview.html', context)


def recentviewduedates(request, pk):
    duedate = AppDueDate.objects.get(id=pk)
    matterid = duedate.matter.id
    activity = task_detail.objects.filter(matter__id=matterid)
    matter = Matters.objects.get(id=matterid)
    ARBills = AccountsReceivable.objects.filter(
        matter__id=matterid, payment_tag="UN")
    Total_bill_amount = AccountsReceivable.objects.filter(
        matter__id=matterid, payment_tag="UN").aggregate(Sum('bill_amount'))
    Unpaid_amt = Total_bill_amount["bill_amount__sum"]

    if request.method == 'POST':
        form = DueDateEntryForm(request.POST, instance=duedate)
        if form.is_valid():
            form.save()
            return redirect('associate-home')
        else:
            form = DueDateEntryForm(instance=duedate)
    else:
        form = DueDateEntryForm(instance=duedate)

    context = {
        'form': form,
        'matter': matter,
        'activity': activity,
        'ARBills': ARBills,
        'total_unpaid': Unpaid_amt,
        'due_id': pk,

    }
    return render(request, 'associates_apps/recentduedateview.html', context)


def recentactivities(request, pk):
    task = task_detail.objects.get(id=pk)
    m_id = task.matter.id
    matter = Matters.objects.get(id=m_id)
    #activities = task_detail.objects.filter(matter__id=m_id)
    listofdocs = FilingDocs.objects.filter(Task_Detail__id=pk)
    duedates = AppDueDate.objects.filter(matter__id=m_id)
    unpaidbills = AccountsReceivable.objects.filter(matter__id=m_id)
    form = TaskEntryForm(instance=task)

    context = {
        'form': form,
        'matter': matter,
        'listofdocs': listofdocs,
        'duedates': duedates,
        'task': task,
        'm_id': m_id

    }
    return render(request, 'associates_apps/recenttaskview.html', context)


def recentactivities_add_task(request, pk, m_id):
    matter = Matters.objects.get(id=m_id)
    codes = IPTaskCodes.objects.all()
    if request.method == "POST":
        # Get the posted form
        form = TaskEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recent-duedate-review', pk)
        else:
            return redirect('recent-add_task', pk, m_id)
    else:
        form = TaskEntryForm()

    context = {
        'form': form,
        'matter': matter,
        'd_id': pk,
        'codes': codes,
    }
    return render(request, 'associates_apps/recent_add_task.html', context)


def recent_taskviewdocs(request, pk, frm):
    docs = FilingDocs.objects.get(id=pk)
    t_id = docs.Task_Detail.id
    lawyer = docs.Task_Detail.lawyer
    matterid = docs.Task_Detail.matter.id
    matter = Matters.objects.get(id=matterid)
    form = DocumentEditForm(instance=docs)

    if request.method == 'POST':
        form = DocumentEditForm(request.POST, request.FILES, instance=docs)
        if form.is_valid():
            form.save()
            return redirect('associate-home')
        else:
            form = DocumentEditForm(instance=docs)
    else:
        form = DocumentEditForm(instance=docs)

    context = {
        'form': form,
        'lawyer': lawyer,
        'matter': matter,
        't_id': t_id,
        'm_id': matterid,

    }
    if frm == 0:
        return render(request, 'associates_apps/recenttaskdocsview.html', context)
    elif frm == 1:
        return render(request, 'associates_apps/taskdocsview.html', context)


def add_expensedetails(request, pk, t_id):
    listofexpenses = TempExpenses.objects.filter(matter__id=pk)
    task = task_detail.objects.get(id=t_id)
    matter = Matters.objects.get(id=pk)
    if request.method == 'POST':
        form = EntryExpensesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('associate-add-ope', pk, t_id)
        else:
            form = EntryExpensesForm()
    else:
        form = EntryExpensesForm()

    context = {
        'form': form,
        'listofexpenses': listofexpenses,
        'matter': matter,
        'task': task,
    }

    return render(request, 'associates_apps/listofexpenses.html', context)


def add_PFdetails(request, pk):
    listofservices = TempBills.objects.filter(matter__id=pk)
    Unpaid = TempBills.objects.filter(matter__id=pk).aggregate(Sum('amount'))
    TPF_amt = Unpaid["amount__sum"]

    matter = Matters.objects.get(id=pk)
    if request.method == 'POST':
        form = EntryBillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('associate-add-PF', pk)
        else:
            form = EntryBillForm()
    else:
        form = EntryBillForm()

    context = {
        'form': form,
        'listofservices': listofservices,
        'matter': matter,
        'TPF_amt': TPF_amt,
    }

    return render(request, 'associates_apps/listofservices.html', context)


def myunbilledactivity(request):
    access_code = request.user.user_profile.userid
    username = request.user.username
    # result = task_detail.objects.values('matter__id','matter__matter_title').annotate(NoOfActivities=Count('task_code')).filter(matter__handling_lawyer__lawyerID__userid=access_code, tran_type="Billable").order_by('-NoOfActivities')

    result = task_detail.objects.values('matter__id', 'matter__matter_title', 'task_code__Activity').annotate(NoOfActivities=Count(
        'task_code')).filter(matter__handling_lawyer__lawyerID__userid=access_code, tran_type="Billable").order_by('-NoOfActivities')

    context = {
        'result': result,
    }

    return render(request, 'associates_apps/myunbilledactivity.html', context)


def unbilledactivitydetails(request):
    pass
    access_code = request.user.user_profile.userid
    username = request.user.username
    unbilled_activities = task_detail.objects.filter(
        matter__handling_lawyer__lawyerID__userid=access_code, tran_type="Billable")
    # result = task_detail.objects.values('matter__id','matter__matter_title').annotate(NoOfActivities=Count('task_code')).filter(matter__handling_lawyer__lawyerID__userid=access_code, tran_type="Billable").order_by('-NoOfActivities')
    print(unbilled_activities)

    context = {
        'unbilled': unbilled_activities,
    }

    return render(request, 'associates_apps/unbilledactivitydetails.html', context)


def myfolderlist(request):
    access_code = request.user.user_profile.userid
    username = request.user.username
    result = Matters.objects.values('folder__folder_type__id', 'folder__folder_type__folder').annotate(
        NoOfMatters=Count('matter_title')).filter(handling_lawyer__lawyerID__userid=access_code).order_by('-NoOfMatters')
    print(result)

    context = {
        'result': result,
    }

    return render(request, 'associates_apps/myfolderlist.html', context)


def myclientlist(request):
    access_code = request.user.user_profile.userid
    username = request.user.username
    result = Matters.objects.values('folder__client__id', 'folder__client__client_name').annotate(
        NoOfMatter=Count('matter_title')).filter(handling_lawyer__lawyerID__userid=access_code).order_by('-NoOfMatter')
    # TotalCount = result.objects.aggregate(Sum('NoOfMatter'))
    # TotalCount = TotalCount["NoOfMatters"]
#    result.objects.aggregate(Sum('NoOfMatters'))

    #  prev_bill_amount = AccountsReceivable.objects.filter(bill_date__year = today.year, bill_date__month = prev_month).aggregate(Sum('bill_amount'))
    # prev_bill_amt = prev_bill_amount["bill_amount__sum"]

    context = {
        'result': result,
    }

    return render(request, 'associates_apps/myclientlist.html', context)


def myfolderdetail(request, pk):
    access_code = request.user.user_profile.userid
    typeoffolder = FolderType.objects.get(id=pk)
    matters = Matters.objects.filter(
        folder__folder_type__id=pk, handling_lawyer__lawyerID__userid=access_code)

    context = {
        'folder_type': typeoffolder,
        'matters': matters,
    }

    return render(request, 'associates_apps/myfolderdetails.html', context)


def myclientdetail(request, pk):
    access_code = request.user.user_profile.userid
    username = request.user.username
    client = Client_Data.objects.get(id=pk)
    matters = Matters.objects.filter(
        folder__client_id=pk, handling_lawyer__lawyerID__userid=access_code)

    context = {
        'client': client,
        'matters': matters,
    }

    return render(request, 'associates_apps/myclientdetails.html', context)


def mybillinglist(request):
    access_code = request.user.user_profile.userid
    username = request.user.username
#    result = AccountsReceivable.objects.filter(, payment_tag='UNPAID')
    result = AccountsReceivable.objects.filter(
        lawyer__lawyerID__userid=access_code, payment_tag='UN').order_by('matter')

    print(result)
    Unpaid = AccountsReceivable.objects.filter(
        lawyer__lawyerID__userid=access_code, payment_tag='UN').aggregate(Sum('bill_amount'))
    Tbill_amt = Unpaid["bill_amount__sum"]

    context = {
        'result': result,
        'TBillAmt': Tbill_amt
    }

    return render(request, 'associates_apps/mybillinglist.html', context)


def mybillingdetail(request, c_id, m_id, ar_id):
    client = Client_Data.objects.get(id=c_id)
    matter = Matters.objects.get(id=m_id)
    ARdetails = AccountsReceivable.objects.get(id=ar_id)

    bills = Bills.objects.filter(bill_number=ar_id)
    billamt = Bills.objects.filter(bill_number=ar_id).aggregate(Sum('amount'))
    Tbill_amt = billamt["amount__sum"]

    Ofees = OFees.objects.filter(bill_number=ar_id)
    feeamt = OFees.objects.filter(bill_number=ar_id).aggregate(Sum('amount'))
    Tfee_amt = feeamt["amount__sum"]

    Ope = OPE.objects.filter(bill_number=ar_id)
    opeamount = OPE.objects.filter(bill_number=ar_id).aggregate(Sum('amount'))
    Tope_amt = opeamount["amount__sum"]

    payments = Payments.objects.filter(bill_number=ar_id)
    payamt = Payments.objects.filter(
        bill_number=ar_id).aggregate(Sum('pay_amount'))
    Tpayments = payamt["pay_amount__sum"]

    if Tpayments == None:
        Tpayments = 0
    if Tope_amt == None:
        Tope_amt = 0
    if Tfee_amt == None:
        Tfee_amt = 0
    if Tbill_amt == None:
        Tbill_amt = 0

    G_total = Tbill_amt + Tfee_amt + Tope_amt
    balance = G_total-Tpayments

    context = {
        'client': client,
        'matter': matter,
        'ARdetails': ARdetails,
        'bills': bills,
        'Ofees': Ofees,
        'Ope': Ope,
        'Tbill_amt': Tbill_amt,
        'Tfee_amt': Tfee_amt,
        'Tope_amt': Tope_amt,
        'Tpayments': Tpayments,
        'G_total': G_total,
        'Balance': balance,

    }

    return render(request, 'associates_apps/mybillingdetails.html', context)


def clientfulldetail(request, pk):
    client = Client_Data.objects.get(id=pk)

    context = {
        'client': client,
    }
    return render(request, 'associates_apps/clientfulldetails.html', context)


def matterfulldetail(request, pk):
    matter = Matters.objects.get(id=pk)

    context = {
        'matter': matter,
    }
    return render(request, 'associates_apps/casefulldetails.html', context)
