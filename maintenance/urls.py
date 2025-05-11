from django.urls import path
from maintenance import views

app_name = 'maintenance'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('mainSelectLoco', views.mainSelectLoco, name='mainSelectLoco'),
    path('mainLocoPart/<str:loco>', views.mainLocoPart, name='mainLocoPart'),

    path('maintenance/', views.maintenance_create, name='maintenance_create'),
    path('mainRecord/', views.mainRecord, name='mainRecord'),
    # path('mainRecordFailure/', views.mainRecordFailure, name='mainRecordFailure'),
    # path('mainRecordRepair/', views.mainRecordRepair, name='mainRecordRepair'),

    path('mainDieselDetails/<str:loco>', views.mainDieselDetails, name='mainDieselDetails'),
]
