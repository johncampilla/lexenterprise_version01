from locale import currency
from math import degrees
from os import makedirs, times_result
from pydoc import describe
from typing import Text
from unittest.mock import DEFAULT
from urllib.parse import MAX_CACHE_SIZE
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.enums import Choices
from django.db.models.fields import CharField, DateField, TextField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey
from django.test import ignore_warnings
from userprofile.models import User_Profile
from django.contrib.auth.models import User

# Create your models here.


class NatureOfBusiness(models.Model):
    industry = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = 'Nature Of Business'

    def __str__(self):
        return f'{self.industry}'


class Currency(models.Model):
    currency = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    local_rate = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return f'{self.currency}'


class Courts(models.Model):
    court = models.CharField(max_length=60)
    address = models.CharField(max_length=200, blank=True, null=True)
    contact_person = models.CharField(max_length=150, blank=True, null=True)
    contact_number = models.CharField(max_length=100, blank=True, null=True)
    presiding_judge = models.CharField(max_length=150, blank=True, null=True)
    remarks = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Courts"

    def __str__(self):
        return f'{self.court}'


class Country(models.Model):
    country = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return f'{self.country}'


class Lawyer_Data(models.Model):
    lawyerID = models.ForeignKey(User_Profile, on_delete=models.PROTECT)
    lawyer_name = models.CharField(max_length=60)
    access_code = models.CharField(max_length=5)
    phone = models.CharField(max_length=100)
    hourlyrate = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    IBPRollNo = models.CharField(max_length=40, blank=True, null=True)
    IBPChapter = models.CharField(max_length=35, blank=True, null=True)
    IBPLifetimeNo = models.CharField(max_length=35, blank=True, null=True)
    Specialization = models.CharField(max_length=150, blank=True, null=True)
    profile_pic = models.ImageField(blank=True)
    remarks = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Lawyers'

    def __str__(self):
        return f'{self.access_code}'


class Client_Data(models.Model):

    CATEGORIES = (
        ('Corporate', 'Corporate'),
        ('Individual', 'Individual'),
    )

    ENTITYTYPE = (
        ('Big Entity', 'Big Entity'),
        ('Medium Entity', 'Medium Entity'),
        ('Small Entity', 'Small Entity')
    )
    STATUS = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Blacklisted', 'Blacklisted')
    )

    client_name = models.CharField(max_length=200)
    industry = models.ForeignKey(
        NatureOfBusiness, on_delete=CASCADE, null=True)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    address = models.CharField(max_length=250, null=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=CASCADE, null=True)
    email = models.EmailField(max_length=200, null=True)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    main_contact = models.CharField(max_length=100, null=True)
    entity_type = models.CharField(
        max_length=20, choices=ENTITYTYPE, null=True, blank=True)
    date_acquired = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS, default="Active")
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    referredby = models.CharField(max_length=150, blank=True)

    class Meta:
        verbose_name_plural = 'Clients'

    def __str__(self):
        return f'{self.client_name}'


class Contact_Person(models.Model):
    client = models.ForeignKey(Client_Data, on_delete=CASCADE, null=True)
    contact_person = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Client's Contact Persons"

    def __str__(self):
        return f'{self.contact_person}'


class FolderType(models.Model):
    folder = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Folder Type'

    def __str__(self):
        return f'{self.folder}'


class CaseFolder(models.Model):
    # FOLDERTYPE = (
    #     ('Intellectual Property', 'Intellectual Property'),
    #     ('Litigation', 'Litigation'),
    #     ('Contracts', 'Contracts'),
    #     ('Corporate', 'Corporate'),
    #     ('Special Project', 'Special Project')
    # )

    client = models.ForeignKey(
        Client_Data, on_delete=CASCADE, null=True)
    folder_description = models.CharField(max_length=200)
    folder_type = models.ForeignKey(
        FolderType, on_delete=models.CASCADE, null=True)
    Supervisinglawyer = models.ForeignKey(
        Lawyer_Data, on_delete=CASCADE, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Case Folders'

    def __str__(self):
        return f'{self.client} - {self.folder_description}'


class EntityType(models.Model):
    entity_type = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = 'Entities/Agencies'

    def __str__(self):
        return f'{self.entity_type}'


class CaseType(models.Model):
    case_type = models.CharField(max_length=60)

    class Meta:
        verbose_name_plural = 'Case Type'

    def __str__(self):
        return f'{self.case_type}'


class NatureOfCase(models.Model):
    casetype = models.ForeignKey(
        CaseType, on_delete=models.PROTECT, null=True, blank=True)
    nature = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Natures Of Cases'

    def __str__(self):
        return f'{self.nature}'


class AppType(models.Model):
    apptype = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'Types Of IP Applications'

    def __str__(self):
        return f'{self.apptype}'


class Appearance(models.Model):
    appearance = CharField(max_length=30, null=True)

    class Meta:
        verbose_name_plural = 'Appearance'

    def __str__(self):
        return f'{self.appearance}'


class Stages(models.Model):
    casetype = models.ForeignKey(CaseType, on_delete=models.CASCADE, null=True)
    stages = models.CharField(max_length=60)

    class Meta:
        verbose_name_plural = "Stages Of The Case"

    def __str__(self):
        return f'{self.casetype} - {self.stages}'


class Status(models.Model):
    status = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f'{self.status}'


class Matters(models.Model):
    folder = models.ForeignKey(CaseFolder, on_delete=CASCADE, null=True)
    referenceno = models.CharField(max_length=30, blank=True)
    clientrefno = models.CharField(max_length=60, blank=True)
    matterno = models.CharField(max_length=30, blank=True)
    filing_date = models.DateField(null=True, blank=True)
    filed_at = models.ForeignKey(
        Courts, on_delete=models.CASCADE, blank=True, null=True)
    case_type = models.ForeignKey(CaseType, on_delete=models.CASCADE)
    apptype = models.ForeignKey(AppType, on_delete=models.CASCADE)
    nature = models.ForeignKey(NatureOfCase, on_delete=CASCADE)
    matter_title = TextField(null=True)
    status = models.ForeignKey(
        Status, on_delete=models.CASCADE, null=True, blank=True)
    appearance = models.ForeignKey(
        Appearance, on_delete=models.CASCADE, null=True, blank=True)
    handling_lawyer = models.ForeignKey(Lawyer_Data, on_delete=models.CASCADE)
    matter_contact_person = models.ForeignKey(
        Contact_Person, on_delete=models.PROTECT, null=True, blank=True)
    lawyers_involve = models.CharField(max_length=60, blank=True, null=True)
    opposing_counsel = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Engagements/Accounts'

    def __str__(self):
        return f'{self.matter_title} - {self.folder}'


class DueCode(models.Model):
    SelectBasis = {
        ('In Days', 'In Days'),
        ('In Months', 'In Months'),
        ('In Years', 'In Years'),
    }

    SelectFieldBasis = {
        ('Publication Date', 'PublicationDate'),
        ('Registration Date', 'RegistrationDate'),
        ('Application Date', 'Application Date'),
        ('Priority Date', 'Priority Date'),
        ('PCT Filing Date', 'PCT Filing Date'),
        ('PCT Publication Date', 'PCT Publication Date'),
        ('Renewal Date', 'Renewal Date'),
        ('Document Date', 'Document Date'),
        ('Document Receipt Date', 'Document Receipt Date'),
        ('OA Mailing Date', 'OA Mailing Date'),
    }

    DueCode = models.CharField(max_length=20, blank=True)
    Description = models.CharField(max_length=200, blank=True)
    folder_type = models.ForeignKey(
        FolderType, on_delete=models.CASCADE, null=True, blank=True)
    apptype = models.ForeignKey(
        AppType, on_delete=models.CASCADE, null=True, blank=True)
    basisofcompute = models.CharField(
        max_length=15, choices=SelectBasis, null=True, blank=True)
    fieldbsis = models.CharField(
        max_length=30, choices=SelectFieldBasis, null=True, blank=True)
    terms = models.DecimalField(
        null=True, blank=True, max_digits=5, decimal_places=3)

    def __str__(self):
        return f'{self.DueCode} - {self.apptype} - {self.Description}'


class Applicant(models.Model):
    CATEGORY = {
        ('Corporate', 'Corporate'),
        ('Inventor', 'Inventor'),
        ('Individual', 'Individual'),
    }
    matter = models.ForeignKey(Matters, on_delete=models.CASCADE, null=True)
    applicant = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Applicants'

    def __str__(self):
        return f'{self.applicant}'


class AppDueDate(models.Model):
    matter = models.ForeignKey(Matters, on_delete=models.CASCADE, null=True)
    duecode = models.CharField(max_length=20, blank=True)
    duedate = models.DateField(null=True, blank=True)
    assignto = models.ForeignKey(
        Lawyer_Data, on_delete=models.CASCADE, null=True, blank=True)
    particulars = models.CharField(max_length=250)
    date_complied = models.DateField(null=True, blank=True)
    createdby = models.CharField(max_length=30, blank=True, null=True)
    updatedby = models.CharField(max_length=30, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)


    class Meta:
        verbose_name_plural = 'Due Dates'

    def __str__(self):
        return f'{self.matter} - {self.duedate} - {self.particulars}'


class IP_Matters(models.Model):
    STATUS = {
        ('PENDING', 'PENDING'),
        ('REGISTERED', 'REGISTERED'),
        ('CANCELLED', 'CANCELLED'),
        ('ABANDONED', 'ABANDONED'),
        ('RENEWAL', 'RENEWAL'),
        ('TRANSFERRED', 'TRANSFERRED'),
    }
    matter = models.ForeignKey(Matters, on_delete=CASCADE, null=True)
    ipo_examiner = models.CharField(max_length=100, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS, null=True, blank=True)
    certificate_no = models.CharField(max_length=30, blank=True)
    registration_date = models.DateField(null=True, blank=True)
    ipc_appno = models.CharField(max_length=25, blank=True)
    ipc_appdate = models.DateField(null=True, blank=True)
    publication_reference = models.CharField(max_length=30, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    priority_number = models.CharField(max_length=25, blank=True)
    priority_date = models.DateField(null=True, blank=True)
    priority_country_filing = models.CharField(max_length=30, blank=True)
    pct_appno = models.CharField(max_length=30, blank=True)
    pct_appdate = models.DateField(null=True, blank=True)
    pct_publication = models.CharField(max_length=30, blank=True)
    pct_pubdate = models.DateField(null=True, blank=True)
    lng_interappln = models.CharField(max_length=30, blank=True)
    lng_interpubln = models.CharField(max_length=30, blank=True)
    reason_withdrawn = models.CharField(max_length=200, blank=True)
    date_Of_PCTPriority = models.DateField(null=True, blank=True)
    copyright_number = models.CharField(max_length=30, blank=True)
    renewal_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'IP Matters'

    def __str__(self):
        return f'{self.matter}'


class CaseMatter(models.Model):
    matter = models.ForeignKey(Matters, on_delete=models.CASCADE, null=True)
    case_description = models.TextField(blank=True, null=True)
    case_theory = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Case Description/Theory'

    def __str__(self):
        return f'{self.matter} - {self.case_description}'


class CaseEvidence(models.Model):
    matter = models.ForeignKey(Matters, on_delete=models.CASCADE, null=True)
    date_submitted = DateField()
    presented_by = CharField(max_length=150)
    evidence_description = TextField(blank=True)
    evidence_image = models.ImageField(blank=True)

    class Meta:
        verbose_name_plural = 'Case Evidences'

    def __str__(self):
        return f'{self.matter} - {self.date_submitted} - {self.presented_by}'


class ClassOfGoods(models.Model):
    matter = models.ForeignKey(Matters, on_delete=models.CASCADE)
    classes = models.SmallIntegerField(null=True, blank=True)
    Goods_Descriptions = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Classification Of Goods'

    def __str__(self):
        return f'{self.matter} - {self.classes}'


class Action_Order(models.Model):
    case_type = models.ForeignKey(CaseType, on_delete=CASCADE)
    order_code = models.CharField(max_length=15)
    order_description = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Case-Type Action Orders'

    def __str__(self):
        return f'{self.case_type} - {self.order_description}'


class Order_Activity(models.Model):
    client = models.ForeignKey(Client_Data, on_delete=models.PROTECT)
    order_date = models.DateField(null=True)
    order_code = models.ForeignKey(Action_Order, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Client's Order"

    def __str__(self):
        return f'{self.client} - {self.order_date} - {self.order_code.order_description}'


class ActivityCodes(models.Model):

    TRANTYPE = {
        ('MAILSIN', 'MAILSIN'),
        ('BILLABLE', 'BILLABLE'),
    }

    foldertype = models.ForeignKey(FolderType, on_delete=models.CASCADE)
    ActivityCode = models.CharField(max_length=15, blank=True)
    TranType = models.CharField(max_length=15, choices=TRANTYPE, null=True, blank=True)
    seqorder = models.IntegerField(blank=True, null=True)
    Activity = models.CharField(max_length=250)
    bill_description = models.CharField(max_length=250, blank=True, null=True)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, null=True, blank=True)
    pesorate = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    pesoamount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.Activity} - {self.ActivityCode}'


class FilingCodes(models.Model):
    activitycode = models.ForeignKey(ActivityCodes, on_delete=models.CASCADE)
    seqorder = models.IntegerField(blank=True, null=True)
    filing = models.CharField(max_length=250, null=True, blank=True)
    filing_description = models.CharField(max_length=200, blank=False)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, null=True, blank=True)
    pesorate = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    pesoamount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.filing_description} - {self.activitycode} - {self.amount}'


class IPTaskCodes(models.Model):
    ip_app_type = models.ForeignKey(AppType, on_delete=models.PROTECT)
    task_code = models.CharField(max_length=15)
    task_description = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Task Codes"

    def __str__(self):
        return f'{self.task_code}'


class IPOExaminer(models.Model):
    examiner = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.examiner}'


class task_detail(models.Model):

    TRANTYPE = {
        ('Billable', 'Billable'),
        ('Non-Billable', 'Non-Billable'),
    }


    DOCTYPE = {
        ('Outgoing', 'Outgoing'),
        ('Incoming', 'Incoming'),
        ('Others', 'Others')
    }

    MAILTYPE = {
        ('Email', 'Email'),
        ('Mail', 'Mail'),
        ('Personal', 'Personal'),
        ('IPO', 'IPO'),
        ('Court', 'Court')

    }

    BILLSTATUS = {
        ('Billed', 'Billed'),
        ('Unbilled', 'Unbilled')
    }

    matter = models.ForeignKey(Matters, on_delete=models.CASCADE, null=True)
    tran_date = models.DateField(null=False)
    doc_type = models.CharField(
        max_length=20, choices=DOCTYPE, null=True, blank=True)
    task_code = models.ForeignKey(
        ActivityCodes, on_delete=models.CASCADE, blank=True, null=True)
    tran_type = models.CharField(
        max_length=15, choices=TRANTYPE, null=True, blank=True)
    preparedby = models.ForeignKey(
        User_Profile, on_delete=models.CASCADE, blank=True, null=True)
    lawyer = models.ForeignKey(
        Lawyer_Data, on_delete=models.CASCADE, null=True, blank=True)
    task = models.TextField(null=False, blank=False)
    spentinhrs = models.DecimalField(
        null=True, blank=True, max_digits=5, decimal_places=3)
    spentinmin = models.DecimalField(
        null=True, blank=True, max_digits=5, decimal_places=3)
    doc_date = models.DateField(null=True, blank=True)
    mailing_date = models.DateField(null=True, blank=True)
    examiner = models.ForeignKey(
        IPOExaminer, on_delete=models.PROTECT, null=True, blank=True)
    mail_type = models.CharField(
        max_length=15, choices=MAILTYPE, null=True, blank=True)
    contact_person = models.CharField(max_length=50, blank=True)
    duecode = models.ForeignKey(
        DueCode, on_delete=models.PROTECT, blank=True, null=True)
    billstatus = models.CharField(
        max_length=15, choices=BILLSTATUS, blank=True, null=True, default='Unbilled')
    createdby = models.CharField(max_length=30, blank=True, null=True)
    updatedby = models.CharField(max_length=30, blank=True, null=True)
    datemodified = models.DateTimeField(auto_now=True)
    datecreated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Tasks/Activities'

    def __str__(self):
        return f'{self.task}'


class DocumentCode(models.Model):
    document = models.CharField(max_length=150)


class MailsIn(models.Model):
    MAILTYPE = {
        ('Email', 'Email'),
        ('Mail', 'Mail'),
        ('Personal', 'Personal')
    }
    client = models.ForeignKey(Client_Data, on_delete=models.CASCADE)
    date_receipt = models.DateField()
    doc_date = models.DateField(blank=True, null=True)
    mailing_date = models.DateField(null=True, blank=True)
    examiner = models.ForeignKey(
        IPOExaminer, on_delete=models.PROTECT, null=True, blank=True)
    documentcode = models.ForeignKey(
        DocumentCode, on_delete=models.CASCADE, null=True, blank=True)
    mail_type = models.CharField(
        max_length=15, choices=MAILTYPE, null=True, blank=True)
    contact_person = models.CharField(max_length=50, blank=True)
    attentionto = models.ManyToManyField(Lawyer_Data, blank=True)
    particulars = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Mails Inward'
        ordering = ['date_receipt']

    def __str__(self):
        return f'{self.date_receipt} - {self.client}'


class MailsIn_Matters(models.Model):
    mails = ForeignKey(MailsIn, on_delete=models.CASCADE)
    matter = ForeignKey(Matters, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Mails In Matters'

    def __str__(self):
        return f'{self.mails.particulars} - {self.matter.matter_title}'


class FilingDocs(models.Model):
    Task_Detail = models.ForeignKey(
        task_detail, on_delete=models.CASCADE, null=True, blank=True)
    Description = models.CharField(max_length=200, null=True, blank=True)
    DocDate = models.DateField(null=True, blank=True)
    DocsPDF = models.FileField(
        blank=True, null=True, upload_to="Documents/%Y/%m/%D/")
    createdby = models.CharField(max_length=30, blank=True, null=True)
    updatedby = models.CharField(max_length=30, blank=True, null=True)
    datemodified = models.DateTimeField(auto_now=True)
    datecreated = models.DateTimeField(auto_now_add=True)



DUEDATESTATUS = {
    ('COMPLIED', 'COMPLIED'),
    ('LAPSED', 'LAPSED'),
}
COMPUTEBASEDON = {
    ('In Years', 'In Years'),
    ('In Months', 'In Months'),
    ('In Days', 'In Days'),

}


class inboxmessage(models.Model):
    STATUS = {
        ('READ', 'READ'),
        ('UNREAD', 'UNREAD'),
    }
    messageto = models.ForeignKey(User_Profile, on_delete=models.CASCADE)
    messagedate = models.DateField(null=True, blank=True)
    messagefrom = models.CharField(max_length=60, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    messagebox = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=15, null=True,
                              blank=True, default='UNREAD', choices=STATUS)
    see_matter = models.ForeignKey(
        Matters, on_delete=models.PROTECT, null=True, blank=True)
    updatedby = models.CharField(max_length=60, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Inbox Messages'

    def __str__(self):
        return f'{self.messagedate} - {self.subject}'


class messageattachment(models.Model):
    message = models.ForeignKey(inboxmessage, on_delete=models.PROTECT)
    description = models.CharField(max_length=150, blank=True, null=True)
    DocsPDF = models.FileField(
        blank=True, null=True, upload_to="Documents/%Y/%m/%D/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Inbox Messages Attachments'


class Alert_Messages(models.Model):
    messageto = models.ForeignKey(
        User, on_delete=PROTECT, null=True, blank=True)
    date_alert = models.DateField(blank=True, null=True)
    message_alert = models.CharField(max_length=100)
    status = models.BooleanField()
    sentby = models.ForeignKey(User_Profile, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Alert Messages'

    def __str__(self):
        return f'{self.messageto} - {self.date_alert}'


class AccountsReceivable(models.Model):
    PAYMENTTAG = (
        ('UN', 'UNPAID'),
        ('PD', 'PAID'),
        ('PP', 'PARIALLY PAID'),
        ('CN', 'CANCELLED'),
    )

    matter = models.ForeignKey(Matters, on_delete=models.PROTECT, null=True)
    bill_number = models.CharField(max_length=15)
    bill_date = models.DateField(null=True, blank=True)
    lawyer = models.ForeignKey(
        Lawyer_Data, on_delete=models.PROTECT, blank=True, null=True)
    currency = models.CharField(max_length=15, null=True, blank=True)
    pesorate = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2)
    pf_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    ofees_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    ope_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    pesoamount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)

    payment_tag = models.CharField(
        max_length=5, choices=PAYMENTTAG, null=True, blank=True)
    DocPDFs = models.FileField(upload_to='Bills/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    prepared_by = models.CharField(max_length=60)

    class Meta:
        verbose_name_plural = 'Accounts Receivable'

    def __str__(self):
        return f'{self.matter.folder.client} - {self.bill_number} - {self.matter.matter_title} - {self.bill_amount} - {self.lawyer}'


class Bills(models.Model):
    bill_number = models.ForeignKey(AccountsReceivable, on_delete=PROTECT)
    task = models.ForeignKey(
        task_detail, on_delete=models.PROTECT, blank=True, null=True)
    bill_code = models.CharField(max_length=10, blank=True)
    lawyer = models.ForeignKey(
        Lawyer_Data, on_delete=models.PROTECT, blank=True, null=True)
    particulars = models.TextField(max_length=250)
    spentinhrs = models.DecimalField(
        null=True, blank=True, max_digits=5, decimal_places=3)
    spentinmin = models.DecimalField(
        null=True, blank=True, max_digits=5, decimal_places=3)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=15, null=True, blank=True)
    pesorate = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    pesoamount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    prepared_by = models.CharField(max_length=60)

    class Meta:
        verbose_name_plural = 'Bill Details'

    def __str__(self):
        #        return f'{self.bill_number} - {self.bill_number.matter.folder.client}'
        return f'{self.bill_number}'


class OFees(models.Model):
    bill_number = models.ForeignKey(AccountsReceivable, on_delete=PROTECT)
    tran_date = models.DateField(null=True, blank=True)
    fee_code = models.CharField(max_length=10, blank=True)
    fee_particulars = CharField(max_length=200, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=15, null=True, blank=True)
    pesorate = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    pesoamount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    prepared_by = models.CharField(max_length=60)

    class Meta:
        verbose_name_plural = 'Filing Fees (Expenses)'

    def __str__(self):
        return f'{self.bill_number} - {self.bill_number.matter.folder.client}'


class OPE(models.Model):
    bill_number = models.ForeignKey(AccountsReceivable, on_delete=PROTECT)
    tran_date = models.DateField(null=True, blank=True)
    ope_code = models.CharField(max_length=10, blank=True)
    expense_details = CharField(max_length=200, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=15, null=True, blank=True)
    pesorate = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    pesoamount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    prepared_by = models.CharField(max_length=60)

    class Meta:
        verbose_name_plural = 'Expenses Details'

    def __str__(self):
        return f'{self.bill_number} - {self.bill_number.matter.folder.client}'


class BillingInstuction(models.Model):
    pass


class Payments(models.Model):
    PAYMENTFOR = (
        ('PF', 'for professional fees'),
        ('OFEE', 'For filing fees'),
        ('OPE', 'for expense fees'),
        ('Full', 'Full Payment'),
        ('Partial', 'Partial Payment')
    )
    bill_number = models.ForeignKey(AccountsReceivable, on_delete=PROTECT)
    payment_date = models.DateField(null=True, blank=True)
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_for = models.CharField(max_length=10, choices=PAYMENTFOR)
    or_number = models.CharField(max_length=15, blank=True)
    or_date = models.DateField(null=True, blank=True)
    or_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bank_details = models.CharField(max_length=150, blank=True)
    payment_reference = models.CharField(max_length=30, blank=True)
    reference_date = models.DateField(null=True, blank=True)
    Charge_details = models.CharField(max_length=30, blank=True)
    Charge_Amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=15, null=True, blank=True)
    pesorate = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    pesoamount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    prepared_by = models.CharField(max_length=60, blank=True)

    class Meta:
        verbose_name_plural = 'Payment Details'

    def __str__(self):
        return f'bill number {self.bill_number.bill_number} - Amount Paid :{self.pay_amount} - {self.bill_number.matter.matter_title}'


class TempExpenses(models.Model):

    EXPENSESTATUS = (
        ('O', 'Open'),
        ('P', 'Proforma'),
        ('B', 'Billed'),
        ('C', 'Cancelled'),
        ('W', 'Waived'),

    )

    matter = models.ForeignKey(Matters, on_delete=PROTECT, null=True)
    tran_date = models.DateField(null=True, blank=True)
    lawyer = models.ForeignKey(
        Lawyer_Data, on_delete=PROTECT, null=True, blank=True)
    exp_preparedby = models.CharField(max_length=35, blank=True, null=True)
    expense_detail = models.CharField(max_length=250)
    expense_actual_amt = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=15, null=True, blank=True)
    pesorate = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    pesoamount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=15, choices=EXPENSESTATUS, blank=True)
    chargetoclient = models.BooleanField(default=False, blank=True)
    DocPDFs = models.FileField(upload_to='Receipts/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TempBills(models.Model):

    BILLSTATUS = (
        ('O', 'Open'),
        ('P', 'Proforma'),
        ('B', 'Billed'),
        ('C', 'Cancelled'),
        ('W', 'Waived'),

    )

    matter = models.ForeignKey(Matters, on_delete=PROTECT, null=True)
    tran_date = models.DateField(null=True, blank=True)
    bill_service = models.ForeignKey(
        ActivityCodes, on_delete=PROTECT, null=True, blank=True)
    lawyer = models.ForeignKey(
        Lawyer_Data, on_delete=models.PROTECT, blank=True, null=True)
    particulars = models.TextField(max_length=250)
    spentinhrs = models.DecimalField(
        null=True, blank=True, max_digits=5, decimal_places=2)
    spentinmin = models.DecimalField(
        null=True, blank=True, max_digits=5, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=15, null=True, blank=True)
    pesorate = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    pesoamount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=15, choices=BILLSTATUS, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    prepared_by = models.CharField(max_length=60)

    class Meta:
        verbose_name_plural = 'Temporary Service Rendered'

    def __str__(self):
        return f'{self.matter} - {self.particulars} - {self.tran_date}'


class TempFilingFees(models.Model):

    FILINGSTATUS = (
        ('O', 'Open'),
        ('P', 'Proforma'),
        ('B', 'Billed'),
        ('C', 'Cancelled'),
        ('W', 'Waived'),

    )

    matter = models.ForeignKey(Matters, on_delete=PROTECT, null=True)
    tran_date = models.DateField(null=True, blank=True)
    bill_service = models.ForeignKey(
        ActivityCodes, on_delete=PROTECT, null=True, blank=True)
    lawyer = models.ForeignKey(
        Lawyer_Data, on_delete=PROTECT, null=True, blank=True)
    filing = models.CharField(max_length=250, null=True, blank=True)
    expense_detail = models.CharField(max_length=250)
    expense_actual_amt = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=15, null=True, blank=True)
    pesorate = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    pesoamount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=15, choices=FILINGSTATUS, blank=True)
    chargetoclient = models.BooleanField(default=False, blank=True)
    DocPDFs = models.FileField(upload_to='Receipts/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class awaitingdocs(models.Model):

    STATUS = (
        ('O', 'Waiting'),
        ('R', 'Received'),
        ('C', 'Cancelled'),
    )

    matter = models.ForeignKey(Matters, on_delete=PROTECT, null=True)
    tran_date = models.DateField(null=True, blank=True)
    awaiting_date = models.DateField(null=True, blank=True)
    lawyer = models.ForeignKey(
        Lawyer_Data, on_delete=PROTECT, null=True, blank=True)
    particulars = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS, blank=True)

class client_user_profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, null=True)
    client = models.ForeignKey(Client_Data, on_delete=CASCADE, null=True)
    remarks = models.CharField(max_length=200, blank=True, null=True)
    date_request = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'User Client Profile'

    def __str__(self):
        return f'{self.client}'

class client_user_activity(models.Model):
    user = models.ForeignKey(User, on_delete=PROTECT, blank=True, null=True)
    matter = models.ForeignKey(Matters, on_delete=PROTECT, null=True)
    viewdate = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'User Client View Actvities'

    def __str__(self):
        return f'{self.user}'

class inifile(models.Model):
    company = models.CharField(max_length=200)
    address = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    Contact_Number = models.CharField(max_length=100, null=True, blank=True)
    ContactPerson = models.CharField(max_length=100, null=True, blank=True)

class sysinifile(models.Model):
    company = models.CharField(max_length=200)
    address = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    Contact_Number = models.CharField(max_length=100, null=True, blank=True)
    ContactPerson = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name_plural = "System INI File"
    
    def __str__(self):
        return f'{self.company}'
