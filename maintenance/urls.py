from django.urls import path
from maintenance import views

app_name = 'maintenance'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('mainRegisterFailure/', views.mainRegisterFailure, name='mainRegisterFailure'),
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

]
