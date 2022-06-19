from ctypes import c_double
from datetime import datetime
from html.entities import html5
from django.contrib.auth import get_user
from django.core import paginator
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.forms.widgets import ClearableFileInput
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from .models import Alert_Messages, CaseFolder, Client_Data, Matters, task_detail
from .forms import *
from userprofile.models import User_Profile
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404

today = date.today()
curr_month = today.month % 12
prev_month = today.month - 1
if prev_month == 0:
    prev_month = 12

global matter_key


@login_required
def main(request):

    ###### Determines the user portal to be displayed ########
    access_code = request.user.user_profile.userid
    user_id = User.id

    user_message_id = request.user.user_profile.id
    alertmessages = inboxmessage.objects.filter(
        messageto_id=user_message_id, status="UNREAD")
    countalert = alertmessages.count()
    srank = request.user.user_profile.rank
    username = request.user.username

    context = {
        'alertmessages': alertmessages,
        'noofalerts': countalert,
        'username': username,
    }

    if User.is_staff and User.is_superuser:
        if srank == 'MANAGING PARTNER' or srank == 'PARTNER':
            return redirect('management-home')
        elif srank == 'SYSTEM ADMIN':
            return render(request, 'adminapps/index.html', context)
        elif srank == 'ASSOCIATES':
            return redirect('associate-home')
        elif srank == 'SECRETARY' or srank == "PARALEGAL" or srank == 'SUPPORTSTAFF':
            return redirect('supportstaff-home')
        elif srank == 'CLIENT':
            return redirect('client-home')


def outputlist(request):

    #list = Client_Data.objects.all()
    #lists = CaseFolder.objects.all().values_list('folder_description').union(Matters.objects.all().values_list('matter_title'))
    #list = Matters.objects.filter(handling_lawyer=7).only('matter_title', )
    #list = Matters.objects.filter(handling_lawyer__lawyer_name__startswith='Atty. R')
    #list = Matters.objects.filter(Q(folder__client__client_name__startswith='Br') | Q (folder__client__client_name__startswith='P'))
    #list = Matters.objects.filter(Q(folder__client__client_name__startswith='Br') & Q (handling_lawyer__lawyer_name__startswith='Atty.'))
    list = User.objects.all().values()
    # print(list)
    print(list.query)
    # print(connection.queries)

    # print(alertmessages)
    # print(alertmessages.query)
    # print(connection.queries)
    profile = User_Profile.objects.get(userid=1)
    #profile = User_Profile.Rank

    sid = profile.rank

    context = {
        'list': list,
        'sid': sid,
    }

    return render(request, 'adminapps/output.html', context)


def taskentry(request, pk):

    matter = Matters.objects.get(id=pk)
    matter_key = pk

    if request.method == "POST":
        # Get the posted form
        form = TaskEntryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin-matter-viewtask', matter_key)
        else:
            return redirect('admin-new-task')
    else:
        form = TaskEntryForm()

    context = {
        'form': form,
        'matter': matter,
    }

    return render(request, 'adminapps/entry_task.html', context)


@login_required
def PaymentEntry(request):
    if request.method == "POST":
        form = PaymentEntryForm(request.POST, request.FILES)
        if form.is_valid():
            AR_profile = AccountsReceivable()
            AR_profile.matter = form.cleaned_data['matter']
            AR_profile.bill_number = form.cleaned_data['bill_number']
            AR_profile.bill_date = form.cleaned_data['bill_date']
            AR_profile.currency = form.cleaned_data['currency']
            AR_profile.bill_amount = form.cleaned_data['bill_amount']
            AR_profile.pf_amount = form.cleaned_data['pf_amount']
            AR_profile.ofees_amount = form.cleaned_data['ofees_amount']
            AR_profile.ope_amount = form.cleaned_data['ope_amount']
            AR_profile.payment_tag = form.cleaned_data['payment_tag']
            AR_profile.DocPDFs = form.cleaned_data['DocPDFs']
            AR_profile.prepared_by = form.cleaned_data['prepared_by']
            AR_profile.save()
            return redirect('admin-matter-viewtask', matter_key)
        else:
            return redirect('admin-new-billARentry')
    else:
        form = PaymentEntryForm()

    context = {
        'form': form,
    }

    return render(request, 'adminapps/entry_newARBill.html', context)


@login_required
def BillAREntry(request):
    if request.method == "POST":
        form = BillEntryForm(request.POST, request.FILES)
        if form.is_valid():
            AR_profile = AccountsReceivable()
            AR_profile.matter = form.cleaned_data['matter']
            AR_profile.bill_number = form.cleaned_data['bill_number']
            AR_profile.bill_date = form.cleaned_data['bill_date']
            AR_profile.currency = form.cleaned_data['currency']
            AR_profile.bill_amount = form.cleaned_data['bill_amount']
            AR_profile.pf_amount = form.cleaned_data['pf_amount']
            AR_profile.ofees_amount = form.cleaned_data['ofees_amount']
            AR_profile.ope_amount = form.cleaned_data['ope_amount']
            AR_profile.payment_tag = form.cleaned_data['payment_tag']
            AR_profile.DocPDFs = form.cleaned_data['DocPDFs']
            AR_profile.prepared_by = form.cleaned_data['prepared_by']
            AR_profile.save()
            return redirect('admin-new-billARentry')
        else:
            return redirect('admin-new-billARentry')
    else:
        form = BillEntryForm()

    context = {
        'form': form,
    }

    return render(request, 'adminapps/entry_newARBill.html', context)


@login_required
def DueDateEntry(request):
    if request.method == "POST":
        form = DueDateEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-new-billARentry')
        else:
            return redirect('admin-new-duedate')
    else:
        form = DueDateEntryForm()

    context = {
        'form': form,
    }

    return render(request, 'adminapps/entry_duedate.html', context)


@login_required
def add_user(request):
    userlist = User_Profile.objects.all()
    if request.method == 'POST':
        form = UserEntryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin-user-add')
        else:
            return redirect('admin-user-add')
    else:

        form = UserEntryForm()

    context = {
        'form': form,
        'userlist': userlist,
    }
    return render(request, 'adminapps/add_user.html', context)


@login_required
def add_lawyer(request):
    userlist = Lawyer_Data.objects.all()
    if request.method == 'POST':
        form = LawyerEntryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin-lawyer-add')
        else:
            return redirect('admin-lawyer-add')
    else:

        form = LawyerEntryForm()

    context = {
        'form': form,
        'userlist': userlist,
    }
    return render(request, 'adminapps/add_lawyer.html', context)


@login_required
def edit_lawyer(request, pk):
    selected = Lawyer_Data.objects.get(id=pk)
    userlist = Lawyer_Data.objects.all()
    if request.method == "POST":
        form = LawyerEntryForm(request.POST, request.FILES, instance=selected)
        if form.is_valid():
            form.save()
            return redirect('admin-lawyer-list')
        else:
            return redirect('admin-lawyer-list')
    else:
        form = LawyerEntryForm(instance=selected)
        context = {
            'form': form,
            'userlist': userlist,
        }
    return render(request, 'adminapps/edit_lawyer.html', context)


@login_required
def remove_lawyer(request, pk):
    selected = Lawyer_Data.objects.get(id=pk)
    selected.delete()
    return redirect('admin-lawyer-add')


@login_required
def cliententry(request):
    access_code = request.user.user_profile.userid
    user_id = User.id

    user_message_id = request.user.user_profile.id
    alertmessages = inboxmessage.objects.filter(
        messageto_id=user_message_id, status="UNREAD")
    countalert = alertmessages.count()
    srank = request.user.user_profile.rank
    username = request.user.username

    if request.method == "POST":
        # Get the posted form
        form = ClientEntryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Client has been successfully added!")
            return redirect('admin-client-list')
        else:
            return redirect('admin-new-client')

    form = ClientEntryForm()

    context = {
        'form': form,
        'alertmessages': alertmessages,
        'noofalerts': countalert,
        'username': username,

    }

    return render(request, 'adminapps/newentryclient_details.html', context)
    # return render(request, 'adminapps/add.html', context)


@login_required
def folderentry(request, pk):
    client = Client_Data.objects.get(id=pk)
    foldertype = FolderType.objects.all()
    supervisinglawyers = Lawyer_Data.objects.all()

    if request.method == 'POST':
        folder_description = request.POST.get('folder_description')
        folder_type = request.POST.get('folder_type')
        Supervisinglawyer = request.POST.get('Supervisinglawyer')
        print("pumasok dito", Supervisinglawyer)

        remarks = request.POST.get('remarks')
        folder_rec = CaseFolder(
            client_id=client.id,
            folder_description=folder_description,
            folder_type_id=folder_type,
            Supervisinglawyer_id=Supervisinglawyer,
            remarks=remarks)
        folder_rec.save()
        return redirect('admin-client-update', pk)
        redirect()

        # tran_date = request.POST.get('tran_date')
        # tran_type = request.POST.get('tran_type')
        # doc_type = request.POST.get('doc_type')
        # preparedby = request.POST.get('preparedby')
        # task_code = request.POST.get('task_code')
        # activity = request.POST.get('task_activity')
        # lawyer = request.POST.get('lawyer')
        # task_desc = request.POST.get('task_activity')
        # spentinmin = request.POST.get('spentinmin')
        # spentinhrs = request.POST.get('spentinhrs')
        # if spentinhrs is None:
        #     spentinhrs = NULL
        # if spentinmin is None:
        #     spentinmin = NULL

        # task_rec = task_detail(
        #     matter_id=m_id,
        #     tran_date=tran_date,
        #     tran_type=tran_type,
        #     doc_type=doc_type,
        #     preparedby_id=preparedby,
        #     lawyer_id=lawyer,
        #     task_code_id=task_code,
        #     task=task_desc,
        #     spentinhrs=spentinhrs,
        #     spentinmin=spentinmin
        # )
        # task_rec.save()

    context = {
        'client': client,
        'foldertype': foldertype,
        'supervisinglawyers': supervisinglawyers,
    }
    return render(request, 'adminapps/newentry_folder.html', context)


@login_required
def matterentry(request):
    #    breakpoint()
    if request.method == 'POST':
        form = EntryMatterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-matter-list')
        else:
            return redirect('admin-new-matter')
    else:
        form = EntryMatterForm()

    context = {
        'form': form,
    }
    return render(request, 'adminapps/newentrymatter.html', context)


@login_required
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

    return render(request, 'adminapps/clientlist.html', context)

@login_required
def folderlist(request):
    if 'q' in request.GET:
        q = request.GET['q']
        #clients = Client_Data.objects.filter(client_name__icontains=q)
        multiple_q = Q(Q(client__client_name__icontains=q) | Q(folder_description__icontains=q) | Q(
            folder_type__folder__icontains=q) | Q(Supervisinglawyer__access_code__icontains=q) | Q(remarks__icontains=q))
        folders = CaseFolder.objects.filter(multiple_q)
    else:
        folders = CaseFolder.objects.all()

    nooffolders = folders.count()
    paginator = Paginator(folders, 10)
    page = request.GET.get('page')
    all_folders = paginator.get_page(page)

    context = {
        'page': page,
        'nooffolders': nooffolders,
        'folders': all_folders,
    }

    return render(request, 'adminapps/admin_folderlist.html', context)

# @login_required
# def matterlist(request):
#     if 'q' in request.GET:
#         q = request.GET['q']
#         #matters = Matters.objects.filter(matter_title__icontains=q)
#         #multiple_q = Q(Q(matter_title__icontains=q) | Q(folder__icontains=q))
#         #matters = Matters.objects.filter(folder__client__client_name__icontains=q)
#         multiple_q = Q(Q(matter_title__icontains=q) | Q(folder__client__client_name__icontains=q) | Q(referenceno__icontains=q) | Q(folder__folder_description__icontains=q))
#         matters = Matters.objects.filter(multiple_q)
#     else:
#         matters = Matters.objects.all().order_by("folder__client__client_name")

#     noofmatters = matters.count()
#     page = Paginator(matters, 12)
#     page_list = request.GET.get('page')
#     page = page.get_page(page_list)


#     context = {
#         'page'    : page,
#         'noofmatters': noofmatters
#     }
# #    return render(request, 'adminapps/matterlist.html', context)
#     return render(request, 'adminapps/listmatters.html', context)

@login_required
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
    return render(request, 'adminapps/listmatters.html', context)


@login_required
def userlist(request):
    if 'q' in request.GET:
        q = request.GET['q']
        #clients = Client_Data.objects.filter(client_name__icontains=q)
        multiple_q = Q(Q(userid__username__icontains=q) | Q(
            userid__last_name__icontains=q) | Q(address__icontains=q) | Q(rank__icontains=q))
        users = User_Profile.objects.filter(
            multiple_q).order_by("userid__last_name")
    else:
        users = User_Profile.objects.all().order_by("userid__last_name")

    noofusers = users.count()
    context = {
        'users': users,
        'noofusers': noofusers
    }
    return render(request, 'adminapps/userlist.html', context)


@login_required
def lawyerlist(request):
    if 'q' in request.GET:
        q = request.GET['q']
        #clients = Client_Data.objects.filter(client_name__icontains=q)
        multiple_q = Q(Q(lawyer_name__icontains=q) | Q(access_code__icontains=q) | Q(
            Specialization__icontains=q) | Q(address__icontains=q) | Q(rank__icontains=q))
        users = Lawyer_Data.objects.filter(
            multiple_q).order_by("userid__last_name")
    else:
        users = Lawyer_Data.objects.all().order_by("lawyer_name")
#        users = Lawyer_Data.objects.all()

    noofusers = users.count()
    context = {
        'users': users,
        'noofusers': noofusers
    }
    return render(request, 'adminapps/lawyerlist.html', context)


@login_required
def client_information(request, pk):
    client = Client_Data.objects.get(id=pk)
    casefolders = CaseFolder.objects.filter(
        client__id=pk).order_by('folder_description')
    contacts = Contact_Person.objects.filter(
        client__id=pk).order_by('contact_person')
    arbills = AccountsReceivable.objects.filter(
        matter__folder__client__id=pk).order_by('-bill_date')
    duedates = AppDueDate.objects.filter(
        matter__folder__client__id=pk).order_by('-duedate')

    total_amount = AccountsReceivable.objects.filter(
        matter__folder__client__id=pk).aggregate(Sum('bill_amount'))

    bill_amt = total_amount["bill_amount__sum"]

    nooffolders = casefolders.count()
    page = Paginator(casefolders, 12)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    context = {
        'client': client,
        'casefolders': casefolders,
        'contacts': contacts,
        'arbills': arbills,
        'total_amount': bill_amt,
        'no_of_folders': nooffolders,
        'duedates': duedates,
        'page': page
    }
    return render(request, 'adminapps/clientinfo.html', context)


@login_required
def client_modify(request, pk):
    client = Client_Data.objects.get(id=pk)
    listofmatters = Matters.objects.filter(folder__client__id=pk)
    listoffolders = CaseFolder.objects.filter(client__id=pk)
    sid = pk
    if request.method == 'POST':
        form = ClientEntryForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('admin-client-update', pk)
        else:
            form = ClientEntryForm(instance=client)
    else:
        form = ClientEntryForm(instance=client)

    context = {
        'form': form,
        'sid': sid,
        'matters': listofmatters,
        'folders': listoffolders,

    }
    return render(request, 'adminapps/admin_clientupdate.html', context)

def clientlistmatters(request, pk):
    matters = Matters.objects.filter(folder__client_id=pk)
    client = Client_Data.objects.get(id=pk)
    noofmatters = matters.count()

    context = {
        'matter': matters,
        'client': client,
        'noofmatters':noofmatters,
    }
    return render(request, 'adminapps/admin_clientmatterlist.html', context)




@login_required
def client_update(request, pk):
    client = Client_Data.objects.get(id=pk)
    sid = pk
    if request.method == 'POST':
        form = ClientModifyForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('admin-client-list')
        else:
            form = ClientModifyForm(instance=client)
    else:
        form = ClientModifyForm(instance=client)

    context = {
        'form': form,
        'sid': sid,
    }
    return render(request, 'adminapps/clientupdate.html', context)
# def IPmatter_edit_details(request, pk):
#     matterinfo = IP_Matters.objects.get(id=pk)
#     if request.method == 'POST':
#         form = IPDetailForm(request.POST, instance=matterinfo)
#         if form.is_valid():
#             form.save()
#             #return redirect('admin-matter-viewtask', matter_key)
#         else:
#             form = IPDetailForm(instance=matterinfo)
#     else:
#         form = IPDetailForm(instance=matterinfo)

#     context = {
# #        'matter':matter,
#         'form':form,
#  #       'ip_matter' : ip_matter
#     }
#     return render(request, 'adminapps/newentrymatter_details.html', context)


@login_required
def matter_update(request, pk):
    matter = Matters.objects.get(id=pk)
    tasks = task_detail.objects.filter(matter__id=pk).order_by('-tran_date')
    try:
        matter_otherinfo = IP_Matters.objects.get(matter__id=pk)
    except IP_Matters.DoesNotExist:
        matter_otherinfo = None

    matter_key = pk
    if request.method == 'POST':
        form = EntryMatterForm(request.POST, instance=matter)
        if form.is_valid():
            form.save()
            return redirect('admin-matter-viewtask', matter_key)
        else:
            form = EntryMatterForm(instance=matter)
    else:
        form = EntryMatterForm(instance=matter)

    if matter_otherinfo == None:
        context = {
            'matter': matter,
            'matter_otherinfo': matter_otherinfo,
            'tasks': tasks,
            'form': form,
        }

#        return render(request, 'adminapps/matterupdatenone.html', context)
        return render(request, 'adminapps/newentrymatter_details.html', context)

    else:
        context = {
            'matter': matter,
            'matter_otherinfo': matter_otherinfo,
            'form': form,
        }

        return render(request, 'adminapps/matterupdate.html', context)


@login_required
def matter_update_client(request, pk):
    matter = Matters.objects.get(id=pk)
    task = task_detail.objects.filter(id=pk)
    f_id = matter.folder.id
    c_id = matter.folder.client.id
    folder = CaseFolder.objects.get(id=f_id)
    client = Client_Data.objects.get(id=c_id)
    if request.method == 'POST':
        form = EntryMatterForm(request.POST, instance=matter)
        if form.is_valid():
            form.save()
#            return redirect('admin-matter-viewtask', matter_key)
            return redirect('admin-client-update', folder.client.id)
        else:
            form = EntryMatterForm(instance=matter)
    else:
        form = EntryMatterForm(instance=matter)

    context = {
        'form': form,
        'matter': matter,
        'folder': folder,
        'client': client,
        'task': task,
    }
    return render(request, 'adminapps/matter_update_inclient.html', context)


def matter_update_folder(request, pk):
    matter = Matters.objects.get(id=pk)
    f_id = matter.folder.id
    folder = CaseFolder.objects.get(id=f_id)
    if request.method == 'POST':
        form = EntryMatterForm(request.POST, instance=matter)
        if form.is_valid():
            form.save()
#            return redirect('admin-matter-viewtask', matter_key)
            return redirect('admin-client-update', folder.client.id)
        else:
            form = EntryMatterForm(instance=matter)
    else:
        form = EntryMatterForm(instance=matter)

    context = {
        'form': form,
        'matter': matter,
        'folder': folder,
    }
    return render(request, 'adminapps/matter_update_infolder.html', context)


@login_required
def matter_add_details(request, pk, fd):
    client = Client_Data.objects.get(id=pk)
    folder = CaseFolder.objects.get(id=fd)
    if request.method == "POST":
        form = EntryMatterForm(request.POST)
        if form.is_valid():
            print("pumasok na sa save")
            matter_rec = form.save()
            matter_rec.folder_id = folder.id
            matter_rec.save()
            # messages.success(request, "Matter added successfully")
            return redirect('admin-client-update', pk)
        else:
            form = EntryMatterForm()
    else:
        form = EntryMatterForm()

    context = {
        'form': form,
        'client': client,
        'folder': folder,
        }
    return render(request, 'adminapps/newentrymatter_details.html', context)


# def matter_add_details(request):
#     showindustry = NatureOfBusiness.objects.all()
#     showfolders = CaseFolder.objects.all()
#     showcourts = Courts.objects.all()
#     showcasetype = CaseType.objects.all()
#     showapptype = AppType.objects.all()
#     shownature = NatureOfCase.objects.all()
#     showappearance = Appearance.objects.all()
#     showlawyer = Lawyer_Data.objects.all()
#     showcontacts = Contact_Person.objects.all()
#     context = {
#         'showindustry':showindustry,
#         'showfolders': showfolders,
#         'showcourts': showcourts,
#         'showcasetype':showcasetype,
#         'showapptype':showapptype,
#         'shownature': shownature,
#         'showappearance':showappearance,
#         'showlawyer':showlawyer,
#         'showcontacts':showcontacts
#     }

#     if request.method == 'POST':
#         casefolder = CaseFolder()
#         court = Courts()
#         casetype=CaseType()
#         app_type=AppType()
#         nature=NatureOfCase()
#         appearance=Appearance()
#         lawyer = Lawyer_Data()
#         matter = Matters()
#         matter.folder = request.POST.get('casefolder.folder')
#         matter.referenceno = request.POST.get('referenceno')
#         matter.clientrefno = request.POST.get('clientrefno')
#         matter.filing_date = request.POST.get('filing_date')
#         matter.filed_at = request.POST.get('court.filed_at')
#         matter.case_type = request.POST.get('casetype.case_type')
#         matter.apptype = request.POST.get('app_type.apptype')
#         matter.nature = request.POST.get('nature.nature')
#         matter.matter_title = request.POST.get('matter_title')
#         matter.appearance = request.POST.get('appearance.appearance')
#         matter.handling_lawyer = request.POST.get('lawyer.handling_lawyer')
#         matter.save()
#         messages.success(request, "Matter added successfully")

#     else:

#         return render(request, 'adminapps/newentrymatter_details2.html', context)

@login_required
def folder_update(request, pk):
    folder = CaseFolder.objects.get(id=pk)
    matter = Matters.objects.filter(folder_id=pk)
    c_id = folder.client_id
    client = Client_Data.objects.get(id=c_id)
    sid = pk
    if request.method == 'POST':
        form = EntryFolderForm(request.POST, instance=folder)
        if form.is_valid():
            form.save()
            return redirect('admin-folder-list')
        else:
            form = EntryFolderForm(instance=folder)
    else:
        form = EntryFolderForm(instance=folder)

    context = {
        'form': form,
        'client': client,
        'matter': matter,
    }
    return render(request, 'adminapps/admin_folderupdate.html', context)


@login_required
def folder_update_Client(request, pk):
    folder = CaseFolder.objects.get(id=pk)
    cid = folder.client_id
    client = Client_Data.objects.get(id=cid)
    matters = Matters.objects.filter(folder_id=pk)
    fid = folder.id
    print(client)
    if request.method == 'POST':
        form = EntryFolderForm(request.POST, instance=folder)
        if form.is_valid():
            form.save()
#            return redirect('admin-client-update', cid)
            return redirect('admin-client-folder-update', fid)
        else:
            form = EntryFolderForm(instance=folder)
    else:
        form = EntryFolderForm(instance=folder)

    context = {
        'form': form,
        'client': client,
        'folder': folder,
        'matter': matters,
    }
    return render(request, 'adminapps/admin_editfolder.html', context)


@login_required
def folder_information(request, pk):

    folders = CaseFolder.objects.get(id=pk)
    matters = Matters.objects.filter(folder=pk).order_by('apptype')
    #matters = folders.matters_set.all()
    duedates = AppDueDate.objects.filter(matter__folder_id=pk)
    context = {
        'folders': folders,
        'matters': matters,
        'duedates': duedates,
    }
    return render(request, 'adminapps/folderinfo.html', context)


def modifytask(request, pk, m_id):
    task = task_detail.objects.get(id=pk)
    matter = Matters.objects.get(id=m_id)
    #accounts = BankAcount.objects.filter(user=request.user)
    #form = PaymentForm()
    #form.fields['accounts'].queryset = accounts
    if request.method == 'POST':
        task_form = TaskEntryForm(request.POST, request.FILES, instance=task)
        if task_form.is_valid():
            task_form.save()
            return redirect('admin-matter-viewtask', m_id)
        else:
            task_form = TaskEntryForm(instance=task)
    else:
        task_form = TaskEntryForm(instance=task)

    context = {
        'form': task_form,
        'matter': matter,
    }
    return render(request, 'adminapps/modify_task.html', context)


def update_uploaded_docs(request, pk):
    task = task_detail.objects.get(id=pk)
    documents = FilingDocs.objects.filter(Task_Detail__id=pk)
    #documents = FilingDocs.objects.filter(Task_Detail__id=pk)
    context = {
        'task': task,
        'docs': documents,
    }

    return render(request, 'adminapps/documentlist.html', context)

    pass


def matter_viewtask(request, pk):
    matter_key = pk
    matter = Matters.objects.get(id=pk)
    try:
        matter_otherinfo = IP_Matters.objects.get(matter_id=pk)
    except IP_Matters.DoesNotExist:
        matter_otherinfo = None

    # matter_otherinfo = IP_Matters.objects.filter(matter_id=pk)
    # if matter_otherinfo.exists():
    #     print("table contains records")
    # else:
    #     print("no record found")
    #     matter_otherinfo = ""

    stype = matter.apptype
    # to display the lists
    activities = task_detail.objects.filter(
        matter_id=pk).order_by("-tran_date")
    listduedates = AppDueDate.objects.filter(matter_id=pk).order_by("-duedate")
    listbillings = AccountsReceivable.objects.filter(
        matter_id=pk).order_by("-bill_date")
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

    listpayments = Payments.objects.filter(
        matter_id=pk).order_by("-payment_date")

    context = {
        'matter': matter,
        'matter_otherinfo': matter_otherinfo,
        'activities': activities,
        'matter_key': matter_key,
        'duedate': listduedates,
        'bills': listbillings,
        'payments': listpayments,
        'Tbill_amt': Tbill_amt,
        'Tpf_amt': Tpf_amt,
        'Tofees_amt': Tofees_amt,
        'Tope_amt': Tope_amt,
        'Classes': listofclasses,
        'apptype': stype,

    }
    return render(request, 'adminapps/matterinfo.html', context)


@login_required
def get_otherinfo(request):
    pass


@login_required
def natureofcase(request):
    nature = NatureOfCase.objects.all()
    if request.method == "POST":
        form = NatureOfCaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nature-code')
        else:
            return redirect('nature-code')
    else:
        form = NatureOfCaseForm()
        context = {
            'form': form,
            'nature': nature,
        }
    return render(request, 'adminapps/entry_nature.html', context)


@login_required
def editnatureofcase(request, pk):
    selected = NatureOfCase.objects.get(id=pk)
    nature = NatureOfCase.objects.all()
    if request.method == "POST":
        form = NatureOfCaseForm(request.POST, instance=selected)
        if form.is_valid():
            form.save()
            return redirect('nature-code')
        else:
            return redirect('nature-code')
    else:
        form = NatureOfCaseForm(instance=selected)
        context = {
            'form': form,
            'nature': nature,
        }
    return render(request, 'adminapps/entry_nature.html', context)


@login_required
def removenatureofcase(request, pk):
    selected = NatureOfCase.objects.get(id=pk)
    nature = NatureOfCase.objects.all()
    selected.delete()
    return redirect('nature-code')


@login_required
def client_delete(request, pk):
    selected = Client_Data.objects.get(id=pk)
    selected.delete()
    return redirect('admin-client-list')


@login_required
def folder_delete(request, pk):
    selected = CaseFolder.objects.get(id=pk)
    c_id = selected.client_id
    selected.delete()
    return redirect('admin-client-update', c_id)


def matter_delete(request, pk):
    selected = Matters.objects.get(id=pk)
    c_id = selected.folder.client_id
    selected.delete()
    return redirect('admin-client-update', c_id)


@login_required
def casetypeentry(request):
    casetype = CaseType.objects.all()
    if request.method == "POST":
        form = CaseTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('casetype-code')
        else:
            return redirect('casetype-code')
    else:
        form = CaseTypeForm()
        context = {
            'form': form,
            'casetype': casetype,
        }
    return render(request, 'adminapps/entry_casetype.html', context)


@login_required
def editcasetype(request, pk):
    selected = CaseType.objects.get(id=pk)
    casetype = CaseType.objects.all()
    if request.method == "POST":
        form = CaseTypeForm(request.POST, instance=selected)
        if form.is_valid():
            form.save()
            return redirect('casetype-code')
        else:
            return redirect('casetype-code')
    else:
        form = CaseTypeForm(instance=selected)
        context = {
            'form': form,
            'casetype': casetype,
        }
    return render(request, 'adminapps/entry_casetype.html', context)


@login_required
def removecasetype(request, pk):
    selected = CaseType.objects.get(id=pk)
    casetype = CaseType.objects.all()
    selected.delete()
    return redirect('casetype-code')
    #form = CaseTypeForm()
    context = {
        'form': form,
        'casetype': casetype,
    }
    return render(request, 'adminapps/entry_casetype.html', context)


@login_required
def duecodeentry(request):
    duecodes = DueCode.objects.all()
    if request.method == "POST":
        form = DueCodeEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('due-code')
        else:
            return redirect('due-code')
    else:
        form = DueCodeEntryForm()

        context = {
            'form': form,
            'duecodes': duecodes,
        }
    return render(request, 'adminapps/entry_duecode.html', context)


@login_required
def foldertypeentry(request):
    folder = FolderType.objects.all()
    if request.method == "POST":
        form = FolderTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('folder-code')
        else:
            return redirect('folder-code')
    else:
        form = FolderTypeForm()

        context = {
            'form': form,
            'folder': folder,
        }
    return render(request, 'adminapps/entry_foldertype.html', context)


@login_required
def editduecode(request, pk):
    selected = DueCode.objects.get(id=pk)
    duecodes = DueCode.objects.all()
    if request.method == "POST":
        form = DueCodeEntryForm(request.POST, instance=selected)
        if form.is_valid():
            form.save()
            return redirect('due-code')
        else:
            return redirect('due-code')
    else:
        form = DueCodeEntryForm(instance=selected)
        context = {
            'form': form,
            'duecodes': duecodes,
        }
    return render(request, 'adminapps/entry_duecode.html', context)


@login_required
def editfoldertype(request, pk):
    selected = FolderType.objects.get(id=pk)
    folder = FolderType.objects.all()
    if request.method == "POST":
        form = FolderTypeForm(request.POST, instance=selected)
        if form.is_valid():
            form.save()
            return redirect('folder-code')
        else:
            return redirect('folder-code')
    else:
        form = FolderTypeForm(instance=selected)
        context = {
            'form': form,
            'folder': folder,
        }
    return render(request, 'adminapps/entry_foldertype.html', context)


@login_required
def removefoldertype(request, pk):
    selected = FolderType.objects.get(id=pk)
    folder = FolderType.objects.all()
    selected.delete()
    return redirect('folder-code')


@login_required
def entityentry(request):
    entity = Courts.objects.all()
    if request.method == "POST":
        form = EntityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('entity-code')
        else:
            return redirect('entity-code')
    else:
        form = EntityForm()

    context = {
        'form': form,
        'entity': entity,
    }

    return render(request, 'adminapps/entry_entity.html', context)


@login_required
def editentity(request, pk):
    entity = Courts.objects.all().order_by('court')
    selected = Courts.objects.get(id=pk)
    if request.method == "POST":
        form = EntityForm(request.POST, instance=selected)
        if form.is_valid():
            form.save()
            return redirect('entity-code')
        else:
            return redirect('entity-code')
    else:
        form = EntityForm(instance=selected)
        context = {
            'form': form,
            'entity': entity,
        }
    return render(request, 'adminapps/entry_entity.html', context)


@login_required
def removeentity(request, pk):
    selected = Courts.objects.get(id=pk)
    entity = Courts.objects.all()
    selected.delete()
    return redirect('entity-code')


def entry_activitycodes(request):
    activitycodes = ActivityCodes.objects.all()
    if request.method == "POST":
        form = ActivityCodesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('activity-code')
        else:
            return redirect('activity-code')
    else:
        form = ActivityCodesForm()

    context = {
        'form': form,
        'codes': activitycodes,
    }

    return render(request, 'adminapps/entry_activitycodes_1.html', context)


def entry_filingfees(request, pk):
    activitycode = ActivityCodes.objects.get(id=pk)
    filingfee = FilingCodes.objects.filter(activitycode_id=pk)
    if request.method == "POST":
        form = FilingFeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('filingfee-code', pk)
        else:
            return redirect('filingfee-code', pk)
    else:
        form = FilingFeeForm()

    context = {
        'form': form,
        'activity': activitycode,
        'filingfee': filingfee,
        'pk': pk,
    }

    return render(request, 'adminapps/entry_filingfeecodes.html', context)


def edittaskcode(request, pk):
    selected = ActivityCodes.objects.get(id=pk)
    activities = ActivityCodes.objects.all()
    if request.method == "POST":
        form = ActivityCodesForm(request.POST, instance=selected)
        if form.is_valid():
            form.save()
            return redirect('activity-code')
        else:
            return redirect('activity-code')
    else:
        form = ActivityCodesForm(instance=selected)
        context = {
            'form': form,
            'codes': activities,
            'selected': selected,
        }
    return render(request, 'adminapps/entry_activitycodes.html', context)


@login_required
def removetaskcode(request, pk):
    selected = ActivityCodes.objects.get(id=pk)
    codes = ActivityCodes.objects.all()
    selected.delete()
    return redirect('activity-code')


@login_required
def appearanceentry(request):
    appearance = Appearance.objects.all()
    if request.method == "POST":
        form = AppearanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appearance-code')
        else:
            return redirect('appearance-code')
    else:
        form = AppearanceForm()
        context = {
            'form': form,
            'appearance': appearance,
        }
    return render(request, 'adminapps/entry_appearance.html', context)


@login_required
def editappearance(request, pk):
    selected = Appearance.objects.get(id=pk)
    appearance = Appearance.objects.all()
    if request.method == "POST":
        form = AppearanceForm(request.POST, instance=selected)
        if form.is_valid():
            form.save()
            return redirect('appearance-code')
        else:
            return redirect('appearance-code')
    else:
        form = AppearanceForm(instance=selected)
        context = {
            'form': form,
            'appearance': appearance,
        }
    return render(request, 'adminapps/entry_appearance.html', context)


def removeappearance(request, pk):
    selected = Appearance.objects.get(id=pk)
    appearance = Appearance.objects.all()
    selected.delete()
    return redirect('appearance-code')


@login_required
def apptypeentry(request):
    apptype = AppType.objects.all()
    if request.method == "POST":
        form = AppTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('apptype-code')
        else:
            return redirect('apptype-code')
    else:

        form = AppTypeForm()
        context = {
            'form': form,
            'apptype': apptype,
        }
    return render(request, 'adminapps/entry_apptype.html', context)


@login_required
def matterstatusentry(request):
    status = Status.objects.all()
    if request.method == "POST":
        form = MatterStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('matterstatus-code')
        else:
            return redirect('matterstatus-code')
    else:

        form = MatterStatusForm()
        context = {
            'form': form,
            'status': status,
        }
    return render(request, 'adminapps/entry_matterstatus.html', context)


@login_required
def editapptype(request, pk):
    selected = AppType.objects.get(id=pk)
    apptype = AppType.objects.all()
    if request.method == "POST":
        form = AppTypeForm(request.POST, instance=selected)
        if form.is_valid():
            form.save()
            return redirect('apptype-code')
        else:
            return redirect('apptype-code')
    else:

        form = AppTypeForm(instance=selected)
        context = {
            'form': form,
            'apptype': apptype,
        }
    return render(request, 'adminapps/entry_apptype.html', context)


@login_required
def editmatterstatus(request, pk):
    selected = Status.objects.get(id=pk)
    status = Status.objects.all()
    if request.method == "POST":
        form = MatterStatusForm(request.POST, instance=selected)
        if form.is_valid():
            form.save()
            return redirect('matterstatus-code')
        else:
            return redirect('matterstatus-code')
    else:

        form = MatterStatusForm(instance=selected)
        context = {
            'form': form,
            'status': status,
        }
    return render(request, 'adminapps/entry_matterstatus.html', context)


@login_required
def removeapptype(request, pk):
    selected = AppType.objects.get(id=pk)
    apptype = AppType.objects.all()
    selected.delete()
    return redirect('apptype-code')


@login_required
def countryentry(request):
    country = Country.objects.all()
    if request.method == "POST":
        form = EditCountryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('country-code')
        else:
            return redirect('country-code')
    else:
        form = EditCountryForm()
        context = {
            'form': form,
            'countries': country,
        }
    return render(request, 'adminapps/entry_country.html', context)


@login_required
def editcountry(request, pk):
    selected = Country.objects.get(id=pk)
    countries = Country.objects.all().order_by("country")
    if request.method == "POST":
        form = EditCountryForm(request.POST, instance=selected)
        if form.is_valid():
            form.save()
            return redirect('country-code')
        else:
            return redirect('country-code')
    else:
        form = EditCountryForm(instance=selected)
        context = {
            'form': form,
            'selected': selected,
            'countries': countries,
        }
    return render(request, 'adminapps/entry_country.html', context)


@login_required
def removecountry(request, pk):
    selected = Country.objects.get(id=pk)
    countries = Country.objects.all().order_by("country")
    selected.delete()
    return redirect('country-code')


@login_required
def industryentry(request):
    industry = NatureOfBusiness.objects.all()
    if request.method == "POST":
        form = EditIndustryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('industry-code')
        else:
            return redirect('industry-code')
    else:
        form = EditIndustryForm()
        context = {
            'form': form,
            'industry': industry
        }
    return render(request, 'adminapps/entry_industry.html', context)


def industryedit(request, pk):
    selected = NatureOfBusiness.objects.get(id=pk)
    industry = NatureOfBusiness.objects.all()
    if request.method == "POST":
        form = EditIndustryForm(request.POST, instance=selected)
        if form.is_valid():
            form.save()
            return redirect('industry-code')
        else:
            return redirect('industry-code')
    else:
        form = EditIndustryForm(instance=selected)
        context = {
            'form': form,
            'industry': industry
        }
    return render(request, 'adminapps/entry_industry.html', context)


@login_required
def removeindustry(request, pk):
    selected = NatureOfBusiness.objects.get(id=pk)
    industry = NatureOfBusiness.objects.all()
    selected.delete()
    return redirect('industry-code')


@login_required
def arview(request):
    arlist = AccountsReceivable.objects.all()

    context = {
        'arlist': arlist,
    }

    return render(request, 'adminapps/arlist.html', context)


@login_required
def arentry(request):
    if request.method == "POST":
        form = AREntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-ar-list')
        else:
            return redirect('admin-ar-new')
    else:
        form = AREntryForm()
        context = {
            'form': form,
        }

    return render(request, 'adminapps/entry_ar.html', context)


def staffprofile(request):
    return render(request, 'user/profile.html')


def lookuplist(request):
    return render(request, 'adminapps/reference.html')

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

    return render(request, 'adminapps/readmessage_dashboard.html', context)

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
    }

    return render(request, 'adminapps/viewattachment.html', context)

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

    context = {
        'myuserid': myuserid,
        'access_code': access_code,
        'receivedmessages': receivedmessages,
        'sentmessages': sentmessages,
    }

    return render(request, 'adminapps/mymessages.html', context)

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
            return redirect('new_attachment', id)
        else:
            return redirect('new_message')
    else:
        form = InboxMessageNewForm()

    context = {
        'form': form,
        'messagefrom_id': user_message_id,
        'messagefrom': username,
        'messagedate': messagedate,
    }

    return render(request, 'adminapps/new_message.html', context)

def new_attachment(request, pk):
    message = inboxmessage.objects.get(id=pk)
    if request.method == 'POST':
        form = InboxAttachmentEntryForm(request.POST, request.FILES)
        if form.is_valid():
            attach_rec = form.save(commit=False)
            attach_rec.message_id = pk
            attach_rec.save()
            return redirect('new_attachment', pk)
        else:
            return redirect('new_attachment', pk)
    else:
        form = InboxAttachmentEntryForm()

    context = {
        'form': form,
        'message': message,
    }

    return render(request, 'adminapps/new_attachment.html', context)

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

    return render(request, 'adminapps/readsentitems.html', context)

def open_filingdocs(request, pk):
    document = FilingDocs.objects.get(id=pk)
    m_id = document.Task_Detail.matter.id
    matter = Matters.objects.get(id=m_id)
    c_id = matter.folder.client.id

    client = Client_Data.objects.get(id=c_id)
    print(client)
    print(matter.matter_title)
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
    return render(request, 'adminapps/opendocument.html', context)


def search_docs(request):
    access_code = request.user.user_profile.userid
    user_id = User.id

    user_message_id = request.user.user_profile.id
    alertmessages = inboxmessage.objects.filter(
        messageto_id=user_message_id, status="UNREAD")
    countalert = alertmessages.count()
    username = request.user.username



    if 'q' in request.GET:
        q = request.GET['q']
        #clients = Client_Data.objects.filter(client_name__icontains=q)
        multiple_q = Q(Q(Task_Detail__task__icontains=q) | Q(Description__icontains=q) | Q(Task_Detail__doc_type__icontains=q))
        docs = FilingDocs.objects.filter(
            multiple_q).order_by('-DocDate')
    else:
        #clients = Client_Data.objects.all().order_by("client_name")
        docs = FilingDocs.objects.all().order_by('-DocDate')

    noofclients = docs.count()
    paginator = Paginator(docs, 11)
    page = request.GET.get('page')
    all_docs = paginator.get_page(page)

    context = {
        'page': page,
        'noofclients': noofclients,
        'clients': all_docs,
        'alertmessages': alertmessages,
        'noofalerts': countalert,
        'username': username,

    }

    return render(request, 'adminapps/search_docs.html', context) 

def clientsearch_docs(request, pk):
    client = Client_Data.objects.get(id=pk)
    docs = FilingDocs.objects.filter(Task_Detail__matter__folder__client__id=pk).order_by('-DocDate')

    noofclients = docs.count()
    paginator = Paginator(docs, 11)
    page = request.GET.get('page')
    all_docs = paginator.get_page(page)

    context = {
        'page': page,
        'client':client,
        'noofclients': noofclients,
        'clients': all_docs
    }

    return render(request, 'adminapps/clientsearch_docs.html', context) 


def awaiting_docs(request, pk):
    docs = awaitingdocs.objects.filter(matter__folder__client_id=pk).order_by('-awaiting_date')
    client = Client_Data.objects.get(id=pk)

    context = {
        'awaitingdocs' : docs,
        'client_id':pk,
        'client':client,
    }

    return render(request, 'adminapps/awaitingdocs.html', context)

def newawaiting_docs(request, pk):
    client = Client_Data.objects.get(id=pk)
    matterlist = Matters.objects.filter(folder__client__id=pk)
    if request.method == 'POST':
        form = NewAwaitingDocForm(request.POST)
        if form.is_valid():
            awaitingdoc_rec = form.save(commit=False)
            awaitingdoc_rec.matter_id = request.POST['matter']
            awaitingdoc_rec.save()
            return redirect('awaiting_docs', pk)
        else:
            return redirect('newawaiting_docs')
    else:
        form = NewAwaitingDocForm()
    
    context = {
        'form': form,
        'client': client,
        'matterlist':matterlist,
    }
    return render(request, 'adminapps/newawaitingdocs.html', context)

def awaitingdoc_view(request, pk):
    awaitingdoc = awaitingdocs.objects.get(id=pk)
    m_id = awaitingdoc.matter_id
    c_id = awaitingdoc.matter.folder.client.id
    client = Client_Data.objects.get(id=c_id)
    matterlist = Matters.objects.filter(folder__client__id=c_id)

    if request.method == 'POST':
        form = ViewAwaitingDocForm(request.POST, instance=awaitingdoc)
        if form.is_valid():
            form.save()
        else:
            return redirect('awaitingdoc_view', pk, c_id)
    else:
        form = ViewAwaitingDocForm(instance=awaitingdoc)

    context = {
        'form': form,
        'awaitingdoc': awaitingdoc,
        'client': client,
        'matterlist':matterlist,
        'm_id': m_id,
    }

    return render(request, 'adminapps/matterviewawaitingdocs.html', context)

def matterawaiting_docs(request, pk):
    docs = awaitingdocs.objects.filter(matter_id=pk).order_by('-awaiting_date')
    matter = Matters.objects.get(id=pk)

    context = {

        'awaitingdocs' : docs,
        'matter' : matter,
    }

    return render(request, 'adminapps/matterawaitingdocs.html', context)

def addawaitingdocs_matter(request, pk):
    matter = Matters.objects.get(id=pk)
    if request.method == "POST":
        form = NewAwaitingDocForm(request.POST)
        if form.is_valid():
            print("Awaiting Doc Pasok dito")
            awaitingdoc_rec = form.save(commit=False)
            awaitingdoc_rec.matter_id = pk
            awaitingdoc_rec.save()
            return redirect('matterawaiting_docs', pk)

        else:
            return redirect('addawaitingdocs_matter', pk)
    else:
        form = NewAwaitingDocForm()

    context = {
        'form' : form,
        'matter' : matter,

    }

    return render(request, 'adminapps/newmatterawaitingdocs.html', context)






    
