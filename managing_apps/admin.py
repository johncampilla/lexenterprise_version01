from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(AppType)
admin.site.register(LawyersCases)
admin.site.register(ClientSummaryCount)
admin.site.register(LawyerSummary)
admin.site.register(CaseTypeSummary)
