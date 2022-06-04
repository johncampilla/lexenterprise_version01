from asyncio.windows_events import NULL
from contextlib import nullcontext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from pandas import notnull
from adminapps.models import *
from datetime import date, datetime, timedelta
from django.core.paginator import Paginator
from dateutil.relativedelta import relativedelta
from adminapps.forms import InboxMessageEntryForm, TaskEditForm, EntryMatterForm, InboxMessageForm, TaskEntryForm, DueDateEntryForm, FilingDocsEntry
from django.db.models import Q, Sum, Count

# Create your views here.
today = date.today()
curr_month = today.month % 12
prev_month = today.month - 1
if prev_month == 0:
    prev_month = 12


@login_required
def main(request):
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
    alertmessages = Alert_Messages.objects.filter(messageto=access_code)
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


#    print(multiple_q)

    duedates = AppDueDate.objects.filter(
        multiple_q, duedate__gte=duedate1, duedate__lte=duedate2, date_complied__isnull=True).order_by('-duedate')

    messages = inboxmessage.objects.filter(
        messageto__userid=access_code, status='OPEN')

    recenttask = task_detail.objects.filter(
        multiple_q, tran_date__year=today.year, tran_date__month=today.month).order_by('-tran_date')

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
        'recenttask': recenttask,
        'recentdocs': recentdocs,
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

    context = {
        'page': page,
        'noofmatters': noofmatters,
        'matters': all_matters
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
    tempbills = TempBills.objects.filter(matter__id=pk)
    tempfilings = TempFilingFees.objects.filter(matter__id=pk)
    expenses = TempExpenses.objects.filter(
        Q(matter__id=pk), Q(status='O') | Q(status='P'))
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

    return render(request, 'supportstaff/openmatter_details.html', context)


def open_message(request, pk):
    message = inboxmessage.objects.get(id=pk)
    if request.method == 'POST':
        form = InboxMessageForm(request.POST, instance=message)
    else:
        form = InboxMessageForm(instance=message)

    context = {
        'form': form,
        'replyid': pk,
    }

    return render(request, 'supportstaff/readmessage.html', context)


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
    dateconvert = datetime.strptime(messagedate, "%m/%d/%Y").strftime('%Y-%m-%d')
    matter = Matters.objects.all()
    if request.method == 'POST':
        form = InboxMessageEntryForm(request.POST)
        if form.is_valid():
            print("pumasok", messageto_id)
            inbox_rec = form.save(commit=False)
            inbox_rec.messageto_id = messageto_id
            inbox_rec.messagefrom = messagefrom
            inbox_rec.messagedate = dateconvert
            inbox_rec.status = "OPEN"
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
            multiple_q, messagefrom=access_code).order_by('-messagedate')

    else:
        receivedmessages = inboxmessage.objects.filter(
            messageto__userid=myuserid).order_by('-messagedate')
        sentmessages = inboxmessage.objects.filter(
            messagefrom=access_code).order_by('-messagedate')

    # receivedmessages = inboxmessage.objects.filter(messageto__userid=myuserid)
    # sentmessages = inboxmessage.objects.filter(messagefrom=access_code)
    print(receivedmessages)
    print(sentmessages)

    context = {
        'myuserid': myuserid,
        'access_code': access_code,
        'receivedmessages': receivedmessages,
        'sentmessages': sentmessages,
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

    context = {
        'page': page,
        'noofmatters': noofmatters,
        'matters': all_matters,

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
        task_form = TaskEntryForm(request.POST)
        if task_form.is_valid():
            task_form.save()
            return redirect('supportstaff-mails_inward')
        else:
            task_form = TaskEntryForm()
    else:
        task_form = TaskEntryForm()

    context = {
        'form': task_form,
        'matters': docs,
    }
    return render(request, 'supportstaff/newinward.html', context)


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
        task_form = TaskEntryForm(request.POST, instance=task)
        if task_form.is_valid():
            task_form.save()
            apptype = matter.apptype.apptype
#            if apptype == "Trademark":
            validateduedates()

            return redirect('supportstaff-mails_inward')
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
    return render(request, 'supportstaff/mailsinwardet.html', context)


def add_task(request, pk):
    def perform_billable_services():
        def save_to_tempPF():
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

        def save_to_tempfiling():
            tempfees = TempFilingFees.objects.filter(
                matter_id=matter_id, tran_date=tran_date, filing=filing)
            if tempfees.exists():
                pass
            else:
                tempfees = TempFilingFees(
                    matter_id=matter_id,
                    tran_date=tran_date,
                    bill_id=filingfees.activitycode.id,
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
    codes = IPTaskCodes.objects.all()
    tasks = task_detail.objects.filter(matter__id=pk)
    if request.method == "POST":
        # Get the posted form
        form = TaskEntryForm(request.POST)
        if form.is_valid():
            form.save()
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
    matter = Matters.objects.all()
    if request.method == "POST":
        pass

    context = {
        'matter': matter,
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
        'm_id': m_id

    }
    return render(request, 'supportstaff/recenttaskview.html', context)


def recentviewduedates(request, pk):
    duedate = AppDueDate.objects.get(id=pk)
    matterid = duedate.matter.id
    activity = task_detail.objects.filter(
        matter__id=matterid).order_by('-tran_date')
    matter = Matters.objects.get(id=matterid)
    ARBills = AccountsReceivable.objects.filter(
        matter__id=matterid, payment_tag="UN").order_by('bill_date')
    Total_bill_amount = AccountsReceivable.objects.filter(
        matter__id=matterid, payment_tag="UN").aggregate(Sum('bill_amount'))
    Unpaid_amt = Total_bill_amount["bill_amount__sum"]
    tmpbills = TempBills.objects.filter(
        matter_id=matterid).order_by('-tran_date')
    tmpfees = TempFilingFees.objects.filter(
        matter_id=matterid).order_by('-tran_date')
    tmpexp = TempExpenses.objects.filter(
        matter_id=matterid).order_by('-tran_date')
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
        'tmpbills': tmpbills,
        'tmpfees': tmpfees,
        'tmpexp': tmpexp,

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
    print("pk=", pk)
    if request.method == "POST":
        # Get the posted form

        form = FilingDocsEntry(request.POST, request.FILES)
        if form.is_valid():
            docs_rec = form.save(commit=False)
            docs_rec.Task_Detail_id = pk
            docs_rec.save()
            return redirect('recent_adddocument', pk, m_id)
        else:
            return redirect('recent_adddocument', pk, m_id)
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
