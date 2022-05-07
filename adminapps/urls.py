
from django.urls import path
from . import views

urlpatterns = [
    path('adminapp/clients/', views.clientlist, name='admin-client-list'),
    path('adminapp/newclient/', views.addclient, name='admin-new-client'),
    path('adminapp/viewclient/<int:pk>/', views.client_view, name='admin-view-client'),
    path('adminapp/updateclient/<int:pk>/', views.client_update, name='admin-update-client'),
    path('adminapp/deleteclient/<int:pk>/', views.client_delete, name='admin-delete-client'),

    path('adminapp/matters/', views.matterlist, name='admin-matter-list'),
    path('adminapp/newmatter/', views.addmatter, name='admin-new-matter'),
    path('adminapp/viewmatter/<int:pk>/', views.matter_view, name='admin-view-matter'),
    path('adminapp/deletematter/<int:pk>/', views.matter_delete, name='admin-delete-matter'),
    path('adminapp/updatematter/<int:pk>/', views.matter_update, name='admin-update-matter'),
    path('adminapp/newtask/', views.add_task, name='admin-new-task'),

    path('adminapp/docs/<int:pk>/', views.docs_view, name='admin-view-docs'),
    path('adminapp/sample/', views.sample_view, name='sample'),
    path('adminapp/buttons/', views.button_view, name='admin-buttons-view'),

    path('adminapp/folders/', views.folderlist, name='admin-folder-list'),



]
