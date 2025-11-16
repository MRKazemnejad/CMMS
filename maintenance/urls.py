from django.urls import path
from maintenance import views

app_name = 'maintenance'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('mainRegisterFailure/', views.mainRegisterFailure, name='mainRegisterFailure'),
    path('mainRegisterFailure1/', views.mainRegisterFailure1, name='mainRegisterFailure1'),
    path('mainRegisterFailure_submit/', views.mainRegisterFailure_submit, name='mainRegisterFailure_submit'),
    path('mainRegisterFailureRepair/', views.mainRegisterFailureRepair, name='mainRegisterFailureRepair'),
    path('mainRegisterFailureRepair_submit/', views.mainRegisterFailureRepair_submit,
         name='mainRegisterFailureRepair_submit'),
    path('mainRegisterService/', views.mainRegisterService, name='mainRegisterService'),
    path('mainRegisterCrash/', views.mainRegisterCrash, name='mainRegisterCrash'),
    path('mainAllHistory/', views.mainAllHistory, name='mainAllHistory'),
    path('mainLocomotiveFailure/<int:locomotive_id>/', views.mainLocomotiveFailure, name='mainLocomotiveFailure'),
    path('mainGetLocomotives/', views.mainGetLocomotives, name='mainGetLocomotives'),
    path('mainDashboardFilter/', views.mainDashboardFilter, name='mainDashboardFilter'),

    path('filter/', views.smart_filter_view, name='smart_filter'),


    path('edit1/', views.edit_page1, name='edit_page1'),

    # FAILURE EDIT
    path('failure-edit/<int:failure_id>/', views.get_failure_for_edit, name='failure_edit'),
    path('failure-edit-save/', views.save_failure_edit, name='failure_edit_save'),
    path('failure-delete/<int:failure_id>/', views.delete_failure, name='delete_failure'),

    # REPAIR EDIT
    path('get-repairs/<int:failure_id>/', views.get_repairs, name='get_repairs'),
    path('get-repair-detail/<int:repair_id>/', views.get_repair_detail, name='get_repair_detail'),
    path('repair-edit-save/', views.repair_edit_save, name='repair_edit_save'),
    path('repair-delete/<int:repair_id>/', views.repair_delete, name='repair_delete'),
    path('search-failures/', views.search_failures, name='search_failures'),

    path('search-services/', views.search_services, name='search_services'),
    path('service-edit/<int:pk>/', views.service_edit_detail, name='service_edit_detail'),
    path('service-edit-save/', views.service_edit_save, name='service_edit_save'),
    path('service-delete/<int:pk>/', views.service_delete, name='service_delete'),
    path('save-service-request/', views.save_service_request, name='save_service_request'),

]
