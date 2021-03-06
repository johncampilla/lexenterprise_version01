# Generated by Django 4.0.4 on 2022-05-11 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminapps', '0020_alter_currency_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitycodes',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='adminapps.currency'),
        ),
        migrations.AddField(
            model_name='activitycodes',
            name='pesoamount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='activitycodes',
            name='pesorate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='duecode',
            name='basisofcompute',
            field=models.CharField(blank=True, choices=[('In Months', 'In Months'), ('In Years', 'In Years'), ('In Days', 'In Days')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='duecode',
            name='fieldbsis',
            field=models.CharField(blank=True, choices=[('Document Receipt Date', 'Document Receipt Date'), ('OA Mailing Date', 'OA Mailing Date'), ('Publication Date', 'PublicationDate'), ('PCT Publication Date', 'PCT Publication Date'), ('PCT Filing Date', 'PCT Filing Date'), ('Priority Date', 'Priority Date'), ('Registration Date', 'RegistrationDate'), ('Document Date', 'Document Date'), ('Renewal Date', 'Renewal Date'), ('Application Date', 'Application Date')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='ip_matters',
            name='status',
            field=models.CharField(blank=True, choices=[('CANCELLED', 'CANCELLED'), ('ABANDONED', 'ABANDONED'), ('TRANSFERRED', 'TRANSFERRED'), ('REGISTERED', 'REGISTERED'), ('PENDING', 'PENDING'), ('RENEWAL', 'RENEWAL')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='mailsin',
            name='mail_type',
            field=models.CharField(blank=True, choices=[('Mail', 'Mail'), ('Email', 'Email'), ('Personal', 'Personal')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='task_detail',
            name='billstatus',
            field=models.CharField(blank=True, choices=[('Billed', 'Billed'), ('Unbilled', 'Unbilled')], default='Unbilled', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='task_detail',
            name='mail_type',
            field=models.CharField(blank=True, choices=[('Mail', 'Mail'), ('Email', 'Email'), ('Personal', 'Personal')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='task_detail',
            name='tran_type',
            field=models.CharField(blank=True, choices=[('Billable', 'Billable'), ('Non-Billable', 'Non-Billable')], max_length=15, null=True),
        ),
    ]
