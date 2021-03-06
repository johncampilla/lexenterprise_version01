# Generated by Django 4.0.4 on 2022-05-02 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapps', '0005_matters_opposing_counsel_alter_applicant_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ip_matters',
            name='renewal_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='duecode',
            name='basisofcompute',
            field=models.CharField(blank=True, choices=[('In Days', 'In Days'), ('In Months', 'In Months'), ('In Years', 'In Years')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='duecode',
            name='fieldbsis',
            field=models.CharField(blank=True, choices=[('Application Date', 'Application Date'), ('Registration Date', 'RegistrationDate'), ('Renewal Date', 'Renewal Date'), ('PCT Filing Date', 'PCT Filing Date'), ('Priority Date', 'Priority Date'), ('PCT Publication Date', 'PCT Publication Date'), ('OA Mailing Date', 'OA Mailing Date'), ('Publication Date', 'PublicationDate'), ('Document Receipt Date', 'Document Receipt Date'), ('Document Date', 'Document Date')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='ip_matters',
            name='status',
            field=models.CharField(blank=True, choices=[('REGISTERED', 'REGISTERED'), ('CANCELLED', 'CANCELLED'), ('TRANSFERRED', 'TRANSFERRED'), ('ABANDONED', 'ABANDONED'), ('RENEWAL', 'RENEWAL'), ('PENDING', 'PENDING')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='task_detail',
            name='doc_type',
            field=models.CharField(choices=[('Outgoing', 'Outgoing'), ('Incoming', 'Incoming'), ('Others', 'Others')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='tempexpenses',
            name='chargetoclient',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='tempexpenses',
            name='status',
            field=models.CharField(blank=True, choices=[('O', 'Open'), ('P', 'Paid'), ('C', 'Cancelled'), ('W', 'Waived')], max_length=15),
        ),
    ]
