from django.contrib.auth import login
from django.shortcuts import render
from adminapps.models import Client_Data, Matters, task_detail, due_dates

# Create your views here.

def homepage(request):
    activities = task_detail.objects.all()
    matters = Matters.objects.all()
    clients = Client_Data.objects.all()

    clientcount = clients.count()
    activitycount = activities.count()
    matterscount = matters.count()
    
    context = {
        'NoOfActivities' : activitycount,
        'NoOfClients' : clientcount,
        'NoOfMatters' : matterscount,

    }
    return render(request, 'adminapps/index.html', context)

def viewchart(request):
    return render(request, 'adminapps/charts.html')
