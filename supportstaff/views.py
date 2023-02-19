from asyncio.windows_events import NULL
from contextlib import nullcontext
from queue import Empty
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from pandas import notnull
from adminapps.models import *
from datetime import date, datetime, timedelta
from django.core.paginator import Paginator, EmptyPage
from dateutil.relativedelta import relativedelta
from adminapps.forms import MailsIn_REG, MailsInwardFormNew, InboxAttachmentEntryForm, InboxAttachmentViewForm, InboxMessageNewForm, InboxMessageEntryForm, TaskEditForm, EntryMatterForm, InboxMessageForm, TaskEntryForm, DueDateEntryForm, FilingDocsEntry, EditMatterForm, ReviewMatterForm,IPDetailForm, Non_IPDetailForm, ClassOfGoodsEntry, ApplicantEntryForm, AddTaskEntryForm, ReplyToMessageForm, DocumentEditForm, MailsInwardFormUpdate, newmailform 
from django.db.models import Q, Sum, Count
from django.core.exceptions import ObjectDoesNotExist
from dateutil.relativedelta import relativedelta
from django.contrib import messages
import io

# Create your views here.
today = date.today()
curr_month = today.month % 12
prev_month = today.month - 1
if prev_month == 0:
    prev_month = 12



@login_required
def main(request):
    inifile = sysinifile.objects.first()
    inifile = inifile.company
    ndays = int(1)
    svalue1 = ("+"+str(ndays))
    ndays = int(35)
    svalue2 = ("+"+str(ndays))
    sdate = today - relativedelta(days=int(5))
    duedate1 = sdate
    duedate2 = sdate + relativedelta(days=int(svalue2))
    print(duedate1, duedate2)
    access_code = request.user.user_profile.userid
    user_id = User.id
    user_message_id = request.user.user_profile.id
    alertmessages = inboxmessage.objects.filter(
        messageto_id=user_message_id, status="UNREAD")
    countalert = alertmessages.count()
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

    # multiple_q = Q(Q(matter__handling_lawyer__access_code=code1) | Q(
    #     matter__handling_lawyer__access_code=code2) | Q(matter__handling_lawyer__access_code=code3))

    multiple_q = Q(Q(matter__handling_lawyer__access_code=code1) | Q(matter__handling_lawyer__access_code=code2) | Q(matter__handling_lawyer__access_code=code3) | Q(
        matter__handling_lawyer__access_code=code4) | Q(matter__handling_lawyer__access_code=code5) | Q(matter__handling_lawyer__access_code=code6) | Q(matter__handling_lawyer__access_code=code7))


    #print(multiple_q)
    handlingLawyer_q = Q(Q(handling_lawyer__access_code=code1) | Q(handling_lawyer__access_code=code2) | Q(handling_lawyer__access_code=code3) | Q(handling_lawyer__access_code=code4) | Q(handling_lawyer__access_code=code5) | Q(handling_lawyer__access_code=code6) | Q(handling_lawyer__access_code=code7))


    recentmatters = Matters.objects.filter(handlingLawyer_q, created_at__gte=duedate1, created_at__lte=duedate2).order_by('-created_at')

    recentmatters_count = recentmatters.count()

    duedates = AppDueDate.objects.filter(
        multiple_q, duedate__gte=duedate1, duedate__lte=duedate2, date_complied__isnull=True).order_by('-duedate')
    
    duedates_count = duedates.count()

    messages = inboxmessage.objects.filter(
        messageto__userid=access_code, status='UNREAD')
    if not messages:
        sw = 1
    else:
        sw = 0
    messages_count = messages.count()
    recenttask = task_detail.objects.filter(
        multiple_q, tran_date__year=today.year, tran_date__month=today.month).order_by('-tran_date')
    
    recenttask_count = recenttask.count()

    multiple_q2 = Q(Q(Task_Detail__matter__handling_lawyer__access_code=code1) | Q(Task_Detail__matter__handling_lawyer__access_code=code2) | Q(Task_Detail__matter__handling_lawyer__access_code=code3) | Q
                    (Task_Detail__matter__handling_lawyer__access_code=code4) | Q(Task_Detail__matter__handling_lawyer__access_code=code5) | Q(Task_Detail__matter__handling_lawyer__access_code=code6) | Q(Task_Detail__matter__handling_lawyer__access_code=code7))

    recentdocs = FilingDocs.objects.filter(
        multiple_q2, DocDate__year=today.year, DocDate__month=today.month).order_by('-DocDate')

    context = {
        'alertmessages': alertmessages,
        'noofalerts': countalert,
        'username': username,
        'duedates': duedates,
        'messages': messages,
        'messages_count':messages_count,
        'recenttask': recenttask,
        'recentdocs': recentdocs,
        'duedates_count': duedates_count,
        'recenttask_count':recenttask_count,
        'recentmatters':recentmatters,
        'recentmatters_count':recentmatters_count,
        'inifile':inifile,
        'sw': sw,
    }

    return render(request, 'supportstaff/index.html', context)


# """     matterlist = Matters.objects.filter(
#         Q(handling_lawyer__access_code=code1) | Q(handling_lawyer__access_code=code2) | Q(handling_lawyer__access_code=code3) | Q(handling_lawyer__access_code=code4) | Q(handling_lawyer__access_code=code5) | Q(handling_lawyer__access_code=code6) | Q(handling_lawyer__access_code=code7))
#  """

@login_required
def matterlist(request):
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

    if 'q' in request.GET:
        q = request.GET['q']
        multiple_q = Q(Q(matter_title__icontains=q) | Q(folder__client__client_name__icontains=q) | Q(
            folder__folder_description__icontains=q) | Q(referenceno__icontains=q))

        multiple_l = Q(Q(handling_lawyer__access_code=code1) | Q(handling_lawyer__access_code=code2) | Q(handling_lawyer__access_code=code3) | Q(
            handling_lawyer__access_code=code4) | Q(handling_lawyer__access_code=code5) | Q(handling_lawyer__access_code=code6) | Q(handling_lawyer__access_code=code7))

        matters = Matters.objects.filter(
            multiple_q, multiple_l).order_by("-filing_date")

    else:

        multiple_q = Q(Q(handling_lawyer__access_code=code1) | Q(handling_lawyer__access_code=code2) | Q(handling_lawyer__access_code=code3) | Q(
            handling_lawyer__access_code=code4) | Q(handling_lawyer__access_code=code5) | Q(handling_lawyer__access_code=code6) | Q(handling_lawyer__access_code=code7))

    #    print(multiple_q)

        matters = Matters.objects.filter(multiple_q).order_by("-filing_date")

    noofmatters = matters.count()
    paginator = Paginator(matters, 11)
    page = request.GET.get('page')
    all_matters = paginator.get_page(page)
    user_message_id = request.user.user_profile.id
    alertmessages = inboxmessage.objects.filter(
        messageto_id=user_message_id, status="UNREAD")
    countalert = alertmessages.count()    

    context = {
        'page': page,
        'noofmatters': noofmatters,
        'matters': all_matters,
        'alertmessages': alertmessages,
        'noofalerts': countalert,
        'username': username,


    }
    return render(request, 'supportstaff/listmatters.html', context)


@login_required
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
    appduedates = AppDueDate.objects.filter(matter__id=pk).order_by('-duedate')
#    tempbills = TempBills.objects.filter(matter__id=pk)
#    tempfilings = TempFilingFees.objects.filter(matter__id=pk)

    tempbills = TempBills.objects.filter(Q(matter__id=pk), Q(status='O') | Q(status='P'))
    tempfilings = TempFilingFees.objects.filter(Q(matter__id=pk), Q(status='O') | Q(status='P'))
    expenses = TempExpenses.objects.filter(Q(matter__id=pk), Q(status='O') | Q(status='P'))
    if request.method == 'POST':
        form = EditMatterForm(request.POST, instance=matter)
        if form.is_valid():
            form.save()
#            apptype = request.POST["apptype"]
            apptype = matter.apptype.apptype
#            if apptype == "Trademark":
            validateduedates()
            return redirect('supportstaff-matter_review', pk)
        else:
            form = EditMatterForm(instance=matter)
    else:
        form = EditMatterForm(instance=matter)

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
        'expenses': expenses,
        'tempbills': tempbills,
        'tempfilings': tempfilings,
        'apptype': apptype,
        'duelist': appduedates,

    }

    return render(request, 'supportstaff/openmatter_details.html', context)


def new_attachment(request, pk):
    message = inboxmessage.objects.get(id=pk)
    if request.method == 'POST':
        form = InboxAttachmentEntryForm(request.POST, request.FILES)
        if form.is_valid():
            attach_rec = form.save(commit=False)
            attach_rec.message_id = pk
            attach_rec.save()
            return redirect('supportstaff-new_attachment', pk)
        else:
            return redirect('supportstaff-new_attachment', pk)
    else:
        form = form = InboxAttachmentEntryForm()

    context = {
        'form': form,
        'message': message,
    }

    return render(request, 'supportstaff/new_attachment.html', context)


def new_message(request):

    user_message_id = request.user.user_profile.id
    username = request.user.username
    a = date.today()
    messagedate = a.strftime('%m/%d/%Y')
    dateconvert = datetime.strptime(
        messagedate, "%m/%d/%Y").strftime('%Y-%m-%d')

    if request.method == "POST":
        form = InboxMessageNewForm(request.POST)
        if form.is_valid():
            inbox_rec = form.save(commit=False)
            inbox_rec.messagefrom = username
            inbox_rec.messagedate = dateconvert
            inbox_rec.status = "UNREAD"
            inbox_rec.save()
            id = inbox_rec.id
            return redirect('supportstaff-new_attachment', id)
        else:
            return redirect('supportstaff-new_message')
    else:
        form = InboxMessageNewForm()

    context = {
        'form': form,
        'messagefrom_id': user_message_id,
        'messagefrom': username,
        'messagedate': messagedate,
    }

    return render(request, 'supportstaff/new_message.html', context)


def open_message(request, pk):
    message = inboxmessage.objects.get(id=pk)
    attachments = messageattachment.objects.filter(message_id=pk)
    message.status = "READ"
    message.save()
    if request.method == 'POST':
        form = InboxMessageForm(request.POST, instance=message)
        return redirect('supportstaff-my_messages')
    else:
        form = InboxMessageForm(instance=message)

    context = {
        'form': form,
        'replyid': pk,
        'attachments': attachments,
    }

    return render(request, 'supportstaff/readmessage.html', context)


def open_sentitems(request, pk):
    message = inboxmessage.objects.get(id=pk)
    attachments = messageattachment.objects.filter(message_id=pk)
    if request.method == 'POST':
        form = InboxMessageForm(request.POST, instance=message)
        return redirect('supportstaff-my_messages')
    else:
        form = InboxMessageForm(instance=message)

    context = {
        'form': form,
        'replyid': pk,
        'attachments': attachments,
    }

    return render(request, 'supportstaff/readsentitems.html', context)


def view_attachment(request, pk):
    viewattachment = messageattachment.objects.get(id=pk)
    message = inboxmessage.objects.get(id=viewattachment.message_id)
    if request.method == 'POST':
        form = InboxAttachmentViewForm(
            request.POST, request.FILES, instance=viewattachment)
        if form.is_valid():
            attachment_rec = form.save(commit=False)
            attachment_rec.message_id = message.id
            attachment_rec.save()
        else:
            form = InboxAttachmentViewForm(instance=viewattachment)
    else:
        form = InboxAttachmentViewForm(instance=viewattachment)

    context = {
        'form': form,
        'message': message,
        'viewattachment' : viewattachment,
    }

    return render(request, 'supportstaff/viewattachment.html', context)


def read_sentitems(request, pk):
    message = inboxmessage.objects.get(id=pk)
    messageto = message.messagefrom
    userprofile = User_Profile.objects.get(access_code=messageto)
    messageto_id = userprofile.id
    messagefrom = message.messageto
    userid = request.user.user_profile.userid
    a = date.today()
    messagedate = a.strftime('%m/%d/%Y')
    dateconvert = datetime.strptime(
        messagedate, "%m/%d/%Y").strftime('%Y-%m-%d')
    matter = Matters.objects.all()
    if request.method == 'POST':
        form = InboxMessageEntryForm(request.POST)
        if form.is_valid():
            inbox_rec = form.save(commit=False)
            inbox_rec.messageto_id = messageto_id
            inbox_rec.messagefrom = messagefrom
            inbox_rec.messagedate = dateconvert
            inbox_rec.save()
            return redirect('supportstaff-home')
        else:
            form = InboxMessageEntryForm()
    else:
        form = InboxMessageEntryForm()

    context = {
        'form': form,
        'messagefrom': messagefrom,
        'messageto': messageto,
        'messagedate': messagedate,
        'matter': matter,
    }

    return render(request, 'supportstaff/newmessage.html', context)


@login_required
def reply_message(request, pk):
    message = inboxmessage.objects.get(id=pk)
    messageto = message.messagefrom
    userprofile = User_Profile.objects.get(access_code=messageto)
    messageto_id = userprofile.id
    messagefrom = message.messageto
    userid = request.user.user_profile.userid
    a = date.today()
    messagedate = a.strftime('%m/%d/%Y')
    dateconvert = datetime.strptime(
        messagedate, "%m/%d/%Y").strftime('%Y-%m-%d')
    matter = Matters.objects.all()
    if request.method == 'POST':
        form = InboxMessageEntryForm(request.POST)
        if form.is_valid():
            inbox_rec = form.save(commit=False)
            inbox_rec.messageto_id = messageto_id
            inbox_rec.messagefrom = messagefrom
            inbox_rec.messagedate = dateconvert
            inbox_rec.status = "READ"
            inbox_rec.save()
            return redirect('supportstaff-home')
        else:
            form = InboxMessageEntryForm()
    else:
        form = InboxMessageEntryForm()

    context = {
        'form': form,
        'messagefrom': messagefrom,
        'messageto': messageto,
        'messagedate': messagedate,
        'matter': matter,
    }

    return render(request, 'supportstaff/newmessage.html', context)


@login_required
def my_messages(request):
    myuserid = request.user.user_profile.userid
    access_code = request.user.user_profile.access_code

    if 'q' in request.GET:
        q = request.GET['q']
        #clients = Client_Data.objects.filter(client_name__icontains=q)
        multiple_q = Q(Q(messagefrom__icontains=q) | Q(subject__icontains=q) | Q(
            messagebox__icontains=q) | Q(status__icontains=q) | Q(see_matter__matter_title__icontains=q))
        receivedmessages = inboxmessage.objects.filter(
            multiple_q, messageto__userid=myuserid).order_by('-messagedate')
        sentmessages = inboxmessage.objects.filter(
            multiple_q, messagefrom=myuserid).order_by('-messagedate')

    else:
        receivedmessages = inboxmessage.objects.filter(
            messageto__userid=myuserid).order_by('-messagedate')
        sentmessages = inboxmessage.objects.filter(
            messagefrom=myuserid).order_by('-messagedate')

    # receivedmessages = inboxmessage.objects.filter(messageto__userid=myuserid)
    # sentmessages = inboxmessage.objects.filter(messagefrom=access_code)
    user_message_id = request.user.user_profile.id
    alertmessages = inboxmessage.objects.filter(
        messageto_id=user_message_id, status="UNREAD")
    countalert = alertmessages.count()
    username = request.user.username    

    context = {
        'myuserid': myuserid,
        'access_code': access_code,
        'receivedmessages': receivedmessages,
        'sentmessages': sentmessages,
        'alertmessages': alertmessages,
        'noofalerts': countalert,
        'username': username,

    }

    return render(request, 'supportstaff/mymessages.html', context)


@login_required
def mails_inward(request):
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

    multiple_q1 = Q(Q(matter__handling_lawyer__access_code=code1) | Q(matter__handling_lawyer__access_code=code2) | Q(matter__handling_lawyer__access_code=code3) | Q(
        matter__handling_lawyer__access_code=code4) | Q(matter__handling_lawyer__access_code=code5) | Q(matter__handling_lawyer__access_code=code6) | Q(matter__handling_lawyer__access_code=code7))

    if 'q' in request.GET:
        q = request.GET['q']
        #clients = Client_Data.objects.filter(client_name__icontains=q)
        multiple_q2 = Q(Q(matter__folder__client__client_name__icontains=q) | Q(task__icontains=q) | Q(matter__matter_title__icontains=q) | Q(
            matter__handling_lawyer__access_code__icontains=q) | Q(matter__referenceno__icontains=q))

        docs = task_detail.objects.filter(
            multiple_q1, multiple_q2, doc_type='Incoming').order_by('-tran_date')

    else:
        docs = task_detail.objects.filter(
            multiple_q1, doc_type='Incoming').order_by('-tran_date')

    noofmatters = docs.count()
    paginator = Paginator(docs, 11)
    page = request.GET.get('page')
    all_matters = paginator.get_page(page)
    user_message_id = request.user.user_profile.id
    alertmessages = inboxmessage.objects.filter(
        messageto_id=user_message_id, status="UNREAD")
    countalert = alertmessages.count()
    username = request.user.username    

    context = {
        'page': page,
        'noofmatters': noofmatters,
        'matters': all_matters,
        'alertmessages': alertmessages,
        'noofalerts': countalert,
        'username': username,

    }
    return render(request, 'supportstaff/mailsin.html', context)


@login_required
def mails_inward_new(request):
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

    docs = task_detail.objects.filter(
        multiple_q, doc_type='Incoming').order_by('-tran_date')

    if request.method == 'POST':
        task_form = MailsInwardFormNew(request.POST)
        if task_form.is_valid():
            mailin_rec = task_form.save()
            mailin_rec.tran_type = 'Non-Billable'
            mailin_rec.doc_type = 'Incoming'
            mailin_rec.save()

            return redirect('supportstaff-mails_inward')
        else:
            task_form = MailsInwardFormNew()
    else:
        task_form = MailsInwardFormNew()

    page = Paginator(docs, 11)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    context = {
            'page': page,
            'form': task_form,
            'matters': docs,
        }

    
    # return render(request, 'supportstaff/newinward.html', context)
    return render(request, 'supportstaff/listofinwardmails.html', context)


@login_required
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
        task_form = MailsInwardFormUpdate(request.POST, instance=task)
        if task_form.is_valid():
            task_form.save()
            apptype = matter.apptype.apptype
#            if apptype == "Trademark":
            validateduedates()

            return redirect('supportstaff-mails_inward')
        else:
            task_form = MailsInwardFormUpdate(instance=task)
    else:
        task_form = MailsInwardFormUpdate(instance=task)

    context = {
        'form': task_form,
        'client': client,
        'pk': pk,
        'mails': task,
        'matter': matter,
        'duedates': duedates,
        'docs': docs,
    }
    return render(request, 'supportstaff/mailsinwardet.html', context)


def add_task(request, pk):
    def perform_billable_services():
        def save_to_tempPF():
            tempbills = TempBills.objects.filter(
                matter_id=matter_id, tran_date=tran_date, bill_service_id=bill_id)
            if tempbills:
                pass
            else:

                # if prate > 0:
                #     pesoamount = (PF_amount * prate)
                # else:
                #     prate = 0
                #     pesoamount = 0
                if bill_description is not None:
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

        def save_to_tempfiling():
            tempfees = TempFilingFees.objects.filter(
                matter_id=matter_id, tran_date=tran_date, filing=filing)
            if tempfees.exists():
                pass
            else:
                tempfees = TempFilingFees(
                    matter_id=matter_id,
                    tran_date=tran_date,
                    bill_service_id=filingfees.activitycode.id,
                    filing=filing,
                    lawyer_id=lawyer,
                    expense_detail=bill_description,
                    pesoamount=PF_amount,
                    expense_actual_amt=PF_amount,
                    # pesorate=prate,
                    currency=currency)
                tempfees.save()

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

            feeresult = FilingCodes.objects.filter(activitycode_id=task_code)
            for filingfees in feeresult:
                filing = filingfees.filing
                bill_description = filingfees.filing_description
                bill_id = filingfees.activitycode.id
                PF_amount = filingfees.amount
                prate = filingfees.pesorate
                currency = filingfees.currency
                save_to_tempfiling()

    matter = Matters.objects.get(id=pk)
    codes = ActivityCodes.objects.all()
    tasks = task_detail.objects.filter(matter__id=pk)
    username = request.user.username
    userid = request.user.user_profile.userid_id

    if request.method == "POST":
        # Get the posted form
        form = TaskEntryForm(request.POST)
        if form.is_valid():
            task_rec = form.save(commit=False)
            task_rec.matter_id = matter.id
            task_rec.task_code_id = request.POST['task_code']
            task_rec.updatedby = username
            task_rec.preparedby_id = userid
            task_rec.save()
            perform_billable_services()

            return redirect('supportstaff-matter_review', pk)
        else:
            return redirect('supportstaff-matter_review', pk)
    else:
        form = TaskEntryForm()

    context = {
        'form': form,
        'matter': matter,
        'm_id': pk,
        'codes': codes,
        'tasks': tasks,
    }
    return render(request, 'supportstaff/add_new_task.html', context)

def newmail(request):

    if request.method == 'POST':
        task_form = newmailform(request.POST)
        if task_form.is_valid():
            mailin_rec = task_form.save()
            mailin_rec.tran_type = 'Non-Billable'
            mailin_rec.doc_type = 'Incoming'
            mailin_rec.save()

            return redirect('supportstaff-mails_inward')
        else:
            task_form = newmailform()
    else:
        task_form = newmailform()
    
    context = {
        'form': task_form,
    }
    
    return render(request, 'supportstaff/newinward.html', context)
    

def add_mail(request, pk):
    matter = Matters.objects.get(id=pk)
    tasks = task_detail.objects.filter(matter__id = pk)
    codes = ActivityCodes.objects.filter(TranType = 'MAILSIN')
    username = request.user.username
    userid = request.user.user_profile.userid_id

    if request.method == 'POST':
        form = MailsIn_REG(request.POST)
        if form.is_valid():
            task_rec = form.save(commit=False)
            task_rec.matter_id = matter.id
            task_rec.task_code_id = request.POST['task_code']
            task_rec.doc_type = 'Incoming'
            task_rec.tran_type = 'Non-Billable'
            task_rec.createdby = username
            task_rec.updatedby = username
            task_rec.preparedby_id = userid
            task_rec.save()
            return redirect('supportstaff-matter_review', pk)
        else:
            return redirect('supportstaff-matter_review', pk)
    else:
        form = MailsIn_REG()
    
    context = {
        'form':form,
        'matter':matter,
        'tasks':tasks,
        'codes':codes,
        'm_id': pk,
    }
    return render(request, 'supportstaff/add_new_incoming.html', context)



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
    return render(request, 'supportstaff/add_new_duedate.html', context)


def add_activity(request):
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

    multiple_q = Q(Q(handling_lawyer__access_code=code1) | Q(handling_lawyer__access_code=code2) | Q(handling_lawyer__access_code=code3) | Q(handling_lawyer__access_code=code4) | Q(handling_lawyer__access_code=code5) | Q(handling_lawyer__access_code=code6) | Q(handling_lawyer__access_code=code7))

    #    print(multiple_q)

    matters = Matters.objects.filter(multiple_q).order_by("-filing_date") 

    multiple_q = Q(Q(matter__handling_lawyer__access_code=code1) | Q(matter__handling_lawyer__access_code=code2) | Q(matter__handling_lawyer__access_code=code3) | Q(
        matter__handling_lawyer__access_code=code4) | Q(matter__handling_lawyer__access_code=code5) | Q(matter__handling_lawyer__access_code=code6) | Q(matter__handling_lawyer__access_code=code7))

    docs = task_detail.objects.filter(
        multiple_q, doc_type='Incoming').order_by('-tran_date')

    if request.method == "POST":
        form = AddTaskEntryForm(request.POST)
        if form.is_valid():
            task_rec = form.save()
            task_rec.matter_id = request.POST["matter"]
            task_rec.doc_type = "Outgoing"
            task_rec.save()
            return redirect('superstaff-add_activity')
        else:
            form = AddTaskEntryForm()
    else:
        form = AddTaskEntryForm()

    context = {
        'form'  :form,
        'tasks':docs,
        'matters':matters,
    }

    return render(request, 'supportstaff/add_task.html', context)


def recentactivities(request, pk):
    task = task_detail.objects.get(id=pk)
    m_id = task.matter.id
    matter = Matters.objects.get(id=m_id)
    #activities = task_detail.objects.filter(matter__id=m_id)
    listofdocs = FilingDocs.objects.filter(Task_Detail__id=pk)
    print(listofdocs)
    duedates = AppDueDate.objects.filter(matter__id=m_id)
    unpaidbills = AccountsReceivable.objects.filter(matter__id=m_id)
    form = TaskEntryForm(instance=task)

    context = {
        'form': form,
        'matter': matter,
        'listofdocs': listofdocs,
        'duedates': duedates,
        'task': task,
        'm_id': m_id,
        'unpaidbills':unpaidbills,

    }
    return render(request, 'supportstaff/recenttaskview.html', context)

    # Financial Data
    # ARBills = AccountsReceivable.objects.filter(
    #     matter__id=matterid, payment_tag="UN").order_by('bill_date')
    # Total_bill_amount = AccountsReceivable.objects.filter(
    #     matter__id=matterid, payment_tag="UN").aggregate(Sum('bill_amount'))
    # Unpaid_amt = Total_bill_amount["bill_amount__sum"]
    # tmpbills = TempBills.objects.filter(
    #     matter_id=matterid).order_by('-tran_date')
    # tmpfees = TempFilingFees.objects.filter(
    #     matter_id=matterid).order_by('-tran_date')
    # tmpexp = TempExpenses.objects.filter(
    #     matter_id=matterid).order_by('-tran_date')


def recentviewduedates(request, pk):
    username = request.user.username
    duedate = AppDueDate.objects.get(id=pk)
    matterid = duedate.matter.id
    activity = task_detail.objects.filter(matter__id=matterid).order_by('-tran_date')
    activity_count = activity.count()
    matter = Matters.objects.get(id=matterid)
    if request.method == 'POST':
        form = DueDateEntryForm(request.POST, instance=duedate)
        if form.is_valid():
           duedate_rec = form.save(commit=False)
           duedate_rec.matter_id = matterid
           duedate_rec.createdby = username
           duedate_rec.save()
           return redirect('supportstaff-home')
        else:
            form = DueDateEntryForm(instance=duedate)
    else:
        form = DueDateEntryForm(instance=duedate)

    context = {
        'form': form,
        'matter': matter,
        'activity': activity,
        'activity_count': activity_count,
        'duedate': duedate
    }
    return render(request, 'supportstaff/recentduedateview.html', context)


def recentactivities_add_task(request, pk, m_id):
    matter = Matters.objects.get(id=m_id)
    matter_title = matter.matter_title
    foldertype = matter.folder.folder_type.id
    codes = ActivityCodes.objects.filter(foldertype_id=foldertype)
    duedate = AppDueDate.objects.get(id=pk)
    users = User_Profile.objects.all()
    lawyers = Lawyer_Data.objects.all()
    userid = request.user.user_profile.userid
    supporto = matter.handling_lawyer.access_code
    if request.method == "POST":
        form = TaskEntryForm(request.POST)
        if form.is_valid():
            print("pumasok valid")
            #            form.save()
            task_rec = form.save(commit=False)
            task_rec.matter_id = m_id
            task_rec.task_code_id = request.POST['task_code']
            task_rec.save()
            return redirect('superstaff-attach-document', pk, m_id)
        else:
            return redirect('superstaff-add_task', pk, m_id)
    else:
        form = TaskEntryForm()

    context = {
        'form': form,
        'matter': matter,
        'matter_title': matter_title,
        'd_id': pk,
        'codes': codes,
        'duedate': duedate,
        'users': users,
        'lawyers': lawyers,
        'userid': userid,
        'supporto': supporto,
    }
    return render(request, 'supportstaff/recent_add_task.html', context)


def recent_modify_task(request, pk, d_id):
    task = task_detail.objects.get(id=pk)
    m_id = task.matter.id
    matter = Matters.objects.get(id=m_id)
    docs = FilingDocs.objects.filter(Task_Detail__id=pk)
    duedates = AppDueDate.objects.filter(matter__id=m_id)

    if request.method == 'POST':
        task_form = TaskEditForm(request.POST, instance=task)
        if task_form.is_valid():
            task_form.save()
            return redirect('supportstaff-home')
        else:
            task_form = TaskEditForm(instance=task)
    else:
        task_form = TaskEditForm(instance=task)

    context = {
        'form': task_form,
        'pk': pk,
        'm_id': m_id,
        'd_id': d_id,
        'matter': matter,
        'docs': docs,
        'duedates': duedates,
        'task': task,
    }
    return render(request, 'supportstaff/recent_modify_task.html', context)


def newdocumentPDF(request, pk, m_id):
    matter = Matters.objects.get(id=m_id)
    task = task_detail.objects.get(id=pk)
    docs = FilingDocs.objects.filter(Task_Detail__id=pk)
    access_code = request.user.user_profile.userid
    if request.method == "POST":
        # Get the posted form

        form = FilingDocsEntry(request.POST, request.FILES)
        if form.is_valid():
            docs_rec = form.save(commit=False)
            docs_rec.Task_Detail_id = pk
            docs_rec.createdby = access_code
            docs_rec.save()
            return redirect('superstaff-recent_adddocument', pk, m_id)
        else:
            return redirect('superstaff-recent_adddocument', pk, m_id)
    else:
        form = FilingDocsEntry()

    context = {
        'form': form,
        'matter': matter,
        'task': task,
        'pk': pk,
        'm_id': m_id,
        't_id': pk,
        'docs': docs,
    }
    return render(request, 'supportstaff/add_new_docs.html', context)


def attach_document(request, pk, m_id):
    duedate = AppDueDate.objects.get(id=pk)
    matter = Matters.objects.get(id=m_id)
    if request.method == "POST":
        # Get the posted form
        form = FilingDocsEntry(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            duedate.date_complied = request.POST["DocDate"]
            duedate.save()
            return redirect('attach-document', pk, m_id)
        else:
            return redirect('recent-add_task', pk, m_id)
    else:
        form = FilingDocsEntry()

    context = {
        'form': form,
        'matter': matter,
        'd_id': pk,
        'duedate': duedate,
    }
    return render(request, 'supportstaff/attachdocument.html', context)


def list_messages(request):
    user_message_id = request.user.user_profile.id
    alertmessages = inboxmessage.objects.filter(
        messageto_id=user_message_id, status="UNREAD")

    context = {
        'alertmessages': alertmessages,
    }
    return render(request, 'supportstaff/list_inboxmessages.html', context)


def edit_alertmessage(request, pk):
    message = inboxmessage.objects.get(id=pk)
    message.status = "READ"
    message.save()
    messagefrom = message.messagefrom
    messageto = message.messageto
    a = message.messagedate
    messagedate = a.strftime('%m/%d/%Y')
    subject = message.subject
    messagebox = message.messagebox
    see_matter = message.see_matter

    attachments = messageattachment.objects.filter(message_id=pk)

    context = {
        'messagefrom': messagefrom,
        'messageto': messageto,
        'messagedate': messagedate,
        'subject': subject,
        'messagebox': messagebox,
        'see_matter': see_matter,
        'attachments': attachments,


    }
    return render(request, 'supportstaff/edit_msg.html', context)


def remove_alertmessage(request, pk):
    selected = inboxmessage.objects.get(id=pk)
    selected.delete()
    return redirect('superstaff-list_messages')

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
                print("pumasok d2 sa form valid")
                ipdetail_rec = form.save(commit=False)
                ipdetail_rec.matter_id = pk
                ipdetail_rec.save()
                ip_matters = IP_Matters.objects.get(matter__id=pk)
                apptype = matter.apptype.apptype
                validateduedates()

                return redirect('supportstaff-matter_review', pk)
            else:
                if sw == 0:
                    form = IPDetailForm()
                else:
                    form = IPDetailForm(instance=ip_matters)
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
            'sk':sk,

        }
        return render(request, 'supportstaff/ipdetailform.html', context)

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
                print("pumasok d2 sa form valid")
                nonipdetail_rec = form.save(commit=False)
                nonipdetail_rec.matter_id = pk
                nonipdetail_rec.save()
                return redirect('supportstaff-matter_review', pk)
            else:
                if sw == 0:
                    form = Non_IPDetailForm()
                else:
                    form = Non_IPDetailForm(instance=casematter)

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
        return render(request, 'supportstaff/nonipdetailform.html', context)

def matter_classofgoods(request, pk):
    matter = Matters.objects.get(id=pk)
    sk = matter.apptype.apptype
    print(sk)
    listofgoods = ClassOfGoods.objects.filter(matter__id=pk)
    if sk == "Trademark":
        if request.method == 'POST':
            form = ClassOfGoodsEntry(request.POST)
            if form.is_valid():
                classofgoods_rec = form.save(commit=False)
                classofgoods_rec.matter_id = pk
                classofgoods_rec.save()
                return redirect('supportstaff-matter-classofgoods', pk)
            else:
                form = ClassOfGoodsEntry()        
        else:
            form = ClassOfGoodsEntry()

        context = {
            'form': form,
            'm_id': pk,
            'matter': matter,
            'listofgoods': listofgoods,
        }
        return render(request, 'supportstaff/classofgoods.html', context)
    else:
        return redirect('supportstaff-matter-otherdetails', pk, 'IPO')



def add_applicant(request, pk):
    matter = Matters.objects.get(id=pk)
    try:
        applicant = Applicant.objects.get(matter__id=pk)
        sw = 1
    except ObjectDoesNotExist:
        sw = 0 
    

    if request.method =='POST':
        if sw == 1:
            form = ApplicantEntryForm(request.POST, instance=applicant)
        else:
            form = ApplicantEntryForm(request.POST)

        if form.is_valid():
            applicant_rec = form.save(commit=False)
            applicant_rec.matter_id = pk
            applicant_rec.save()
            return redirect('supportstaff-matter_review', pk)
        else:
            if sw == 1:
                form = ApplicantEntryForm(instance=applicant)
            else:
                form = ApplicantEntryForm()
    else:
        if sw == 1:
            form = ApplicantEntryForm(instance=applicant)
        else:
            form = ApplicantEntryForm()
    
    context = {
        'form' :form,
        'matter':matter
    }
    return render(request, 'supportstaff/new_applicant_IP.html', context)

def replymessage(request, pk):
    username = request.user.username
    prevmessage = inboxmessage.objects.get(id=pk)


    messageto = prevmessage.messagefrom
    subject = "REPLY: "+ prevmessage.subject
    see_matter = prevmessage.see_matter

    if request.method=='POST':
        form = ReplyToMessageForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=messageto)
            user_id = user.id
            messageto = User_Profile.objects.get(userid_id=user_id)
            message_rec = form.save(commit=False)
            message_rec.messageto_id = messageto.id
            message_rec.messagefrom = username
            message_rec.messagedate = today
            message_rec.subject = subject
            message_rec.see_matter = see_matter
            message_rec.status = "UNREAD"
            message_rec.save()
            message_id = message_rec.id
            return redirect('associate-message_withfile', message_id)
        else:
            form = ReplyToMessageForm()
    else:
        form = ReplyToMessageForm()
    
    context = {
        'form':form,
        'prevmessage':prevmessage,
        'messagedate':today,
        'see_matter':see_matter,
        'subject': subject,
    }
    
    return render(request, 'supportstaff/reply_msg.html', context)

def view_document(request, pk, m_id, t_id):
    fileddocs = FilingDocs.objects.get(id=pk)
    matter = Matters.objects.get(id=m_id)
    if request.method == 'POST':
        form = DocumentEditForm(request.POST, request.FILES, instance=fileddocs)
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

    return render(request, 'supportstaff/editdocument.html', context)

