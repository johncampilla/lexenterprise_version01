# Generated by Django 4.0.4 on 2022-05-03 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapps', '0008_documentcode_ipoexaminer_mailsin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='category',
            field=models.CharField(choices=[('Corporate', 'Corporate'), ('Individual', 'Individual'), ('Inventor', 'Inventor')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='duecode',
            name='basisofcompute',
            field=models.CharField(blank=True, choices=[('In Days', 'In Days'), ('In Years', 'In Years'), ('In Months', 'In Months')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='duecode',
            name='fieldbsis',
            field=models.CharField(blank=True, choices=[('Priority Date', 'Priority Date'), ('OA Mailing Date', 'OA Mailing Date'), ('Document Date', 'Document Date'), ('Document Receipt Date', 'Document Receipt Date'), ('PCT Filing Date', 'PCT Filing Date'), ('Renewal Date', 'Renewal Date'), ('Application Date', 'Application Date'), ('Publication Date', 'PublicationDate'), ('PCT Publication Date', 'PCT Publication Date'), ('Registration Date', 'RegistrationDate')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='ip_matters',
            name='status',
            field=models.CharField(blank=True, choices=[('CANCELLED', 'CANCELLED'), ('REGISTERED', 'REGISTERED'), ('PENDING', 'PENDING'), ('TRANSFERRED', 'TRANSFERRED'), ('RENEWAL', 'RENEWAL'), ('ABANDONED', 'ABANDONED')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='mailsin',
            name='mail_type',
            field=models.CharField(blank=True, choices=[('Email', 'Email'), ('Mail', 'Mail'), ('Personal', 'Personal')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='mailsin',
            name='mailing_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
