from django.http import FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from maintenance.forms import MaintenanceForm
from maintenance.models import MaintenanceImage,Maintenance,ChangeParts
import json


@login_required
def dashboard(request):
    context={'segment':'dashboard'}
    return render(request,'maintenance/home/index.html')


@login_required
def mainSelectLoco(request):
    context = {'segment': 'dashboard'}
    return render(request, 'maintenance/home/index.html')


@login_required
def mainLocoPart(request,loco):
    context = {'segment': 'dashboard','loco':loco}
    return render(request, 'maintenance/home/mainLocoPart.html',context)

@login_required
def mainLocoPartChange(request,loco):
    datas=ChangeParts.objects.filter(diesel=loco)
    fail_desc=Maintenance.objects.filter(diesel_name=loco)
    context = {'segment': 'dashboard', 'loco': loco,'datas':datas,}
    return render(request, 'maintenance/home/mainLocoPartChange.html', context)


@login_required
def mainDieselDetails(request,loco):

    datas=Maintenance.objects.filter(diesel_name=loco).values()
    context = {'segment': 'dashboard','datas':datas,'loco':loco}
    return render(request, 'maintenance/home/mainDieselDetails.html',context)


@login_required
def mainRecord(request):
    return render(request, 'maintenance/home/mainRecord.html')


@login_required
def registerFailure(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST, request.FILES)
        if form.is_valid():
            maintenance = form.save()
            image_types = json.loads(form.cleaned_data['image_types'] or '{}')
            for i, image in enumerate(request.FILES.getlist('images')):
                image_type = image_types.get(f'image_{i}', 'before')  # پیش‌فرض: قبل از تعمیر
                MaintenanceImage.objects.create(
                    maintenance=maintenance,
                    image=image,
                    image_type=image_type
                )
            return redirect('maintenance:dashboard')  # جایگزین با URL موفقیت
    else:
        form = MaintenanceForm()
    return render(request, 'maintenance/home/maintenance_form.html', {'form': form})

@login_required
def registerRepair(request):

    return render(request, 'maintenance/home/registerRepair.html')

@login_required
def electricalRepairForm(request):

    return render(request, 'maintenance/home/electricalRepairForm.html')


@login_required
def motorizedRepairForm(request):

    return render(request, 'maintenance/home/motorizedRepairForm.html')


@login_required
def dailyCheckForm(request):

    return render(request, 'maintenance/home/dailyCheckForm.html')

@login_required
def serviceList(request):

    return render(request, 'maintenance/home/serviceList.html')


@login_required
def oilTest(request):

    return render(request, 'maintenance/home/oilTest.html')

def download_file(request,id):

    response = FileResponse(open(f'maintenance/file/{id}.pdf', 'rb'))
    file_name = f'{id}.pdf'
    response['Content-Disposition'] = 'inline; filename=' + file_name
    return response






