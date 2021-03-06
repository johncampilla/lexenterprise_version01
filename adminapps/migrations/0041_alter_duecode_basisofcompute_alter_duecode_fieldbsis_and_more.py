# Generated by Django 4.0.5 on 2022-06-17 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminapps', '0040_remove_applicant_category_applicant_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duecode',
            name='basisofcompute',
            field=models.CharField(blank=True, choices=[('In Months', 'In Months'), ('In Days', 'In Days'), ('In Years', 'In Years')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='duecode',
            name='fieldbsis',
            field=models.CharField(blank=True, choices=[('Registration Date', 'RegistrationDate'), ('Priority Date', 'Priority Date'), ('OA Mailing Date', 'OA Mailing Date'), ('Renewal Date', 'Renewal Date'), ('Publication Date', 'PublicationDate'), ('Document Receipt Date', 'Document Receipt Date'), ('PCT Filing Date', 'PCT Filing Date'), ('Application Date', 'Application Date'), ('Document Date', 'Document Date'), ('PCT Publication Date', 'PCT Publication Date')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='inboxmessage',
            name='status',
            field=models.CharField(blank=True, choices=[('READ', 'READ'), ('UNREAD', 'UNREAD')], default='UNREAD', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='ip_matters',
            name='status',
            field=models.CharField(blank=True, choices=[('ABANDONED', 'ABANDONED'), ('CANCELLED', 'CANCELLED'), ('PENDING', 'PENDING'), ('TRANSFERRED', 'TRANSFERRED'), ('REGISTERED', 'REGISTERED'), ('RENEWAL', 'RENEWAL')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='mailsin',
            name='mail_type',
            field=models.CharField(blank=True, choices=[('Personal', 'Personal'), ('Mail', 'Mail'), ('Email', 'Email')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='matters',
            name='remarks',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task_detail',
            name='billstatus',
            field=models.CharField(blank=True, choices=[('Unbilled', 'Unbilled'), ('Billed', 'Billed')], default='Unbilled', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='task_detail',
            name='doc_type',
            field=models.CharField(blank=True, choices=[('Others', 'Others'), ('Incoming', 'Incoming'), ('Outgoing', 'Outgoing')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='task_detail',
            name='mail_type',
            field=models.CharField(blank=True, choices=[('Personal', 'Personal'), ('Mail', 'Mail'), ('Email', 'Email')], max_length=15, null=True),
        ),
        migrations.CreateModel(
            name='awaitingdocs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tran_date', models.DateField(blank=True, null=True)),
                ('awaiting_date', models.DateField(blank=True, null=True)),
                ('particulars', models.CharField(blank=True, max_length=200, null=True)),
                ('lawyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='adminapps.lawyer_data')),
                ('matter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='adminapps.matters')),
            ],
        ),
    ]
