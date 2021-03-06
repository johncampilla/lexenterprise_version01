# Generated by Django 4.0.4 on 2022-05-14 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapps', '0021_activitycodes_currency_activitycodes_pesoamount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitycodes',
            name='bill_description',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='category',
            field=models.CharField(choices=[('Individual', 'Individual'), ('Inventor', 'Inventor'), ('Corporate', 'Corporate')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='duecode',
            name='basisofcompute',
            field=models.CharField(blank=True, choices=[('In Days', 'In Days'), ('In Years', 'In Years'), ('In Months', 'In Months')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='duecode',
            name='fieldbsis',
            field=models.CharField(blank=True, choices=[('OA Mailing Date', 'OA Mailing Date'), ('PCT Publication Date', 'PCT Publication Date'), ('Priority Date', 'Priority Date'), ('Registration Date', 'RegistrationDate'), ('Publication Date', 'PublicationDate'), ('Renewal Date', 'Renewal Date'), ('Application Date', 'Application Date'), ('PCT Filing Date', 'PCT Filing Date'), ('Document Receipt Date', 'Document Receipt Date'), ('Document Date', 'Document Date')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='ip_matters',
            name='status',
            field=models.CharField(blank=True, choices=[('ABANDONED', 'ABANDONED'), ('PENDING', 'PENDING'), ('REGISTERED', 'REGISTERED'), ('CANCELLED', 'CANCELLED'), ('RENEWAL', 'RENEWAL'), ('TRANSFERRED', 'TRANSFERRED')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='mailsin',
            name='mail_type',
            field=models.CharField(blank=True, choices=[('Mail', 'Mail'), ('Personal', 'Personal'), ('Email', 'Email')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='task_detail',
            name='doc_type',
            field=models.CharField(blank=True, choices=[('Others', 'Others'), ('Incoming', 'Incoming'), ('Outgoing', 'Outgoing')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='task_detail',
            name='mail_type',
            field=models.CharField(blank=True, choices=[('Mail', 'Mail'), ('Personal', 'Personal'), ('Email', 'Email')], max_length=15, null=True),
        ),
    ]
