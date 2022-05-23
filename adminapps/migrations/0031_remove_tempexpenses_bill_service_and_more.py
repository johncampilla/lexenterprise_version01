# Generated by Django 4.0.4 on 2022-05-19 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapps', '0030_tempexpenses_exp_preparedby_alter_applicant_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tempexpenses',
            name='bill_service',
        ),
        migrations.RemoveField(
            model_name='tempexpenses',
            name='exp_date',
        ),
        migrations.AlterField(
            model_name='applicant',
            name='category',
            field=models.CharField(choices=[('Individual', 'Individual'), ('Corporate', 'Corporate'), ('Inventor', 'Inventor')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='duecode',
            name='basisofcompute',
            field=models.CharField(blank=True, choices=[('In Days', 'In Days'), ('In Months', 'In Months'), ('In Years', 'In Years')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='duecode',
            name='fieldbsis',
            field=models.CharField(blank=True, choices=[('PCT Publication Date', 'PCT Publication Date'), ('PCT Filing Date', 'PCT Filing Date'), ('Application Date', 'Application Date'), ('OA Mailing Date', 'OA Mailing Date'), ('Renewal Date', 'Renewal Date'), ('Priority Date', 'Priority Date'), ('Document Receipt Date', 'Document Receipt Date'), ('Publication Date', 'PublicationDate'), ('Document Date', 'Document Date'), ('Registration Date', 'RegistrationDate')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='ip_matters',
            name='status',
            field=models.CharField(blank=True, choices=[('PENDING', 'PENDING'), ('TRANSFERRED', 'TRANSFERRED'), ('CANCELLED', 'CANCELLED'), ('ABANDONED', 'ABANDONED'), ('RENEWAL', 'RENEWAL'), ('REGISTERED', 'REGISTERED')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='mailsin',
            name='mail_type',
            field=models.CharField(blank=True, choices=[('Email', 'Email'), ('Mail', 'Mail'), ('Personal', 'Personal')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='task_detail',
            name='billstatus',
            field=models.CharField(blank=True, choices=[('Billed', 'Billed'), ('Unbilled', 'Unbilled')], default='Unbilled', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='task_detail',
            name='doc_type',
            field=models.CharField(blank=True, choices=[('Others', 'Others'), ('Outgoing', 'Outgoing'), ('Incoming', 'Incoming')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='task_detail',
            name='mail_type',
            field=models.CharField(blank=True, choices=[('Email', 'Email'), ('Mail', 'Mail'), ('Personal', 'Personal')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='task_detail',
            name='tran_type',
            field=models.CharField(blank=True, choices=[('Non-Billable', 'Non-Billable'), ('Billable', 'Billable')], max_length=15, null=True),
        ),
    ]