from django.contrib import admin
from .models import *
from userprofile.models import *
from django.contrib.auth.models import Group

admin.site.site_header = 'LEXEnprise System'


class MatterAdmin(admin.ModelAdmin):
    list_display = ('folder', 'matter_title', 'handling_lawyer',
                    'created_at', 'modified_at')
    search_fields = ['matter_title']
    list_per_page = 8
#    list_filter = ('category', 'name')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'email', 'mobile', 'country')


class CaseFolderAdmin(admin.ModelAdmin):
    list_display = ('client', 'folder_description', 'folder_type')


class TaskDetailAdmin(admin.ModelAdmin):
    list_display = ('matter', 'tran_date', 'preparedby', 'task')


class LawyersAdmin(admin.ModelAdmin):
    list_display = ('lawyerID', 'lawyer_name')


# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('userid', 'address', 'rank', 'mobile')

class AlertMessages(admin.ModelAdmin):
    list_display = ('messageto', 'date_alert',
                    'message_alert', 'status', 'sentby')


admin.site.register(Client_Data, ClientAdmin)
admin.site.register(Lawyer_Data, LawyersAdmin)
admin.site.register(Matters, MatterAdmin)
admin.site.register(task_detail, TaskDetailAdmin)
admin.site.register(CaseFolder, CaseFolderAdmin)
admin.site.register(Applicant)
admin.site.register(User_Profile)
admin.site.register(Alert_Messages, AlertMessages)
admin.site.register(NatureOfBusiness)
admin.site.register(Country)
admin.site.register(Contact_Person)
admin.site.register(AccountsReceivable)
admin.site.register(Bills)
admin.site.register(OFees)
admin.site.register(OPE)
admin.site.register(Payments)
admin.site.register(CaseType)
admin.site.register(EntityType)
admin.site.register(NatureOfCase)
admin.site.register(FolderType)
admin.site.register(AppType)
admin.site.register(Appearance)
admin.site.register(AppDueDate)
admin.site.register(ClassOfGoods)
admin.site.register(Action_Order)
admin.site.register(Order_Activity)
admin.site.register(FilingDocs)
admin.site.register(CaseEvidence)
admin.site.register(CaseMatter)
admin.site.register(IPTaskCodes)
admin.site.register(Courts)
admin.site.register(Stages)
admin.site.register(ActivityCodes)
admin.site.register(FilingCodes)
admin.site.register(TempExpenses)
admin.site.register(TempBills)
admin.site.register(TempFilingFees)
admin.site.register(Status)
admin.site.register(IP_Matters)
admin.site.register(MailsIn)
admin.site.register(MailsIn_Matters)
admin.site.register(IPOExaminer)
admin.site.register(DocumentCode)
admin.site.register(Currency)
admin.site.register(inboxmessage)
admin.site.register(messageattachment)
admin.site.register(awaitingdocs)
admin.site.register(client_user_profile)
admin.site.register(client_user_activity)
admin.site.register(inifile)
admin.site.register(sysinifile)


# Register your models here.
