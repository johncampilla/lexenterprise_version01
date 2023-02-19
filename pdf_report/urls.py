from django.urls import path
from pdf_report import views

urlpatterns = [
    path('createpdf', views.pdf_report_create_newmatter, name='report-createpdf-newmatter'),
    path('createpdf/duedatelist', views.pdf_report_create_duedatelist, name='report-createpdf-duedatelist')
]