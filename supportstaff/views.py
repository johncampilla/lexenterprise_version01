from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from adminapps.models import *
from datetime import date, datetime, timedelta
from django.core.paginator import Paginator
from dateutil.relativedelta import relativedelta
from adminapps.forms import EntryMatterForm, InboxMessageForm
from django.db.models import Q, Sum, Count

# Create your views here.
today = date.today()
curr_month = today.month % 12
prev_month = today.month - 1
if prev_month == 0:
    prev_month = 12


# #just for review
#            if basisofcompute == "In Months":
#                 nmonths = int(terms)
#                 svalue = ("+"+str(nmonths))
#                 sduedate = sdate + relativedelta(months=int(svalue))
#                 duedate = sduedate

#             if basisofcompute == "In Years":
#                 nyears = int(terms)
#                 svalue = ("+"+str(nyears))
#                 sduedate = sdate + relativedelta(years=int(svalue))
#                 duedate = sduedate

#             if basisofcompute == "In Days":
#                 ndays = int(terms)
#                 svalue = ("+"+str(ndays))
#                 sduedate = sdate + relativedelta(days=int(svalue))
#                 duedate = sduedate
# #


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

    context = {
        'alertmessages': alertmessages,
        'noofalerts': countalert,
        'username': username,
        'duedates': duedates,
        'messages': messages,
    }

    return render(request, 'supportstaff/index.html', context)


# """     matterlist = Matters.objects.filter(
#         Q(handling_lawyer__access_code=code1) | Q(handling_lawyer__access_code=code2) | Q(handling_lawyer__access_code=code3) | Q(handling_lawyer__access_code=code4) | Q(handling_lawyer__access_code=code5) | Q(handling_lawyer__access_code=code6) | Q(handling_lawyer__access_code=code7))
#  """

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


def reply_message(request, pk):
    message = inboxmessage.objects.get(id=pk)
    if request.method == 'POST':
        form = InboxMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supportstaff-home')
        else:
            form = InboxMessageForm()
    else:
        form = InboxMessageForm()

    context = {
        'form': form,
    }

    return render(request, 'supportstaff/newmessage.html', context)


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
