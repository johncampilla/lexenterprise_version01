from dataclasses import fields
from logging import PlaceHolder
from turtle import textinput
from django import forms
from django.forms import TextInput, ModelForm, DateTimeInput
from django.db.models.query import QuerySet
from django.forms import widgets
from django.forms.widgets import NumberInput, TextInput, Textarea, Widget
from .models import *
from userprofile.models import User_Profile


class AREntryForm(forms.ModelForm):
    class Meta:
        model = AccountsReceivable
        fields = 'matter', 'bill_number', 'bill_date', 'lawyer', 'bill_amount', 'pf_amount', 'ofees_amount', 'ope_amount', 'payment_tag', 'DocPDFs'
        widgets = {
            'bill_date': NumberInput(attrs={'type': 'date'})

        }


class ClientModifyForm(forms.ModelForm):
    class Meta:
        model = Client_Data
        fields = '__all__'


class FolderModifyForm(forms.ModelForm):
    class Meta:
        model = CaseFolder
        fields = '__all__'


class ClientEntryForm(forms.ModelForm):
    #    country = forms.ModelChoiceField(queryset=Country.objects.filter(country="Russia"))

    class Meta:
        model = Client_Data
        fields = 'client_name', 'address', 'country', 'city', 'state', 'email', 'mobile', 'main_contact', 'category', 'industry', 'entity_type', 'date_acquired', 'status', 'referredby', 'remarks'
        # labels = {
        #     'client_name': 'Client',
        #     'address':'Full Address',
        #     'country':'Country',
        #     'email':'E-Mail',
        #     'mobile':'Phone Number',
        #     'main_contact':'Contact Person/Account Officer',
        #     'category':'Category',
        #     'industry':'Nature Of Business',
        #     'entity_type': 'Entity Type',
        #     'date_acquired': 'Date Acquired',
        #     'status':'Status',
        #     'referredby':'Referal By'}
        widgets = {
            'client_name': Textarea(attrs={'class': 'form-control', 'cols': 200, 'rows': 2}),
            'address': Textarea(attrs={'class': 'form-control', 'cols': 200, 'rows': 2}),
            'remarks': Textarea(attrs={'class': 'form-control', 'cols': 200, 'rows': 2}),
            'date_acquired': NumberInput(attrs={'type': 'date'})

        }


class FilingDocsEntry(forms.ModelForm):
    class Meta:
        model = FilingDocs
        fields = 'DocDate', 'DocsPDF', 'Description'
        widgets = {
            'DocDate': NumberInput(attrs={'type': 'date'}),
            'Description': Textarea(attrs={'class': 'form-control', 'cols': 200, 'rows': 2}),
        }


class ReplyToMessageForm(forms.ModelForm):
    class Meta:
        model = inboxmessage
        fields =  'messagebox',
        widgets = {
            'messagebox': Textarea(attrs={'cols': 200, 'rows': 10, 'placeholder': 'Type here your message...'}),
        }

class AlertMessageForm(forms.ModelForm):
    class Meta:
        model = inboxmessage
        fields = 'messageto', 'messagedate', 'messagefrom', 'subject', 'messagebox', 'status', 'see_matter', 'updatedby'
        widgets = {
            'messagebox': Textarea(attrs={'cols': 200, 'rows': 10}),
            'messagedate': NumberInput(attrs={'type': 'date'}),
        }


class AlertUpdateStatusForm(forms.ModelForm):
    class Meta:
        model = Alert_Messages
        fields = 'status',


class UserEntryForm(forms.ModelForm):
    class Meta:
        model = User_Profile
        fields = 'userid', 'address', 'rank', 'mobile', 'image', 'supporto', 'remarks'
        widgets = {
            'remarks': Textarea(attrs={'cols': 200, 'rows': 3}),
        }


class InboxMessageForm(forms.ModelForm):
    class Meta:
        model = inboxmessage
        fields = 'messageto', 'messagedate', 'messagefrom', 'subject', 'messagebox', 'status', 'see_matter', 'updatedby'
        widgets = {
            'messagebox': Textarea(attrs={'cols': 200, 'rows': 10}),
            'messagedate': NumberInput(attrs={'type': 'date'}),

        }


class InboxAttachmentEntryForm(forms.ModelForm):
    class Meta:
        model = messageattachment
        fields = 'description', 'DocsPDF'


class InboxAttachmentViewForm(forms.ModelForm):
    class Meta:
        model = messageattachment
        fields = 'description', 'DocsPDF'


class InboxMessageEntryForm(forms.ModelForm):
    class Meta:
        model = inboxmessage
        fields = 'subject', 'messagebox', 'see_matter'
        widgets = {
            'messagebox': Textarea(attrs={'cols': 200, 'rows': 10}),
            'messagedate': NumberInput(attrs={'type': 'date'}),

        }


class InboxMessageNewForm(forms.ModelForm):
    class Meta:
        model = inboxmessage
        fields = 'messageto', 'subject', 'messagebox', 'see_matter'
        widgets = {
            'messagebox': Textarea(attrs={'cols': 200, 'rows': 10}),
            'messagedate': NumberInput(attrs={'type': 'date'}),

        }
class LawyerEntryForm(forms.ModelForm):
    class Meta:
        model = Lawyer_Data
        fields = '__all__'
        widgets = {
            'remarks': Textarea(attrs={'cols': 200, 'rows': 3}),
            'Specialization': Textarea(attrs={'cols': 200, 'rows': 3}),
        } 

class UserEntryForm(forms.ModelForm):
    class Meta:
        model = User_Profile
        fields = '__all__'
        widgets = {
            'remarks': Textarea(attrs={'cols': 200, 'rows': 3}),
            'date_acquired' : NumberInput(attrs={'type': 'date'}),
        }

class newmailform(forms.ModelForm):
    class Meta:
        model = task_detail
        fields = 'matter', 'tran_date','task_code', 'preparedby', 'lawyer', 'task', 'doc_date','mailing_date', 'examiner', 'mail_type', 'contact_person', 'duecode'
        widgets = {
            'task': Textarea(attrs={'cols': 200, 'rows': 3}),
            'tran_date': NumberInput(attrs={'type': 'date'}),
            'doc_date': NumberInput(attrs={'type': 'date'}),
            'mailing_date': NumberInput(attrs={'type': 'date'}),
        }
        
class MailsInwardFormNew(forms.ModelForm):
    class Meta:
        model = task_detail
        fields = 'matter', 'tran_date','task_code', 'preparedby', 'lawyer', 'task', 'doc_date','mailing_date', 'examiner', 'mail_type', 'contact_person', 'duecode'
        widgets = {
            'task': Textarea(attrs={'cols': 200, 'rows': 3}),
            'tran_date': NumberInput(attrs={'type': 'date'}),
            'doc_date': NumberInput(attrs={'type': 'date'}),
            'mailing_date': NumberInput(attrs={'type': 'date'}),
        }

class MailsInwardFormNew(forms.ModelForm):
    class Meta:
        model = task_detail
        fields = 'matter', 'tran_date','task_code', 'preparedby', 'lawyer', 'task', 'doc_date','mailing_date', 'examiner', 'mail_type', 'contact_person', 'duecode'
        widgets = {
            'task': Textarea(attrs={'cols': 200, 'rows': 3}),
            'tran_date': NumberInput(attrs={'type': 'date'}),
            'doc_date': NumberInput(attrs={'type': 'date'}),
            'mailing_date': NumberInput(attrs={'type': 'date'}),
        }

class MailsInwardFormUpdate(forms.ModelForm):
    class Meta:
        model = task_detail
        fields = 'tran_date', 'preparedby', 'lawyer', 'task', 'task_code','doc_date', 'mail_type', 'mailing_date', 'examiner', 'contact_person', 'duecode'
        widgets = {
            'task': Textarea(attrs={'cols': 200, 'rows': 3}),
            'tran_date': NumberInput(attrs={'type': 'date'}),
            'doc_date': NumberInput(attrs={'type': 'date'}),
            'mailing_date': NumberInput(attrs={'type': 'date'}),

        }

class MailsIn_IPO(forms.ModelForm):
    class Meta:
        model = task_detail
        fields = 'tran_date','lawyer', 'task', 'task_code' ,'doc_date', 'mailing_date', 'examiner', 'duecode'
        widgets = {
            'task': Textarea(attrs={'cols': 200, 'rows': 3}),
            'tran_date': NumberInput(attrs={'type': 'date'}),
            'doc_date': NumberInput(attrs={'type': 'date'}),
            'mailing_date': NumberInput(attrs={'type': 'date'}),
        }

class MailsIn_REG(forms.ModelForm):
    class Meta:
        model = task_detail
        fields = 'tran_date','lawyer', 'task', 'task_code', 'tran_type', 'doc_type', 'mail_type', 'doc_date', 'lawyer', 'contact_person', 'duecode','mailing_date', 'examiner', 'duecode'
        widgets = {
            'task': Textarea(attrs={'cols': 200, 'rows': 3}),
            'tran_date': NumberInput(attrs={'type': 'date'}),
            'doc_date': NumberInput(attrs={'type': 'date'}),
            'mailing_date': NumberInput(attrs={'type': 'date'}),
        }

class AddTaskEntryForm(forms.ModelForm):
    class Meta:
        model  = task_detail
        fields = 'matter', 'tran_date','task_code', 'doc_type','tran_type','preparedby', 'lawyer', 'task', 'doc_date','mailing_date', 'examiner', 'mail_type', 'contact_person', 'duecode', 'spentinhrs', 'spentinmin'
        widgets = {
            'task': Textarea(attrs={'cols': 200, 'rows': 3}),
            'tran_date': NumberInput(attrs={'type': 'date'}),
            'doc_date': NumberInput(attrs={'type': 'date'}),
            'mailing_date': NumberInput(attrs={'type': 'date'}),

        }

class TaskEntryForm(forms.ModelForm):
    # TRANTYPE = {
    #     ('Billable', 'Billable'),
    #     ('Non-Billable', 'Non-Billable'),
    # }
    class Meta:
        model = task_detail
        fields = 'tran_date', 'tran_type', 'doc_type', 'lawyer','task_code','task','spentinhrs', 'spentinmin'
        widgets = {
            'task': Textarea(attrs={'cols': 200, 'rows': 3, 'placeholder': 'Type here the activity details..'}),
            'tran_date': NumberInput(attrs={'type': 'date'}),
            'doc_date': NumberInput(attrs={'type': 'date'}),
            'mailing_date': NumberInput(attrs={'type': 'date'}),

        }

class TaskEntryFormLawyer(forms.ModelForm):
    # TRANTYPE = {
    #     ('Billable', 'Billable'),
    #     ('Non-Billable', 'Non-Billable'),
    # }
    class Meta:
        model = task_detail
        fields = 'tran_date', 'tran_type', 'doc_type', 'task','spentinhrs', 'spentinmin'
        widgets = {
            'task': Textarea(attrs={'cols': 200, 'rows': 3, 'placeholder': 'Type here the activity details..'}),
            'tran_date': NumberInput(attrs={'type': 'date'}),
            'doc_date': NumberInput(attrs={'type': 'date'}),
            'mailing_date': NumberInput(attrs={'type': 'date'}),

        }


    # matter = forms.ModelChoiceField(label="Matter", queryset=Matters.objects.all().order_by('matter_title'))
    # tran_date = forms.DateField(label='Activity Date', widget=NumberInput(attrs={'type':'date'}))
    # tran_type = forms.ChoiceField(label='Transaction Type', widget=forms.RadioSelect, choices=TRANTYPE)
    # preparedby = forms.ModelChoiceField(label='Prepared By', queryset=User_Profile.objects.all())
    # lawyer = forms.ModelChoiceField(label='Lawyer', queryset=Lawyer_Data.objects.all())
    # task = forms.CharField(label="Activity ", widget=forms.Textarea(attrs={'rows':3}))
    # order_compliance = forms.ModelChoiceField(label="Order Compliance", queryset=Order_Activity.objects.all())
    # DocPDFs = forms.FileField()

#    date_acquired = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

# class EntryFolderForm(forms.ModelForm):
#     class Meta:
#         model = CaseFolder
#         fields= '__all__'


class TaskEditForm(forms.ModelForm):
    # TRANTYPE = {
    #     ('Billable', 'Billable'),
    #     ('Non-Billable', 'Non-Billable'),
    # }
    class Meta:
        model = task_detail
        fields = 'matter', 'tran_date', 'task_code', 'tran_type', 'doc_type', 'preparedby', 'lawyer', 'task', 'spentinhrs', 'spentinmin'
        widgets = {
            'task': Textarea(attrs={'cols': 200, 'rows': 3, 'placeholder': 'Activity Details..'}),
            'tran_date': NumberInput(attrs={'type': 'date'}),
            'doc_date': NumberInput(attrs={'type': 'date'}),
            'mailing_date': NumberInput(attrs={'type': 'date'}),

        }


class TaskEntryForm1(forms.Form):
    # TRANTYPE = {
    #     ('Billable', 'Billable'),
    #     ('Non-Billable', 'Non-Billable'),
    # }
    # class Meta:
    #     model = task_detail
    #     fields = 'matter', 'tran_date', 'task_code', 'doc_type', 'tran_type','preparedby', 'lawyer', 'task'
    #     task_code = forms.ModelChoiceField(queryset=AppType.objects.all())
    #     widgets = {
    #         'task' :Textarea(attrs={'cols': 200, 'rows': 3}),
    #         'tran_date':NumberInput(attrs={'type':'date'}),

    # }

    DOCTYPE = {
        ('MailsIn', 'MailsIn'),
        ('MailsOut', 'MailsOut'),
        ('Activity', 'Activity'),
    }
    TRANTYPE = {
        ('Billable', 'Billable'),
        ('Non-Billable', 'Non-Billable'),

    }

    matter = forms.ModelChoiceField(
        label="Matter", queryset=Matters.objects.all().order_by('matter_title'))
    tran_date = forms.DateField(
        label='Activity Date', widget=NumberInput(attrs={'type': 'date'}))
    task_code = forms.ModelChoiceField(
        label='Task Code', queryset=ActivityCodes.objects.all())
    doc_type = forms.ChoiceField(
        label='Document Type', widget=forms.RadioSelect, choices=DOCTYPE)
    tran_type = forms.ChoiceField(
        label='Transaction Type', widget=forms.RadioSelect, choices=TRANTYPE)
    preparedby = forms.ModelChoiceField(
        label='Prepared By', queryset=User_Profile.objects.all())
    lawyer = forms.ModelChoiceField(
        label='Lawyer', queryset=Lawyer_Data.objects.all())
    task = forms.CharField(
        label="Activity ", widget=forms.Textarea(attrs={'rows': 3}))

#    date_acquired = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


class MailsInwardForm(forms.ModelForm):
    class Meta:
        model = task_detail
        fields = 'matter', 'tran_date', 'tran_type', 'doc_type', 'task', 'doc_date', 'mailing_date', 'examiner', 'mail_type', 'contact_person', 'task_code'
        widgets = {
            'task': Textarea(attrs={'cols': 200, 'rows': 3}),
            'tran_date': NumberInput(attrs={'type': 'date'}),
            'doc_date': NumberInput(attrs={'type': 'date'}),
            'mailing_date': NumberInput(attrs={'type': 'date'}),

        }


class PaymentEntryForm(forms.Form):
    PAYMENTFOR = (
        ('PF', 'for professional fees'),
        ('OFEE', 'For filing fees'),
        ('OPE', 'for expense fees'),
        ('Full', 'Full Payment'),
        ('Partial', 'Partial Payment')
    )

    matter = forms.ModelChoiceField(
        label="Matter", queryset=Matters.objects.all().order_by('matter_title'))
    bill_number = forms.ModelChoiceField(
        label="Bill Number", queryset=AccountsReceivable.objects.all().order_by('bill_date'))
    payment_date = forms.DateField(
        label='Payment Date', widget=NumberInput(attrs={'type': 'date'}))
    pay_amount = forms.DecimalField(label="Pay Amount")
    payment_for = forms.ChoiceField(choices=PAYMENTFOR)
    or_number = forms.CharField(label="OR Number", max_length=15)
    or_date = forms.DateField(
        label='OR Date', widget=NumberInput(attrs={'type': 'date'}))
    or_amount = forms.DecimalField(label="OR Amount")
    bank_details = forms.CharField(label="Bank Details", max_length=150)
    payment_reference = forms.CharField(
        label="Payment Reference", max_length=30)
    reference_date = forms.DateField(
        label='Reference Date', widget=NumberInput(attrs={'type': 'date'}))
    Charge_details = forms.CharField(
        label="Charger Details if any", max_length=30)
    Charge_Amount = forms.DecimalField(label="Charge Amount")


class BillEntryForm(forms.Form):
    CURRENCY = {
        ('Dollar', 'Dollar'),
        ('Peso', 'Peso'),
    }

    PAYMENTTAG = (
        ('UN', 'UNPAID'),
        ('PD', 'PAID'),
        ('PP', 'PARIALLY PAID'),
        ('CN', 'CANCELLED'),
    )

    matter = forms.ModelChoiceField(
        label="Matter", queryset=Matters.objects.all().order_by('matter_title'))
    bill_number = forms.CharField(label="Bill Number", max_length=15)
    bill_date = forms.DateField(
        label='Bill Date', widget=NumberInput(attrs={'type': 'date'}))
    currency = forms.ChoiceField(
        label='Currency', widget=forms.RadioSelect, choices=CURRENCY)
    bill_amount = forms.DecimalField(label="Bill Amount")
    pf_amount = forms.DecimalField(label="PF Amount")
    ofees_amount = forms.DecimalField(label="Filing Fee")
    ope_amount = forms.DecimalField(label="OPE Expense")
    payment_tag = forms.ChoiceField(choices=PAYMENTTAG)
    DocPDFs = forms.FileField()
    prepared_by = forms.CharField(label="Prepared By", max_length=15)


class DocumentEditForm(forms.ModelForm):
    class Meta:
        model = FilingDocs
        fields = '__all__'
        widgets = {
            'DocDate': NumberInput(attrs={'type': 'date'}),
        }

class DueDateEntryForm(forms.ModelForm):
    class Meta:
        model = AppDueDate
        fields = 'duedate', 'assignto', 'particulars', 'date_complied'
        widgets = {
            'particulars': Textarea(attrs={'cols': 200, 'rows': 3}),
            'duedate': NumberInput(attrs={'type': 'date'}),
            'date_complied': NumberInput(attrs={'type': 'date'}),

        }


    # matter = forms.ModelChoiceField(label="Matter", queryset=Matters.objects.all().order_by('matter_title'))
    # duecode = forms.CharField(label="Due Code", max_length=20)
    # duedate = forms.DateField(label='Due Date', widget=NumberInput(attrs={'type':'date'}))
    # assignto = forms.ModelChoiceField(label="Lawyer", queryset=Lawyer_Data.objects.all().order_by('lawyer_name'))
    # particulars = forms.CharField(label="Particulars ", widget=forms.Textarea(attrs={'rows':3}))
    # date_complied= forms.DateField(label='Date Complied', widget=NumberInput(attrs={'type':'date'}))


# class EntryFolderForm(forms.Form):
#     client = forms.ModelChoiceField(label="Client", queryset=Client_Data.objects.all().order_by("client_name"))
#     folder_description = forms.CharField(label="Folder Description", max_length=200)
#     folder_type = forms.ModelChoiceField(label="Folder Type", queryset=FolderType.objects.all().order_by("folder"))
#     Supervisinglawyer = forms.ModelChoiceField(label="Supervising Lawyer", queryset=Lawyer_Data.objects.all().order_by("lawyer_name"))
#     remarks = forms.CharField(label="Remarks", widget=forms.Textarea(attrs={'rows':2}))

class EntryFolderForm(forms.ModelForm):
    class Meta:
        model = CaseFolder
        fields = '__all__'
        widgets = {
            'folder_description': Textarea(attrs={'cols': 200, 'rows': 2}),
            'remarks': Textarea(attrs={'cols': 200, 'rows': 2})
        }


class DueCodeEntryForm(forms.ModelForm):
    class Meta:
        model = DueCode
        fields = '__all__'


class NatureOfCaseForm(forms.ModelForm):
    class Meta:
        model = NatureOfCase
        fields = '__all__'


class EntryExpensesForm(forms.ModelForm):
    class Meta:
        model = TempExpenses
        fields = 'tran_date', 'expense_detail', 'expense_actual_amt', 'currency', 'pesorate', 'pesoamount', 'status', 'chargetoclient', 'DocPDFs'
        widgets = {
            'tran_date': NumberInput(attrs={'type': 'date'}),
            'expense_detail': Textarea(attrs={'cols': 250, 'rows': 2})
        }


class EntryBillForm(forms.ModelForm):
    class Meta:
        model = TempBills
        fields = 'matter', 'tran_date', 'bill_service', 'lawyer', 'particulars', 'spentinhrs', 'spentinmin', 'amount', 'prepared_by'
        widgets = {
            'tran_date': NumberInput(attrs={'type': 'date'}),
            'particulars': Textarea(attrs={'cols': 200, 'rows': 2})

        }

class OpendocForm(forms.ModelForm):
    class Meta:
        model = FilingDocs
        fields = ['DocsPDF']   

class NewAwaitingDocForm(forms.ModelForm):
    class Meta:
        model = awaitingdocs
        fields = 'awaiting_date', 'particulars', 'status'
        widgets = {
            'awaiting_date': NumberInput(attrs={'type': 'date'}),
            'particulars': Textarea(attrs={'cols': 200, 'rows': 2})
        }

class ViewAwaitingDocForm(forms.ModelForm):
    class Meta:
        model = awaitingdocs
        fields = 'matter','tran_date', 'awaiting_date', 'lawyer', 'particulars', 'status'
        widgets = {
            'tran_date': NumberInput(attrs={'type': 'date'}),
            'awaiting_date': NumberInput(attrs={'type': 'date'}),
            'particulars': Textarea(attrs={'cols': 200, 'rows': 2})
        }

class EntryMatterForm(forms.ModelForm):

    class Meta:
        model = Matters
#        fields = '__all__'
        fields = 'appearance', 'case_type', 'apptype', 'nature', 'handling_lawyer', 'lawyers_involve', 'filed_at','matter_title', "opposing_counsel", 'remarks'
        widgets = {
            'matter_title': Textarea(attrs={'cols': 200, 'rows': 2}),
            "lawyers_involve": Textarea(attrs={"placeholder": "type here the initials of the lawyers and put a comma in between...", "rows": 1}),
            "opposing_counsel": Textarea(attrs={"placeholder": "type here the name of the opposing law firm and lawyers...", "rows": 1}),
            'remarks': Textarea(attrs={'cols': 200, 'rows': 2})
        }

class ReviewMatterForm(forms.ModelForm):

    class Meta:
        model = Matters
        fields = 'appearance', 'referenceno', 'filing_date', 'filed_at', 'case_type', 'apptype', 'nature', 'matter_contact_person', 'lawyers_involve', 'matter_title', 'clientrefno', 'matterno', 'status', 'remarks', "opposing_counsel"
        widgets = {
            'matter_title': Textarea(attrs={'cols': 200, 'rows': 2}),
            "lawyers_involve": Textarea(attrs={"placeholder": "type here the initials of the lawyers and put a comma in between...", "rows": 1}),
            "opposing_counsel": Textarea(attrs={"placeholder": "type here the name of the opposing law firm and lawyers...", "rows": 1}),
            'filing_date': NumberInput(attrs={'type': 'date'}),
            'remarks': Textarea(attrs={'cols': 200, 'rows': 2})
        }

class EditMatterForm(forms.ModelForm):

    class Meta:
        model = Matters
        fields = 'referenceno', 'filing_date', 'filed_at', 'matter_contact_person', 'clientrefno', 'matterno', 'status', 'remarks',
        widgets = {
            'filing_date': NumberInput(attrs={'type': 'date'}),
            'remarks': Textarea(attrs={'cols': 200, 'rows': 2})
        }


class MatterHeaderForm(forms.ModelForm):
    class Meta:
        model = Matters
        fields = 'folder', 'appearance', 'referenceno', 'filing_date', 'case_type', 'handling_lawyer', \
            'matter_title'
        widgets = {
            'matter_title': Textarea(attrs={'cols': 200, 'rows': 3}),
            'filing_date': NumberInput(attrs={'type': 'date'}),
            'remarks': Textarea(attrs={'cols': 200, 'rows': 2})
        }


class ApplicantEntryForm(forms.ModelForm):
    class Meta:
        model  = Applicant
        fields = 'applicant', 'address', 'title', 'email' 
        widgets = {
            'applicant': Textarea(attrs={'cols': 200, 'rows': 2}),
            'address': Textarea(attrs={'cols': 200, 'rows': 2}),

        }

class IPDetailForm(forms.ModelForm):
    # matter, applicant, ipo_examiner, status, certificate_no, registration_date, ipc_appno,
    # ipc_appdate, publication_reference, publication_date, priority_number, priority_date,
    # priority_country_filing, pct_appno, pct_appdate, pct_publication, pct_pubdate, lng_interappln,
    # lng_interpubln, reason_withdrawn, date_Of_PCTPriority, copyright_number

    class Meta:
        model = IP_Matters
        fields = 'ipo_examiner', 'status', 'reason_withdrawn', 'certificate_no', \
            'registration_date', 'ipc_appno', 'ipc_appdate', 'publication_reference', \
            'publication_date', 'priority_number', 'priority_date', 'priority_country_filing',\
            'pct_appno', 'pct_appdate', 'pct_publication', 'pct_pubdate', 'lng_interappln', \
            'lng_interpubln', 'date_Of_PCTPriority', 'copyright_number', 'renewal_date'
        labels = {
            'matter': 'Matter Title',
        }

        widgets = {
            'registration_date': NumberInput(attrs={'type': 'date'}),
            'ipc_appdate': NumberInput(attrs={'type': 'date'}),
            'publication_date': NumberInput(attrs={'type': 'date'}),
            'priority_date': NumberInput(attrs={'type': 'date'}),
            'pct_appdate': NumberInput(attrs={'type': 'date'}),
            'pct_pubdate': NumberInput(attrs={'type': 'date'}),
            'date_Of_PCTPriority': NumberInput(attrs={'type': 'date'}),
            'date_Of_PCTPriority': NumberInput(attrs={'type': 'date'}),
            'renewal_date': NumberInput(attrs={'type': 'date'}),
            'reason_withdrawn': Textarea(attrs={'cols': 200, 'rows': 3}),


        }


class EditClientForm(forms.ModelForm):
    class Meta:
        model = Client_Data
        fields = '__all__'


class EditCountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = 'country',
        widgets = {
            "country": Textarea(
                attrs={
                    "placeholder": "Country Name",
                    "rows": 1,
                }
            )
        }


class EditIndustryForm(forms.ModelForm):
    class Meta:
        model = NatureOfBusiness
        fields = 'industry',
        widgets = {
            "industry": Textarea(
                attrs={
                    "placeholder": "Industry Name",
                    "rows": 1,
                }
            )
        }


class CaseTypeForm(forms.ModelForm):
    class Meta:
        model = CaseType
        fields = 'case_type',
        widgets = {
            "case_type": Textarea(
                attrs={
                    "placeholder": "Type of Case",
                    "rows": 1,
                }
            )
        }


class FolderTypeForm(forms.ModelForm):
    class Meta:
        model = FolderType
        fields = 'folder',
        widgets = {
            "folder": Textarea(
                attrs={
                    "placeholder": "type of folder",
                    "rows": 1,
                }
            )
        }


class EntityForm(forms.ModelForm):
    class Meta:
        model = Courts
        fields = '__all__'


class ActivityCodesForm(forms.ModelForm):
    class Meta:
        model = ActivityCodes
        fields = '__all__'
        widgets = {
            'bill_description': Textarea(attrs={'cols': 200, 'rows': 2}),
            'Activity': Textarea(
                attrs={
                    "placeholder": "Enter Activity/Task Descriptiontype",
                    "rows": 3,
                }
            )
        }


class FilingFeeForm(forms.ModelForm):
    class Meta:
        model = FilingCodes
        fields = '__all__'
        widgets = {
            'filing_description': Textarea(attrs={'cols': 200, 'rows': 2}),
            'filing': Textarea(attrs={'cols': 200, 'rows': 2}),
        }


class AppearanceForm(forms.ModelForm):
    class Meta:
        model = Appearance
        fields = '__all__'


class AppTypeForm(forms.ModelForm):
    class Meta:
        model = AppType
        fields = '__all__'


class MatterStatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = '__all__'


class ModifyClientForm(forms.ModelForm):

    class Meta:
        model = Client_Data
        fields = 'client_name', 'industry', 'date_acquired', 'address', 'country', 'email', 'mobile', 'main_contact'
        widgets = {
            #            'client_name' :Textarea(attrs={'cols': 200, 'rows': 1}),
            'date_acquired': NumberInput(attrs={'type': 'date'}),
        }


class Non_IPDetailForm(forms.ModelForm):
    class Meta:
        model = CaseMatter
        fields = 'case_description', 'case_theory'
        widgets = {
            'case_description': Textarea(attrs={'cols': 200, 'rows': 3}),
            'case_theory': Textarea(attrs={'cols': 200, 'rows': 3}),

        }


class MailsInwardEntry(forms.ModelForm):
    class Meta:
        model = MailsIn
        fields = '__all__'
        widgets = {
            'particulars': Textarea(attrs={'cols': 200, 'rows': 3, "placeholder": "Type here the mail description in details", }),
            'date_receipt': NumberInput(attrs={'type': 'date'}),
            'doc_date': NumberInput(attrs={'type': 'date'}),
            'mailing_date': NumberInput(attrs={'type': 'date'}),

        }


class ClassOfGoodsEntry(forms.ModelForm):
    class Meta:
        model = ClassOfGoods
        fields = 'classes', 'Goods_Descriptions'
        widgets = {
            'Goods_Descriptions': Textarea(attrs={'cols': 200, 'rows': 4}),
        }
