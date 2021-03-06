# Generated by Django 4.0.4 on 2022-05-19 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapps', '0029_tempexpenses_exp_date_alter_duecode_basisofcompute_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempexpenses',
            name='exp_preparedby',
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='category',
            field=models.CharField(choices=[('Corporate', 'Corporate'), ('Individual', 'Individual'), ('Inventor', 'Inventor')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='duecode',
            name='fieldbsis',
            field=models.CharField(blank=True, choices=[('Document Date', 'Document Date'), ('Document Receipt Date', 'Document Receipt Date'), ('Renewal Date', 'Renewal Date'), ('Publication Date', 'PublicationDate'), ('Registration Date', 'RegistrationDate'), ('PCT Filing Date', 'PCT Filing Date'), ('OA Mailing Date', 'OA Mailing Date'), ('PCT Publication Date', 'PCT Publication Date'), ('Priority Date', 'Priority Date'), ('Application Date', 'Application Date')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='ip_matters',
            name='status',
            field=models.CharField(blank=True, choices=[('TRANSFERRED', 'TRANSFERRED'), ('REGISTERED', 'REGISTERED'), ('RENEWAL', 'RENEWAL'), ('CANCELLED', 'CANCELLED'), ('PENDING', 'PENDING'), ('ABANDONED', 'ABANDONED')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='task_detail',
            name='doc_type',
            field=models.CharField(blank=True, choices=[('Outgoing', 'Outgoing'), ('Others', 'Others'), ('Incoming', 'Incoming')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='task_detail',
            name='tran_type',
            field=models.CharField(blank=True, choices=[('Billable', 'Billable'), ('Non-Billable', 'Non-Billable')], max_length=15, null=True),
        ),
    ]
