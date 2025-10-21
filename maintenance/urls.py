from django.urls import path
from maintenance import views

app_name = 'maintenance'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('mainSelectLoco/', views.mainSelectLoco, name='mainSelectLoco'),
    path('mainRegisterFailure/', views.mainRegisterFailure, name='mainRegisterFailure'),
    path('mainRegisterFailure_submit/', views.mainRegisterFailure_submit, name='mainRegisterFailure_submit'),

]
