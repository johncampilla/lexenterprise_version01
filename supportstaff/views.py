from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from adminapps.models import *
from datetime import date, datetime, timedelta

from django.db.models import Q, Sum, Count

# Create your views here.


@login_required
def main(request):
    access_code = request.user.user_profile.userid
    user_id = User.id
    alertmessages = Alert_Messages.objects.filter(messageto=access_code)
    countalert = alertmessages.count()
    srank = request.user.user_profile.rank
    username = request.user.username
    lawyers = request.user.user_profile.supporto
    listoflawyers = lawyers.split(',')
    for i in range(0, len(listoflawyers)):
        print(listoflawyers[i])

    context = {
        'alertmessages': alertmessages,
        'noofalerts': countalert,
        'username': username,
    }

    return render(request, 'supportstaff/index.html', context)
