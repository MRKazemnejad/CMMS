from django.urls import path
from maintenance import views

app_name = 'maintenance'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('mainSelectLoco', views.mainSelectLoco, name='mainSelectLoco'),
    path('mainLocoPart/<str:loco>', views.mainLocoPart, name='mainLocoPart'),
    path('mainLocoPartChange/<str:loco>', views.mainLocoPartChange, name='mainLocoPartChange'),


    path('mainRecord/', views.mainRecord, name='mainRecord'),
    path('registerFailure/', views.registerFailure, name='registerFailure'),
    path('registerRepair/', views.registerRepair, name='registerRepair'),

    path('electricalRepairForm/', views.electricalRepairForm, name='electricalRepairForm'),
    path('motorizedRepairForm/', views.motorizedRepairForm, name='motorizedRepairForm'),
    path('dailyCheckForm/', views.dailyCheckForm, name='dailyCheckForm'),

    path('mainDieselDetails/<str:loco>', views.mainDieselDetails, name='mainDieselDetails'),
]
