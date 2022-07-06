from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import *
from adminapps.models import *
from django.core.paginator import Paginator
from datetime import date, datetime, timedelta
from django.db.models import Q, Sum, Count
from adminapps.forms import *
from userprofile.forms import *
from django.shortcuts import render, redirect
from userprofile.models import User_Profile

today = date.today()
curr_month = today.month % 12
curr_year = today.year

prev_year  = today.year
prev_month = today.month -1
if prev_month == 0:
    prev_month = 12
    prev_year  = today.year -1 



# Create your views here.

@login_required
def main(request):
    access_code = request.user.user_profile.userid
    username = request.user.username
#    alertmessages = Alert_Messages.objects.filter(messageto=access_code)
    user_message_id = request.user.user_profile.id
    alertmessages = inboxmessage.objects.filter(
        messageto_id=user_message_id, status="UNREAD")
    countalert = alertmessages.count()

    srank = request.user.user_profile.rank
    username = request.user.username

    # details
    activitydetails = task_detail.objects.filter(tran_date__year = today.year, tran_date__month = today.month).order_by('-tran_date')
    
    bill_amount = AccountsReceivable.objects.filter(bill_date__year = today.year, bill_date__month = today.month).exclude(payment_tag="CN").aggregate(Sum('bill_amount'))
    bill_amt = bill_amount["bill_amount__sum"]

    prev_bill_amount = AccountsReceivable.objects.filter(bill_date__year = prev_year, bill_date__month = prev_month).exclude(payment_tag="CN").aggregate(Sum('bill_amount'))
    prev_bill_amt = prev_bill_amount["bill_amount__sum"]

    peso_amount = AccountsReceivable.objects.filter(bill_date__year = today.year, bill_date__month = today.month).exclude(payment_tag="CN").aggregate(Sum('pesoamount'))
    peso_amt = peso_amount["pesoamount__sum"]

    prev_peso_amount = AccountsReceivable.objects.filter(bill_date__year =prev_year, bill_date__month = prev_month).exclude(payment_tag="CN").aggregate(Sum('pesoamount'))
    prev_peso_amt = prev_peso_amount["pesoamount__sum"]

    Unbill_amount = AccountsReceivable.objects.filter(payment_tag = 'UN').aggregate(Sum('bill_amount'))
    unbill_amt = Unbill_amount["bill_amount__sum"]

    


    matters = Matters.objects.filter(filing_date__year = today.year, filing_date__month = today.month)
    prevmatters = Matters.objects.filter(filing_date__year = today.year, filing_date__month = prev_month)
    clients = Client_Data.objects.filter(date_acquired__year = today.year, date_acquired__month = today.month)
    prevclient = Client_Data.objects.filter(date_acquired__year = today.year, date_acquired__month = prev_month)

    lawyer_summary = Matters.objects.values('handling_lawyer').annotate(case_count=Count('handling_lawyer')).filter(filing_date__year = today.year, filing_date__month = today.month)
    prev_lawyer_summary = Matters.objects.values('handling_lawyer').annotate(case_count=Count('handling_lawyer')).filter(filing_date__year = today.year, filing_date__month = prev_month)

    activities = task_detail.objects.all()
#    matters = Matters.objects.all()

    clientcount = clients.count()
    activitycount = activities.count()
    matterscount = matters.count()
    prevmonthmatters = prevmatters.count
    prevclientcount = prevclient.count
    lawyerInventory = LawyersCases.objects.all()
    queryset = AppType.objects.all()
    countalert = alertmessages.count()

#   empty table and insert summary count for client
    vs_client_countdata = Matters.objects.values('folder__client__client_name').annotate(NoOfMatter = Count('folder')).order_by('folder__client__client_name')
    ClientSummaryCount.objects.all().delete()
    for data in vs_client_countdata :
        clientname = data['folder__client__client_name']
        noofmatter = data['NoOfMatter']
        clientsum = ClientSummaryCount(client_name=clientname, no_of_matters=noofmatter)
        clientsum.save()
    clientsummary = ClientSummaryCount.objects.all()

#   empty table and insert summary count for lawyers
    vs_lawyer_countdata = Matters.objects.values('handling_lawyer__access_code').annotate(NoOfMatter = Count('handling_lawyer__access_code')).order_by('handling_lawyer__access_code')
    LawyerSummary.objects.all().delete()
    for data in vs_lawyer_countdata :
        lawyer = data['handling_lawyer__access_code']
        noofmatter = data['NoOfMatter']
        lawyersum = LawyerSummary(Lawyer=lawyer, no_of_matters=noofmatter)
        lawyersum.save()
    lawyersummary = LawyerSummary.objects.all()

#   empty table and insert summary count for the casetype
    vs_casetype_countdata = Matters.objects.values('case_type__case_type').annotate(NoOfMatter = Count('case_type__case_type'))
    CaseTypeSummary.objects.all().delete()
    for data in vs_casetype_countdata :
        casetype = data['case_type__case_type']
        noofmatter = data['NoOfMatter']
        casetypesum = CaseTypeSummary(casetype=casetype, no_of_matters=noofmatter)
        casetypesum.save()
    casetypesummary = CaseTypeSummary.objects.all()

    context = {
        'activitycount' : activitycount,
        'clientcount' : clientcount,
        'prevclientcount' : prevclientcount,
        'matterscount' : matterscount,
        'prevcount' : prevmonthmatters,
        'ARbills': bill_amt,
        'peso_amt': peso_amt,        
        'prev_ARbills' : prev_bill_amt,
        'prev_peso_amt':prev_peso_amt,
        'unbill_amount': unbill_amt,
        'queryset' : queryset,
        'inventory': lawyerInventory,
        'activitydetails' : activitydetails,
        'alertmessages': alertmessages,
        'noofalerts': countalert,
        'username': username,
        'data' : clientsummary, 
        'lawyersum': lawyersummary,
        'casetypesum':casetypesummary,
    }
    return render(request, 'managing_apps/index.html', context)

def view_new_clients(request):

    # filtering new clients for the month ######################
    clients = Client_Data.objects.filter(date_acquired__year = today.year, date_acquired__month = today.month).order_by('client_name')
    client_count = clients.count()

    # filtering new clients for the month ######################
    prevclients = Client_Data.objects.filter(date_acquired__year = prev_year, date_acquired__month = prev_month).order_by('-date_acquired')
    prevclient_counts = prevclients.count()

    client_summary_count = Matters.objects.values('folder__client__client_name').annotate(NoOfMatter = Count('folder__client')).filter(filing_date__year = today.year, filing_date__month = today.month).order_by('folder__client__client_name')

    print(client_summary_count)


    total_numberofmatters = client_summary_count.count()

    # for visual data


    context = {

        'clients' : clients,
        'clientcount' : client_count,
        'prevclients': prevclients,
        'prevclientcount': prevclient_counts,
        'clientsummary' : client_summary_count,
        'total_count_matters' : total_numberofmatters,
    }

    return render(request, 'managing_apps/view_newclients.html', context)

def view_new_matters(request):
    # filter matters filed current month #############
    matters = Matters.objects.filter(filing_date__year = today.year, filing_date__month = today.month ).order_by('-filing_date')
    # filter matters filed previous month
    prevmatters = Matters.objects.filter(filing_date__year = prev_year, filing_date__month = prev_month).order_by('-filing_date')

    matter_count = matters.count()
    prevmonthmatters = prevmatters.count()

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

    listpayments = Payments.objects.filter(bill_number__matter__id=pk).order_by("-payment_date")

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

def clientlist(request):
    access_code = request.user.user_profile.userid
    user_id = User.id

    user_message_id = request.user.user_profile.id
    alertmessages = inboxmessage.objects.filter(
        messageto_id=user_message_id, status="UNREAD")
    countalert = alertmessages.count()
    srank = request.user.user_profile.rank
    username = request.user.username

    if 'q' in request.GET:
        q = request.GET['q']
        #clients = Client_Data.objects.filter(client_name__icontains=q)
        multiple_q = Q(Q(client_name__icontains=q) | Q(main_contact__icontains=q) | Q(email__icontains=q) | Q(
            address__icontains=q) | Q(industry__industry__icontains=q) | Q(status__icontains=q) | Q(country__country__icontains=q))
        clients = Client_Data.objects.filter(
            multiple_q).order_by("client_name")
    else:
        clients = Client_Data.objects.all().order_by("client_name")

    noofclients = clients.count()
    paginator = Paginator(clients, 11)
    page = request.GET.get('page')
    all_clients = paginator.get_page(page)

    context = {
        'page': page,
        'noofclients': noofclients,
        'clients': all_clients,
        'alertmessages': alertmessages,
        'noofalerts': countalert,
        'username': username,
    }

    return render(request, 'managing_apps/clientlist.html', context)

def clientlistmatters(request, pk):
    access_code = request.user.user_profile.userid
    user_id = User.id

    user_message_id = request.user.user_profile.id
    alertmessages = inboxmessage.objects.filter(
    messageto_id = user_message_id, status="UNREAD")
    countalert = alertmessages.count()
    srank = request.user.user_profile.rank
    username = request.user.username

    matters = Matters.objects.filter(folder__client_id=pk).order_by('-filing_date')
    client = Client_Data.objects.get(id=pk)
    noofmatters = matters.count()

    context = {
        'matter': matters,
        'client': client,
        'noofmatters':noofmatters,
        'alertmessages': alertmessages,
        'noofalerts': countalert,
        'username': username,
    }
    return render(request, 'managing_apps/clientview.html', context)

def matter_update_client(request, pk):
    access_code = request.user.user_profile.userid
    user_id = User.id

    user_message_id = request.user.user_profile.id
    alertmessages = inboxmessage.objects.filter(
        messageto_id=user_message_id, status="UNREAD")
    countalert = alertmessages.count()
    srank = request.user.user_profile.rank
    username = request.user.username

    matter = Matters.objects.get(id=pk)
    task = task_detail.objects.filter(matter__id=pk)
    task_count = task.count()
    duedates = AppDueDate.objects.filter(matter__id=pk, date_complied__isnull=True)
    duedate_count = duedates.count()
    f_id = matter.folder.id
    c_id = matter.folder.client.id
    folder = CaseFolder.objects.get(id=f_id)
    client = Client_Data.objects.get(id=c_id)
    tempbills = TempBills.objects.filter(matter__id=pk)
    tempfilings = TempFilingFees.objects.filter(matter__id=pk)
    expenses = TempExpenses.objects.filter(matter__id=pk)
    docs = FilingDocs.objects.filter(Task_Detail__matter__id=pk)
    docs_count = docs.count()
    applicant = Applicant.objects.filter(matter__id=pk)




    context = {
        'matter': matter,
        'folder': folder,
        'client': client,
        'task': task,
        'duedatelist':duedates,
        'duedate_count': duedate_count,
        'tempbills': tempbills,
        'tempfilings': tempfilings,
        'listofexpenses': expenses,
        'docs': docs,
        'alertmessages': alertmessages,
        'noofalerts': countalert,
        'username': username,
        'task_count': task_count,
        'docs_count':docs_count,
        'applicant':applicant,
    }

    return render(request, 'managing_apps/matterview.html', context)

def matterlist(request):
    access_code = request.user.user_profile.userid
    user_id = User.id

    user_message_id = request.user.user_profile.id
    alertmessages = inboxmessage.objects.filter(
        messageto_id=user_message_id, status="UNREAD")
    countalert = alertmessages.count()
    srank = request.user.user_profile.rank
    username = request.user.username


    if 'q' in request.GET:
        q = request.GET['q']
        #matters = Matters.objects.filter(matter_title__icontains=q)
        #multiple_q = Q(Q(matter_title__icontains=q) | Q(folder__icontains=q))
        #matters = Matters.objects.filter(folder__client__client_name__icontains=q)
        multiple_q = Q(Q(matter_title__icontains=q) | Q(folder__client__client_name__icontains=q) | Q(
            referenceno__icontains=q) | Q(handling_lawyer__lawyer_name__icontains=q) | Q(folder__folder_description__icontains=q))
        matters = Matters.objects.filter(multiple_q)
    else:
        matters = Matters.objects.all().order_by("folder__client__client_name")

    noofmatters = matters.count()
    paginator = Paginator(matters, 11)
    page = request.GET.get('page')
    all_matters = paginator.get_page(page)

    context = {
        'page': page,
        'noofmatters': noofmatters,
        'matters': all_matters,
        'alertmessages': alertmessages,
        'noofalerts': countalert,
        'username': username,

    }
    return render(request, 'managing_apps/listmatters.html', context)

def lawyerlist(request):

    access_code = request.user.user_profile.userid 
    user_id = User.id

    user_message_id = request.user.user_profile.id
    alertmessages = inboxmessage.objects.filter(
        messageto_id=user_message_id, status="UNREAD")
    countalert = alertmessages.count()
    srank = request.user.user_profile.rank
    username = request.user.username

    # emplist = User_Profile.objects.filter(rank__startswith="ASS") | User_Profile.objects.filter(rank__startswith = "PART")

    emplist = Lawyer_Data.objects.all().order_by('access_code')
    empcount = emplist.count()

    context = {
        'emplist' : emplist,
        'alertmessages': alertmessages,
        'noofalerts': countalert,
        'username': username,
        'empcount':empcount,
    }
    return render(request, 'managing_apps/emplist.html', context)

def open_filingdocs(request, pk):
    document = FilingDocs.objects.get(id=pk)
    m_id = document.Task_Detail.matter.id
    matter = Matters.objects.get(id=m_id)
    c_id = matter.folder.client.id
    client = Client_Data.objects.get(id=c_id)
    if request.method == 'POST':
        form = FilingDocsEntry(request.POST, instance=document)
        if form.is_valid():
            form.save()
            return redirect('search_docs')
    else:
        form = FilingDocsEntry(instance=document)
    
    context = {
        'form': form,
        'client':client,
        'matter':matter,
    }
    return render(request, 'managing_apps/opendocument.html', context)

def unpaidbills(request):

    # unpaidbills = AccountsReceivable.objects.values('matter__folder__client__id', 'matter__folder__client__client_name').annotate(NoOfMatter=Count('bill_number')).order_by('-NoOfMatter')

    unpaidbills = AccountsReceivable.objects.values('matter__folder__client__id','matter__folder__client__client_name').annotate(NoOfMatter=Count('bill_number')).filter(payment_tag = 'UN').order_by('-NoOfMatter')
    bill_count = unpaidbills.aggregate(Sum('NoOfMatter'))
    billcount = bill_count["NoOfMatter__sum"]



    unpaid_bills = AccountsReceivable.objects.filter(payment_tag = 'UN').order_by('-bill_date')

    curr_total_bll_amount =unpaid_bills.aggregate(Sum('bill_amount'))
    curr_Tot_bill_amount = curr_total_bll_amount["bill_amount__sum"]

    curr_total_peso_amount =unpaid_bills.aggregate(Sum('pesoamount'))
    curr_Tot_peso_amount = curr_total_peso_amount["pesoamount__sum"]

    context = {
        'unpaidbills': unpaidbills,
        'billcount':billcount,
        'unpaid_bills':unpaid_bills,
        'curr_Tot_bill_amount': curr_Tot_bill_amount,
        'curr_Tot_peso_amount': curr_Tot_peso_amount,

    }
    return render(request, 'managing_apps/unpaidbills.html', context)

def unpaid_details(request, pk):
    client = Client_Data.objects.get(id=pk)
    bills = AccountsReceivable.objects.filter(matter__folder__client__id = pk, payment_tag = 'UN')

    context={
        'bills' : bills,
        'client': client,
    }

    return render(request, 'managing_apps/listbills.html', context)



def employee_detail(request, pk):
    access_code = request.user.user_profile.userid 
    lawyer = Lawyer_Data.objects.get(id=pk)
    userid = User_Profile.objects.get(id=pk)
    user = User.objects.get(id=userid.userid.id)
    form = UserEntryForm(instance=userid)
    u_form = UserUpdateForm(instance=user)
    access_code = lawyer.access_code
    print(access_code)

    # lawyer_summary = Matters.objects.values('case_type').annotate(case_count=Count('folder')).filter(filing_date__year = today.year, filing_date__month = today.month, handling_lawyer__access_code = access_code)
    
    lawyer_summary = Matters.objects.values('case_type__case_type').annotate(NoOfMatter=Count('folder')).filter(handling_lawyer__access_code = access_code)

    CaseTypeSummary.objects.all().delete()
    for data in lawyer_summary :
        casetype = data['case_type__case_type']
        noofmatter = data['NoOfMatter']
        casetypesum = CaseTypeSummary(casetype=casetype, no_of_matters=noofmatter)
        casetypesum.save()

    casetypesummary = CaseTypeSummary.objects.all()

    lawyer_summary = Matters.objects.values('case_type__case_type').annotate(NoOfMatter=Count('folder')).filter(handling_lawyer__access_code = access_code, filing_date__year = today.year, filing_date__month = today.month)

    CaseTypeSummary_Month.objects.all().delete()
    for data in lawyer_summary :
        casetype = data['case_type__case_type']
        noofmatter = data['NoOfMatter']
        casetypesum = CaseTypeSummary_Month(casetype=casetype, no_of_matters=noofmatter)
        casetypesum.save()

    casetypesummary1 = CaseTypeSummary_Month.objects.all()

    # prev_lawyer_summary = Matters.objects.values('handling_lawyer').annotate(case_count=Count('handling_lawyer')).filter(filing_date__year = today.year, filing_date__month = prev_month)



    context = {
        'form' : form,
        'u_form':u_form,
        'user': user,
        'lawyer':lawyer,
        'userprof':userid,
        'data': casetypesummary,
        'data1': casetypesummary1,
    }
    return render(request, 'managing_apps/empview.html', context)

def view_billings_details(request):

    current_bills = AccountsReceivable.objects.filter(bill_date__year = today.year, bill_date__month = today.month).exclude(payment_tag="CN")

    curr_total_bll_amount =current_bills.aggregate(Sum('bill_amount'))
    curr_Tot_bill_amount = curr_total_bll_amount["bill_amount__sum"]

    curr_total_peso_amount =current_bills.aggregate(Sum('pesoamount'))
    curr_Tot_peso_amount = curr_total_peso_amount["pesoamount__sum"]

    prev_bills = AccountsReceivable.objects.filter(bill_date__year = prev_year, bill_date__month = prev_month).exclude(payment_tag="CN")

    prev_total_bll_amount =prev_bills.aggregate(Sum('bill_amount'))
    prev_Tot_bill_amount = prev_total_bll_amount["bill_amount__sum"]

    prev_total_peso_amount =prev_bills.aggregate(Sum('pesoamount'))
    prev_Tot_peso_amount = prev_total_peso_amount["pesoamount__sum"]



    context = {
        'current_bills':current_bills,
        'prev_bills':prev_bills,
        'curr_Tot_bill_amount': curr_Tot_bill_amount,
        'curr_Tot_peso_amount': curr_Tot_peso_amount,

        'prev_Tot_bill_amount':prev_Tot_bill_amount,
        'prev_Tot_peso_amount': prev_Tot_peso_amount,
    }

    return render(request, 'managing_apps/view_billdetails.html', context)

def view_unpaidbills(request):
    unpaid_bills = AccountsReceivable.objects.filter(payment_tag = 'UN').order_by('-bill_date')

    curr_total_bll_amount =unpaid_bills.aggregate(Sum('bill_amount'))
    curr_Tot_bill_amount = curr_total_bll_amount["bill_amount__sum"]

    curr_total_peso_amount =unpaid_bills.aggregate(Sum('pesoamount'))
    curr_Tot_peso_amount = curr_total_peso_amount["pesoamount__sum"]


    context = {
        'unpaid_bills': unpaid_bills,
        'curr_Tot_bill_amount': curr_Tot_bill_amount,
        'curr_Tot_peso_amount': curr_Tot_peso_amount,

    }

    return render(request, 'managing_apps/view_unpaidbills.html', context)

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
    rcvd_msgcount = receivedmessages.count()
    sent_msgcount = sentmessages.count()
    context = {
        'myuserid': myuserid,
        'access_code': access_code,
        'receivedmessages': receivedmessages,
        'rcvd_msgcount':rcvd_msgcount,
        'sentmessages': sentmessages,
        'sent_msgcount':sent_msgcount,

    }

    return render(request, 'managing_apps/mymessages.html', context)

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
            return redirect('management-my_messages')
        else:
            return redirect('management-my_messages')
    else:
        form = InboxMessageNewForm()

    context = {
        'form': form,
        'messagefrom_id': user_message_id,
        'messagefrom': username,
        'messagedate': messagedate,
    }

    return render(request, 'managing_apps/new_message.html', context)
