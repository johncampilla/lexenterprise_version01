from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from adminapps.models import *
from django.shortcuts import render, redirect
from datetime import date, datetime, timedelta
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from adminapps.forms import InboxMessageNewForm, MailsInwardForm, EntryBillForm, EntryExpensesForm, Non_IPDetailForm, ClassOfGoodsEntry, IPDetailForm, AREntryForm, EntryMatterForm, DocumentEditForm, TaskEntryForm1, TaskEntryForm, TaskEntryFormLawyer, FilingDocsEntry, AlertMessageForm, AlertUpdateStatusForm, DueDateEntryForm, InboxAttachmentEntryForm, ReplyToMessageForm, NewAwaitingDocForm
from django.db.models import Q, Sum, Count



# Create your views here.
today = date.today()
curr_month = today.month % 12
prev_month = today.month - 1
if prev_month == 0:
    prev_month = 12

@login_required
def main(request):
    access_code = request.user.user_profile.userid
    username = request.user.username
#    alertmessages = Alert_Messages.objects.filter(messageto=access_code)
    user_message_id = request.user.user_profile.id
    open_clients = client_user_profile.objects.filter(user__username = access_code)
    sclient = open_clients[0]
    s_id = sclient.client_id
    open_folders = CaseFolder.objects.filter(client__id = s_id)
    matterlist = Matters.objects.filter(folder__client_id = s_id)
    alertmessages = inboxmessage.objects.filter(
        messageto_id=user_message_id, status="UNREAD")
    countalert = alertmessages.count()

    duedates = AppDueDate.objects.filter(duedate__year=today.year, duedate__month=today.month,
                                         matter__handling_lawyer__lawyerID__userid=access_code, date_complied__isnull=True).order_by('-duedate')
    recentdocs = FilingDocs.objects.filter(
        Task_Detail__lawyer__lawyerID__userid=access_code).order_by('-DocDate')
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
        'username': username,
        'noofalerts': countalert,
        'duedates': duedates,
        'recenttask': recenttask,
        'recentdocs': recentdocs,
        'recent_billables': recent_billables,
        'matterlist': matterlist,
        'number_of_task': number_of_task,
        'number_of_dues': number_of_dues,
        'number_of_docs': number_of_docs,

    }
    return render(request, 'clientuserapps/index.html', context)

def matter_review(request, pk):
    matter = Matters.objects.get(id=pk)
    c_id = matter.folder.client.id
    client = Client_Data.objects.get(id=c_id)
    appduedates = AppDueDate.objects.filter(matter__id=pk).order_by('-duedate')
    tempbills = TempBills.objects.filter(matter__id=pk).order_by('-tran_date')
    tempfilings = TempFilingFees.objects.filter(matter__id=pk)
    expenses = TempExpenses.objects.filter(
        Q(matter__id=pk), Q(status='O') | Q(status='P'))
    if request.method == 'POST':
        form = EntryMatterForm(request.POST, instance=matter)
        if form.is_valid():
            form.save()
            apptype = matter.apptype.apptype
        else:
            form = EntryMatterForm(instance=matter)
    else:
        form = EntryMatterForm(instance=matter)

    activities = task_detail.objects.filter(
        matter__id=pk).order_by('-tran_date')
    duedatelist = AppDueDate.objects.filter(matter__id=pk).order_by('-duedate')
    ardetails = AccountsReceivable.objects.filter(
        matter__id=pk).order_by('-bill_date')
    payments = Payments.objects.filter(
        bill_number__matter__id=pk).order_by('-payment_date')
    filingdocs = FilingDocs.objects.filter(
        Task_Detail__matter__id=pk).order_by('-DocDate')
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
        'tempbills': tempbills,
        'tempfilings': tempfilings,
        'apptype': apptype,
        'duelist': appduedates,

    }

    return render(request, 'clientuserapps/openmatter_details.html', context)

def review_task(request, pk, m_id):
    task = task_detail.objects.get(id=pk)
    matter = Matters.objects.get(id=m_id)
    c_id = matter.folder.client.id
    client = Client_Data.objects.get(id=c_id)
    docs = FilingDocs.objects.filter(Task_Detail__id=pk)
    duedates = AppDueDate.objects.filter(matter__id=m_id).order_by('-duedate')
    tmpbills = TempBills.objects.filter(
        matter_id=m_id, tran_date=task.tran_date, bill_service_id=task.task_code_id)
    tmpfees = TempFilingFees.objects.filter(
        matter_id=m_id, tran_date=task.tran_date, bill_service_id=task.task_code_id)
    print(m_id, task.tran_date, task.task_code_id)
    tmpexp = TempExpenses.objects.filter(matter_id=m_id)
    task_list = task_detail.objects.filter(matter__id=m_id)

    if request.method == 'POST':
        task_form = TaskEntryForm(request.POST, instance=task)
        if task_form.is_valid():
            pass
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
        'client': client,
        'tmpbills': tmpbills,
        'tmpfees': tmpfees,
        'tmpexp': tmpexp,
        'task_list': task_list,
    }
    return render(request, 'clientuserapps/review_task.html', context)


#     context = {
#         'client_user' : client_user,

#     } 

def matter_otherdetails(request, pk, sk):
    matter = Matters.objects.get(id=pk)
    m_id = matter.folder.client.id

    client = Client_Data.objects.get(id=m_id)
    listofgoods = ClassOfGoods.objects.filter(matter__id=pk)

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
            'listofgoods':listofgoods,

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
        return render(request, 'clientuserapps/nonipdetailform.html', context)


   
    
