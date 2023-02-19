"""lexenterprise URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import viewsmatter_add_details
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from userprofile import views as user_view
from adminapps import views as main_view
from authentication import views as authenticate_view
from managing_apps import views as management
from supportstaff import views as supportstaff_view
from clientuserapps import views as clientuserapps_view
from associate_apps import views as associates
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(
        template_name='user/login.html'), name='user-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'),
         name='user-logout'),
    path('register/', authenticate_view.register_page, name='user-register'),

    # Users
    path('register/', user_view.register, name='user-register'),
    path('profile/', user_view.profile, name='user-profile'),
    path('profile/update', user_view.profile_update, name='user-update-profile'),

    # for supportstaff
    path('support/', supportstaff_view.main, name='supportstaff-home'),


    path('support/matters', supportstaff_view.matterlist,
         name='supportstaff-matterlist'),
    path('support/matters/review/<int:pk>/', supportstaff_view.matter_review,
         name='supportstaff-matter_review'),

    path('support/message/view/<int:pk>/', supportstaff_view.open_message,
         name='supportstaff-open_inboxmessage'),

    path('support/message/view_sentitems/<int:pk>/', supportstaff_view.open_sentitems,
         name='supportstaff-open_sentitems'),

    path('support/message/reply/<int:pk>/', supportstaff_view.reply_message,
         name='supportstaff-reply_inboxmessage'),

    path('support/message/mymessages/', supportstaff_view.my_messages,
         name='supportstaff-my_messages'),
    path('support/message/inward/', supportstaff_view.mails_inward,
         name='supportstaff-mails_inward'),
    path('support/message/inward/add/', supportstaff_view.mails_inward_new,
         name='supportstaff-mails_new'),

    path('support/newmail/', supportstaff_view.newmail,
         name='supportstaff-add_newmail'),



    path('support/inward/update/<int:pk>/<int:m_id>/',
         supportstaff_view.mails_inward_update, name='supportstaff-mailsinward_update'),
    path('support/matters/createtask/<int:pk>/',
         supportstaff_view.add_task, name='supportstaff-add_new_task'),
    path('support/matters/mailsin/<int:pk>/',
         supportstaff_view.add_mail, name='supportstaff-add_mail'),

    path('support/recent/activities/<int:pk>/',
         supportstaff_view.recentactivities, name='superstaff-activity-review'),
    path('support/recent/duedate/<int:pk>/',
         supportstaff_view.recentviewduedates, name='superstaff-duedate-review'),
    path('support/recent_addtask/<int:pk>/<int:m_id>/',
         supportstaff_view.recentactivities_add_task, name='superstaff-add_task'),
    path('support/recent_modify/activities/<int:pk>/<int:d_id>/',
         supportstaff_view.recent_modify_task, name='superstaff-activity-modify'),
    path('support/recent_add/documents/<int:pk>/<int:m_id>/',
         supportstaff_view.newdocumentPDF, name='superstaff-recent_adddocument'),
    path('support/viewdocs/<int:pk>/<int:m_id>/<int:t_id>/',
         supportstaff_view.view_document, name='supportstaff-view_document'),

    path('support/attach/<int:pk>/<int:m_id>/',
         supportstaff_view.attach_document, name='superstaff-attach-document'),
    path('support/inboxmessages/list/',
         supportstaff_view.list_messages, name='superstaff-list_messages'),
    path('support/alertmessages/edit/<int:pk>/',
         supportstaff_view.edit_alertmessage, name='superstaff-edit_alertmessage'),
    path('support/alertmessages/remove/<int:pk>/',
         supportstaff_view.remove_alertmessage, name='superstaff-remove_alertmessage'),
    path('support/alertmessages/new/',
         supportstaff_view.new_message, name='supportstaff-new_message'),
    path('support/alertmessages/newattachment/<int:pk>/',
         supportstaff_view.new_attachment, name='supportstaff-new_attachment'),
    path('support/alertmessages/viewattachment/<int:pk>/',
         supportstaff_view.view_attachment, name='supportstaff-open_document'),
    path('support/matters/otherinfo/<int:pk>/<str:sk>/',
         supportstaff_view.matter_otherdetails, name='supportstaff-matter-otherdetails'),
    path('support/matters/classofgoods/<int:pk>/',
         supportstaff_view.matter_classofgoods, name='supportstaff-matter-classofgoods'),
    path('associates/matters/classofgoods/<int:pk>/',
         associates.matter_classofgoods, name='associates-matter-classofgoods'),

    path('support/matters/applicant/<int:pk>/',
         supportstaff_view.add_applicant, name='supportstaff-matter-add-applicant'),
    path('associates/matters/applicant/<int:pk>/',
         associates.add_applicant, name='associates-matter-add-applicant'),

    path('support/task/addactivy/',
         supportstaff_view.add_activity, name='superstaff-add_activity'),
    path('support/replymessages/edit/<int:pk>/',
         main_view.replymessage, name='supportstaff-replymessage'),


    # for management urls
    path('management/', management.main, name='management-home'),
    path('management/view_newmatters/', management.view_new_matters,
         name='management-view-newmatters'),
    path('management/view_matters/<int:pk>/',
         management.view_matter, name='management-view-matter'),
    path('management/view_newclients/', management.view_new_clients,
         name='management-view-newclients'),
    path('management/chart_onbills', management.chartonbillings,
         name='management-chart-view-bills'),
    path('management/client/', management.clientlist, name='manage-clientlist'),
    path('management/matters/', management.matterlist, name='manage-matter-list'),

    path('management/client_matterlist/<int:pk>',
         management.clientlistmatters, name='management-clientview'),
    path('management/matter/update_client/<int:pk>/', management.matter_update_client, name='management-matterview'),

    path('management/employeelist/',
         management.lawyerlist, name='management-lawyerlist'),   
     path('mamagement/opendocument/<int:pk>/', management.open_filingdocs, name='management-documentview'),
    path('management/unpaidbills/',management.unpaidbills, name='management-unpaidbills'), 

    path('management/unpaid_details/<int:pk>/', management.unpaid_details, name='management-unpaid_details'), 

    path('management/empdetails/<int:pk>/', management.employee_detail, name='employee-detail'), 

    path('management/viewbills/', management.view_billings_details, name='management-view-billings'),

    path('management/message/mymessages/', management.my_messages,
         name='management-my_messages'),

    path('management/alertmessages/new/', management.new_message, name='management-new_message'),


    # for Main VIew  urls (adimin)
    path('sysadmin/', main_view.main, name='sysadmin-home'),
    # client url
    path('sysadmin/client/', main_view.clientlist, name='admin-client-list'),
    path('sysadmin/client/new/', main_view.cliententry, name='admin-new-client'),
    path('sysadmin/client/info/<int:pk>/',
         main_view.client_information, name='admin-client-information'),
    #path('sysadmin/client/update/<int:pk>/', main_view.client_update, name='admin-client-update'),
    path('sysadmin/client/update/<int:pk>/',
         main_view.client_modify, name='admin-client-update'),
    path('sysadmin/client/delete/<int:pk>/',
         main_view.client_delete, name='admin-client-delete'),

    path('sysadmin/folder/delete/<int:pk>/',
         main_view.folder_delete, name='admin-folder-delete'),

    # matter url
    path('sysadmin/matters/', main_view.matterlist, name='admin-matter-list'),
    path('sysadmin/users/', main_view.userlist, name='admin-user-list'),
    path('sysadmin/users/add_user/', main_view.add_user, name='admin-user-add'),

    path('sysadmin/lawyers/', main_view.lawyerlist, name='admin-lawyer-list'),
    path('sysadmin/nonlawyer/', main_view.nonlawyer, name='admin-nonlawyer-list'),
    path('sysadmin/management_user/', main_view.management, name='admin-management-list'),
    path('sysadmin/admin_user/', main_view.admin, name='admin-admin-list'),
    path('sysadmin/client_userlist/', main_view.client_userlists, name='admin-client-userlist'),

    path('sysadmin/lawyers/add_lawyer/',
         main_view.add_lawyer, name='admin-lawyer-add'),
    path('sysadmin/lawyers/edit_lawyer/<int:pk>/',
         main_view.edit_lawyer, name='admin-lawyer-edit'),
    path('sysadmin/lawyers/delete_lawyer/<int:pk>/',
         main_view.remove_lawyer, name='admin-lawyer-delete'),

    path('sysadmin/matters/removetask/<int:pk>/<int:m_id>/',
          main_view.remove_task, name='main_view-remove_task'),


    # path('sysadmin/matters/', main_view.matterlist, name='admin-matter-list'),



    path('sysadmin/newmatter/<int:pk>/<int:fd>/',
         main_view.matter_add_details, name='admin-new-matter'),
    path('sysadmin/matter/update/<int:pk>/',
         main_view.matter_update, name='admin-update-matter'),
    path('sysadmin/matter/update_client/<int:pk>/',
         main_view.matter_update_client, name='admin-update-matter_client'),
    path('sysadmin/matter/update_folder/<int:pk>/',
         main_view.matter_update_folder, name='admin-update-matter_folder'),
    path('sysadmin/matter/delete_matter/<int:pk>/',
         main_view.matter_delete, name='admin-delete-matter'),
    path('sysadmin/matter/new_mail/<int:pk>/',
         main_view.matter_newmail, name='matter_new-mail'),
    path('sysadmin/matter/new_mail_IPO/<int:pk>/',
         main_view.new_mailIPO, name='matter_new-mailIPO'),

         

    #    path('sysadmin/matter_info/add/', main_view.IPmatter_add_details, name='admin-IPmatter-details'),
    #    path('sysadmin/matter_info/update/<int:pk>/', main_view.IPmatter_edit_details, name='admin-IPmatter-edit-details'),



    # folder url
    path('sysadmin/folders/', main_view.folderlist, name='admin-folder-list'),
    path('sysadmin/newfolder/<int:pk>/',
         main_view.folderentry, name='admin-new-folder'),
    path('sysadmin/folderinfo/<int:pk>/', main_view.folder_information,
         name='admin-folder-information'),
    path('sysadmin/folder/update/<int:pk>/',
         main_view.folder_update, name='admin-folder-update'),
    path('sysadmin/client_folder/update/<int:pk>/',
         main_view.folder_update_Client, name='admin-client-folder-update'),
    path('sysadmin/folder/task/<int:pk>/',
         main_view.matter_viewtask, name='admin-matter-viewtask'),
    path('sysadmin/folder/newtask/<int:pk>/',
         main_view.taskentry, name='admin-new-task'),
    path('sysadmin/folder/modifytask/<int:pk>/<int:m_id>/',
         main_view.modifytask, name='admin-modify-task'),
    #    path('sysadmin/folder/modifytask/<int:pk>/<int:m_id>/', main_view.modifytask, name='admin-modify-task'),
    path('sysadmin/matters/modifydocs/<int:pk>/',
         main_view.update_uploaded_docs, name='admin-uploaded-docs'),
    path('sysadmin/ref/filingfees/<int:pk>/',
         main_view.entry_filingfees, name='filingfee-code'),
    path('sysadmin/message/view/<int:pk>/', main_view.open_message,
         name='open_inboxmessage'),
    path('sysadmin/alertmessages/viewattachment/<int:pk>/',
         main_view.view_attachment, name='open_document'),
    path('sysadmin/message/mymessages/', main_view.my_messages,
         name='my_messages'),
    path('sysadmin/alertmessages/new/',
         main_view.new_message, name='new_message'),
    path('sysadmin/alertmessages/newattachment/<int:pk>/',
         main_view.new_attachment, name='new_attachment'),
    path('sysadmin/message/view_sentitems/<int:pk>/', main_view.open_sentitems,
         name='open_sentitems'),
    path('sysadmin/searchdocs/',
         main_view.search_docs, name='search_docs'),
    path('sysadmin/client_searchdocs/<int:pk>',
         main_view.clientsearch_docs, name='clientsearch_docs'),

    path('sysadmin/matter_searchdocs/<int:pk>',
         main_view.mattersearch_docs, name='mattersearch_docs'),

    path('sysadmin/matter_unbilled/<int:pk>',
         main_view.matter_unbilledservices, name='matter_unbilledservices'),
    path('sysadmin/message/inward/add/', main_view.mails_inward_new,
         name='mails_inward_new'),
    path('sysadmin/matters/createtask/<int:pk>/',
         main_view.add_task, name='add_task'),



     
    path('sysadmin/client_matterlist/<int:pk>',
         main_view.clientlistmatters, name='clientlistmatters'),

    path('sysadmin/opendocument/<int:pk>/',
         main_view.open_filingdocs, name='open_filingdocs'),


    path('sysadmin/awaitingdocs/<int:pk>/',
         main_view.awaiting_docs, name='awaiting_docs'),
    path('sysadmin/newawaiting/<int:pk>/',
         main_view.newawaiting_docs, name='newawaiting_docs'),
    path('sysadmin/viewawaiting/<int:pk>/',
         main_view.awaitingdoc_view, name='awaitingdoc_view'),
    path('sysadmin/viewmatterawaiting/<int:pk>/',
         main_view.matterawaiting_docs, name='matterawaiting_docs'),
    path('sysadmin/addmatterawaiting/<int:pk>/',
         main_view.addawaitingdocs_matter, name='addawaitingdocs_matter'),

    path('sysadmin/message/view/<int:pk>/', main_view.open_message,
         name='open_message'),
         

         


    path('sysadmin/folder/newduedate/',
         main_view.DueDateEntry, name='admin-new-duedate'),
    path('sysadmin/folder/newarentry/',
         main_view.BillAREntry, name='admin-new-billARentry'),

    # AR url
    path('sysadmin/ar/list/', main_view.arview, name='admin-ar-list'),
    # Users url
    #path('staffprofile/', main_view.staffprofile, name='user-profile'),
    # Lookup url
    path('sysadmin/reflistings/', main_view.lookuplist, name='admin-lookup-list'),
    path('sysadmin/ref/country/', main_view.countryentry, name='country-code'),
    path('sysadmin/ref/industry/', main_view.industryentry, name='industry-code'),
    path('sysadmin/ref/folder/', main_view.foldertypeentry, name='folder-code'),
    path('sysadmin/ref/duecode/', main_view.duecodeentry, name='due-code'),

    path('sysadmin/ref/casetype/', main_view.casetypeentry, name='casetype-code'),
    path('sysadmin/ref/nature/', main_view.natureofcase, name='nature-code'),
    path('sysadmin/ref/entity/', main_view.entityentry, name='entity-code'),
    path('sysadmin/ref/apptype/', main_view.apptypeentry, name='apptype-code'),
    path('sysadmin/ref/matterstatus/',
         main_view.matterstatusentry, name='matterstatus-code'),

    path('sysadmin/ref/appearance/',
         main_view.appearanceentry, name='appearance-code'),
    path('sysadmin/ref/activity/',
         main_view.entry_activitycodes, name='activity-code'),

    # lookup listings
    path('sysadmin/view/country/<int:pk>/',
         main_view.editcountry, name='admin-edit-country'),
    path('sysadmin/del/country/<int:pk>/',
         main_view.removecountry, name='admin-remove-country'),
    path('sysadmin/view/industry/<int:pk>/',
         main_view.industryedit, name='admin-edit-industry'),
    path('sysadmin/del/industry/<int:pk>/',
         main_view.removeindustry, name='admin-remove-industry'),
    path('sysadmin/view/foldertype/<int:pk>/',
         main_view.editfoldertype, name='admin-edit-foldertype'),
    path('sysadmin/view/duecode/<int:pk>/',
         main_view.editduecode, name='admin-edit-duecode'),
    path('sysadmin/del/foldertype/<int:pk>/',
         main_view.removefoldertype, name='admin-remove-foldertype'),
    path('sysadmin/view/casetype/<int:pk>/',
         main_view.editcasetype, name='admin-edit-casetype'),
    path('sysadmin/del/casetype/<int:pk>/',
         main_view.removecasetype, name='admin-remove-casetype'),
    path('sysadmin/view/nature/<int:pk>/',
         main_view.editnatureofcase, name='admin-edit-nature'),
    path('sysadmin/del/nature/<int:pk>/',
         main_view.removenatureofcase, name='admin-remove-nature'),
    path('sysadmin/view/apptype/<int:pk>/',
         main_view.editapptype, name='admin-edit-apptype'),
    path('sysadmin/view/matterstatus/<int:pk>/',
         main_view.editmatterstatus, name='admin-edit-matterstatus'),

    path('sysadmin/del/apptype/<int:pk>/',
         main_view.removeapptype, name='admin-remove-apptype'),
    path('sysadmin/view/entity/<int:pk>/',
         main_view.editentity, name='admin-edit-entity'),
    path('sysadmin/del/entity/<int:pk>/',
         main_view.removeentity, name='admin-remove-entity'),
    path('sysadmin/view/appearance/<int:pk>/',
         main_view.editappearance, name='admin-edit-appearance'),
    path('sysadmin/del/appearance/<int:pk>/',
         main_view.removeappearance, name='admin-remove-appearance'),
    path('sysadmin/view/activitycode/<int:pk>/',
         main_view.edittaskcode, name='admin-edit-taskcode'),
    path('sysadmin/del/activitycode/<int:pk>/',
         main_view.removetaskcode, name='admin-remove-taskcode'),
    path('sysadmin/replymessages/edit/<int:pk>/',
         main_view.replymessage, name='admin-replymessage'),





    # for Associates urls (associates)
    path('associates/', associates.main, name='associate-home'),
    path('associates/alertmessages/', associates.alert_messages,
         name='associate-alert_messages'),
    path('associates/alertmessages/edit/<int:pk>/',
         associates.edit_alertmessage, name='associate-edit_alertmessage'),
    path('associates/replymessages/edit/<int:pk>/',
         associates.replymessage, name='associate-replymessage'),

    path('associates/alertmessages/new/',
         associates.new_message, name='associate-new_message'),
    path('associates/fileattachment/new/<int:pk>/',
         associates.message_withfile, name='associate-message_withfile'),

    path('associates/alertmessages/remove/<int:pk>/',
         associates.remove_alertmessage, name='associate-remove_alertmessage'),
    path('associates/alertmessages/status/<int:pk>/',
         associates.edit_statusmessage, name='associate-edit_statusmessage'),
    path('associates/inboxmessages/list/',
         associates.list_messages, name='associate-list_messages'),
    path('associates/message/mymessages/', associates.my_messages,
         name='associate-my_messages'),
    path('associates/ar/new/<int:m_id>/',
         associates.arentry, name='associate-ar-new'),
    path('associates/ar/edit/<int:pk>/<int:m_id>/',
         associates.modifyAR, name='associate-ar-edit'),
    path('associates/alertmessages/view/', associates.view_sentmessages,
         name='associate-view_sentmessages'),
    path('associates/mymatters/', associates.matterlist,
         name='associate-matter-list'),
    path('associates/print_mymatters/', associates.print_matterlist,
         name='print_matterlist'),

    path('associates/myclients/', associates.myclientlist,
         name='associate-myclient-list'),
    path('associates/mybills/', associates.mybillinglist,
         name='associate-mybilling-list'),
    path('associates/mybillsDetails/<int:c_id>/<int:m_id>/<int:ar_id>/',
         associates.mybillingdetail, name='associate-mybilling-details'),
    path('associates/myfolders/', associates.myfolderlist,
         name='associate-myfolder-list'),
    path('associates/myunbilled/', associates.myunbilledactivity,
         name='associate-myunbilled-activity'),
    path('associates/myunbilleddetails/', associates.unbilledactivitydetails,
         name='associate-myunbilled-activitydet'),


    path('associates/myclients/details/<int:pk>/',
         associates.myclientdetail, name='associates-view-myclient-det'),
    path('associates/myfolders/details/<int:pk>/',
         associates.myfolderdetail, name='associates-view-myfolder-det'),
    path('associates/client/fdetails/<int:pk>/',
         associates.clientfulldetail, name='client-full-details'),
    path('associates/matter/fdetails/<int:pk>/',
         associates.matterfulldetail, name='matter-full-details'),

    path('associates/mybills/', associates.billing_list,
         name='associate-billing_list'),
    path('associates/inward/', associates.mails_inward,
         name='associate-mails_inward'),
    path('associates/inward/update/<int:pk>/<int:m_id>/',
         associates.mails_inward_update, name='associate-mailsinward_update'),
    path('associates/inward/add/', associates.mails_inward_new,
         name='associate-mailsinward_new'),

    path('associates/mydocs/modify/<int:pk>/<int:m_id>/<int:t_id>/',
         associates.viewfiled_document, name='associate-viewfiled_document'),
    path('associates/matters/review/<int:pk>/',
         associates.matter_review, name='associate-matter-review'),
    path('associates/unbilled_servicesPF/<int:pk>/',
         associates.unbilled_PF, name='associate-unbilled-services_PF'),

    path('associates/matters/special/',
         associates.specialinstruction, name='special-instruction'),

    path('associates/matters/otherinfo/<int:pk>/<str:sk>/',
         associates.matter_otherdetails, name='associate-matter-otherdetails'),
    path('associates/matters/classofgoods/<int:pk>/<str:sk>/',
         associates.matter_classofgoods, name='associate-matter-clasofgoods'),
    path('associates/matters/edit/classofgood/<int:pk>/<int:cl>/',
         associates.editclassofgoods, name='admin-edit-classofgood'),

    path('associates/matters/portfolio/<int:m_id>/',
         associates.view_portfolio, name='associate-view_portfolio'),
    path('associates/matters/newtask/<int:m_id>/',
         associates.portfolio_new_task, name='associate-portfolio_new_task'),
    path('associates/porfolio/newduedates/<int:m_id>/',
         associates.duedate_entry, name='associate-portfolio_DueDateEntry'),
    path('associates/porfolio/modifyduedates/<int:pk>/<int:m_id>/',
         associates.duedate_modify, name='associate-portfolio_duedate_modify'),
    path('associates/porfolio/remove/<int:pk>/<int:m_id>/',
         associates.duedate_remove, name='associate-portfolio_duedate_remove'),

    #    path('associates/matters/newtask/<int:pk>/<int:m_id>/', associates.add_new_task, name='associate-add_new_task'),
    path('associates/matters/createtask/<int:pk>/',
         associates.add_task, name='associate-add_new_task'),
    path('associates/matters/modifytask/<int:pk>/<int:m_id>/',
         associates.modify_task, name='associate-modify_task'),
    path('associates/matters/add_exepense/<int:pk>/<int:t_id>',
         associates.add_expensedetails, name='associate-add-ope'),
    path('associates/matters/add_PF/<int:pk>/',
         associates.add_PFdetails, name='associate-add-PF'),
    path('associates/matters/add_tmpexepense/<int:pk>/',
         associates.add_tmpexpense, name='associate-add_tmpexpense'),


    path('associates/matters/removetask/<int:pk>/<int:m_id>/',
         associates.remove_task, name='associate-remove_task'),

    path('associates/matters/addduedate/<int:pk>/',
         associates.add_duedate, name='associate-add_duedate'),
    path('associates/matters/editduedate/<int:pk>/<int:m_id>/',
         associates.modify_duedate, name='associate-edit_duedate'),
    path('associates/matters/removeduedate/<int:pk>/<int:m_id>/',
         associates.remove_duedate, name='associate-remove_duedate'),

    path('associates/matters/newdocs/<int:pk>/<int:m_id>/<int:frm>/',
         associates.newdocs, name='associate-newdocs'),


    path('associates/matters/edittask/<int:m_id>/<int:t_id>/',
         associates.edit_task, name='associate-edit_task'),

    path('associates/matters/list/docs/<int:t_id>/<int:m_id>/',
         associates.list_uploaded_docs, name='associate-list_uploaded_docs'),
    path('associates/matters/modifydocs/<int:pk>/<int:m_id>/',
         associates.upload_new_docs, name='associate-update_uploaded_docs'),

    #   Associates Recent Activities
    path('associates/recent/docs/<int:pk>/',
         associates.recentviewdocs, name='recent-docs-review'),
    path('associates/recent/duedate/<int:pk>/',
         associates.recentviewduedates, name='recent-duedate-review'),
    path('associates/recent/activities/<int:pk>/',
         associates.recentactivities, name='recent-activity-review'),
    path('associates/recent_modify/activities/<int:pk>/<int:d_id>/',
         associates.recent_modify_task, name='recent-activity-modify'),
    path('associates/recent_add/documents/<int:pk>/<int:m_id>/',
         associates.newdocumentPDF, name='recent_adddocument'),
    path('associates/recent_addtask/<int:pk>/<int:m_id>/',
         associates.recentactivities_add_task, name='recent-add_task'),
    path('associates/attach/<int:pk>/<int:m_id>/',
         associates.attach_document, name='attach-document'),

    path('associates/message/view/<int:pk>/', associates.open_message,
         name='associates-open_inboxmessage'),

    path('associates/alertmessages/viewattachment/<int:pk>/',
         associates.view_attachment, name='associates-open_document'),



#    path('associates/recent_viewdocs/<int:pk>/<int:frm>/',
#         associates.recent_taskviewdocs, name='recent-tasks-docs-review'),

     path('associates/recent_viewdocs/<int:pk>/',
         associates.viewdocument, name='recent-viewdocument'),

         

    path('associates/awaitingdocs/<int:pk>/',
         associates.viewawaitingdocs, name='view_awaitingdocs'),

    path('associates/searchdocument/<int:pk>/',
         associates.accesstemplate, name='access_template'),

    path('associates/newawaitingdoc/<int:pk>/',
         associates.newawaitingdocs, name='new_awaitingdocs'),

    path('associates/docsearch/',
         associates.docsearch, name='doc_search'),

     # URL for client users

    path('client_user/', clientuserapps_view.main, name='client-home'),

    path('clientuserapps/matters/review/<int:pk>/<int:m_id>/',
         clientuserapps_view.review_task, name='clientuserapps-modify_task'),


    path('clientuserapps/matters/review/<int:pk>/',
         clientuserapps_view.matter_review, name='clientuserapps-matter-review'),

    path('clientuserapps/matters/otherinfo/<int:pk>/<str:sk>/',
         clientuserapps_view.matter_otherdetails, name='clientuserapps-matter-otherdetails'),

    path('pdf/', include('pdf_report.urls')),



    #   URL for lawyers button in the associate portal
    # query list
    path('sysadmin/output/list/', main_view.outputlist, name='output-list'),
    path('report_pdf', associates.pdf_report_create, name='duedate_list-PDF')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
