import jdatetime
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import json
from maintenance.models import Locomotive, Failure, FailureImage, Repair, RepairImage
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.db.models import Count
from django.core.exceptions import ValidationError




# Dictionary for damage type translations
DAMAGE_TYPE_LABELS = {
    'MECHANICAL': 'مکانیکی',
    'ELECTRICAL': 'برقی',
    'BOGIE_CHASSIS': 'بوژی و شاسی',
    'BRAKE': 'ترمز',
    'CABIN_AMENITIES': 'کابین و رفاهی'
}

# Dictionary for province IDs (for amCharts)
PROVINCE_IDS = {
    'تهران': 'IR-07',
    'اصفهان': 'IR-04',
    'فارس': 'IR-14',
    'خوزستان': 'IR-06',
    'مازندران': 'IR-02',
    'آذربایجان شرقی': 'IR-01',
    'آذربایجان غربی': 'IR-03',
    'کرمان': 'IR-08',
    'سیستان و بلوچستان': 'IR-11',
    'کرمانشاه': 'IR-17',
    'خراسان رضوی': 'IR-09',
    'البرز': 'IR-30',
    'قم': 'IR-26',
    'مرکزی': 'IR-00',
    'قزوین': 'IR-28',
    'گیلان': 'IR-19',
    'اردبیل': 'IR-24',
    'زنجان': 'IR-25',
    'یزد': 'IR-21',
    'هرمزگان': 'IR-23',
    'بوشهر': 'IR-18',
    'چهارمحال و بختیاری': 'IR-13',
    'خراسان جنوبی': 'IR-29',
    'خراسان شمالی': 'IR-31',
    'کهگیلویه و بویراحمد': 'IR-20',
    'گلستان': 'IR-27',
    'ایلام': 'IR-16',
    'لرستان': 'IR-15',
    'کردستان': 'IR-12',
    'همدان': 'IR-10',
    'سمنان': 'IR-05',
    # Add other provinces as needed
}

@login_required
def dashboard(request):
    # Get total counts
    total_locomotives = Locomotive.objects.count()
    total_failures = Failure.objects.count()

    # Get failure counts by damage type
    failure_by_type = Failure.objects.values('damage_type').annotate(count=Count('damage_type')).order_by('damage_type')
    failure_types = [item['damage_type'] for item in failure_by_type]
    failure_type_counts = [item['count'] for item in failure_by_type]
    failure_type_labels = [DAMAGE_TYPE_LABELS.get(item['damage_type'], item['damage_type']) for item in failure_by_type]

    # Get failure counts by locomotive
    failure_by_locomotive = Failure.objects.values('locomotive__locomotive_id').annotate(
        count=Count('locomotive')).order_by('locomotive__locomotive_id')
    locomotive_ids = [item['locomotive__locomotive_id'] for item in failure_by_locomotive]
    locomotive_counts = [item['count'] for item in failure_by_locomotive]

    # Get recent failures (last 5) and convert dates to Jalali
    recent_failures = Failure.objects.select_related('locomotive').order_by('-reported_date', '-reported_time')[:5]
    recent_failures_data = []
    for failure in recent_failures:
        # Convert Gregorian date to Jalali
        jalali_date = jdatetime.date.fromgregorian(date=failure.reported_date)
        # Get images
        images = [img.image.url for img in failure.images.all()]
        recent_failures_data.append({
            'locomotive_model': failure.locomotive.locomotive_id,  # Use model instead of locomotive_id
            'damage_type': DAMAGE_TYPE_LABELS.get(failure.damage_type, failure.damage_type),  # Ensure translation
            'location': failure.location,
            'reported_date': jalali_date.strftime("%Y/%m/%d"),
            'reported_time': failure.reported_time.strftime("%H:%M"),
            'images': json.dumps(images),  # JSON-encode images list

        })

    context = {
        'total_locomotives': total_locomotives,
        'total_failures': total_failures,
        'failure_types': json.dumps(failure_types),
        'failure_type_counts': json.dumps(failure_type_counts),
        'failure_type_labels': json.dumps(failure_type_labels),
        'locomotive_ids': json.dumps(locomotive_ids),
        'locomotive_counts': json.dumps(locomotive_counts),
        'recent_failures': recent_failures_data,
    }
    return render(request, 'maintenance/home/dashboard.html', context)

    # return render(request,'maintenance/home/index.html',context)



@login_required
def mainSelectLoco(request):

    context = {'segment': 'dashboard'}
    return render(request, 'maintenance/home/index.html',context)

@login_required
def mainRegisterFailure(request):

    context = {'segment': 'failure'}
    return render(request, 'maintenance/home/mainRegisterFailure.html', context)

@login_required
def mainRegisterFailure_submit(request):
    if request.method == 'POST':
        try:
            # Get form data from request.POST
            locomotive_id = request.POST.get('locomotiveId')
            damage_type = request.POST.get('damageType')
            description = request.POST.get('description')
            location = request.POST.get('location')
            reported_date = request.POST.get('reportedDate')  # Expected format: YYYY/MM/DD (Jalali)
            reported_time = request.POST.get('reportedTime')  # Expected format: HH:MM

            # Validate required fields
            if not all([locomotive_id, damage_type, description, location, reported_date, reported_time]):
                return JsonResponse({'status': 'error', 'message': 'همه فیلدها الزامی هستند'}, status=400)

            # Get locomotive instance
            try:
                locomotive = Locomotive.objects.get(locomotive_id=locomotive_id)
            except Locomotive.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'شناسه لکوموتیو نامعتبر است'}, status=400)

            # Validate damage type
            if damage_type not in dict(Failure.DAMAGE_TYPES).keys():
                return JsonResponse({'status': 'error', 'message': 'نوع خرابی نامعتبر است'}, status=400)

            # Convert Jalali date and time to Gregorian
            try:
                # Parse Jalali date (e.g., "1404/01/01") and time (e.g., "14:30")
                jalali_datetime = jdatetime.datetime.strptime(
                    f"{reported_date} {reported_time}",
                    "%Y/%m/%d %H:%M"
                )
                # Convert to Gregorian
                gregorian_datetime = jalali_datetime.togregorian()
                gregorian_date = gregorian_datetime.date()
                gregorian_time = gregorian_datetime.time()
            except ValueError as e:
                return JsonResponse({'status': 'error', 'message': f'فرمت تاریخ یا ساعت نامعتبر است: {str(e)}'},
                                    status=400)

            # Create Failure instance
            failure = Failure.objects.create(
                locomotive=locomotive,
                damage_type=damage_type,
                description=description,
                location=location,
                reported_date=gregorian_date,  # Store Gregorian date
                reported_time=gregorian_time,  # Store Gregorian time
                inRepair=True
            )

            # Handle image uploads
            if request.FILES.getlist('images'):
                for image in request.FILES.getlist('images'):
                    FailureImage.objects.create(failure=failure, image=image)

            return JsonResponse({'status': 'success', 'message': 'خرابی با موفقیت ثبت شد'}, status=201)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'متد درخواست نامعتبر است'}, status=405)


@login_required
def mainRegisterFailureRepair(request):

    # Get failure counts by damage type
    failure_by_type = Failure.objects.values('damage_type').annotate(count=Count('damage_type')).order_by('damage_type')
    failure_types = [item['damage_type'] for item in failure_by_type]
    failure_type_counts = [item['count'] for item in failure_by_type]
    failure_type_labels = [DAMAGE_TYPE_LABELS.get(item['damage_type'], item['damage_type']) for item in failure_by_type]

    # Get failure counts by locomotive
    failure_by_locomotive = Failure.objects.values('locomotive__locomotive_id').annotate(
        count=Count('locomotive')).order_by('locomotive__locomotive_id')
    locomotive_ids = [item['locomotive__locomotive_id'] for item in failure_by_locomotive]
    locomotive_counts = [item['count'] for item in failure_by_locomotive]

    # Get recent failures (last 5) and convert dates to Jalali
    recent_failures = Failure.objects.select_related('locomotive').order_by('-reported_date', '-reported_time')[:5]
    recent_failures_data = []
    for failure in recent_failures:
        # Convert Gregorian date to Jalali
        jalali_date = jdatetime.date.fromgregorian(date=failure.reported_date)
        # Get images
        images = [img.image.url for img in failure.images.all()]
        recent_failures_data.append({
            'locomotive_model': failure.locomotive.locomotive_id,  # Use model instead of locomotive_id
            'damage_type': DAMAGE_TYPE_LABELS.get(failure.damage_type, failure.damage_type),  # Ensure translation
            'location': failure.location,
            'reported_date': jalali_date.strftime("%Y/%m/%d"),
            'reported_time': failure.reported_time.strftime("%H:%M"),
            'images': json.dumps(images),  # JSON-encode images list
            'desc': failure.description,
            'id': failure.id
        })

    context = {
        'failure_types': json.dumps(failure_types),
        'failure_type_counts': json.dumps(failure_type_counts),
        'failure_type_labels': json.dumps(failure_type_labels),
        'locomotive_ids': json.dumps(locomotive_ids),
        'locomotive_counts': json.dumps(locomotive_counts),
        'recent_failures': recent_failures_data,
        'segment': 'repair',
    }

    return render(request, 'maintenance/home/mainRegisterFailureRepair.html', context)


@login_required
def mainRegisterFailureRepair_submit(request):
    try:
        # Extract form data
        failure_id = request.POST.get('failure_id')
        title = request.POST.get('title')
        location = request.POST.get('location')
        start_date = request.POST.get('start_date')
        start_time = request.POST.get('start_time')
        end_date = request.POST.get('end_date')
        end_time = request.POST.get('end_time')
        technician = request.POST.get('technician')
        status = request.POST.get('status')
        description = request.POST.get('description')
        images = request.FILES.getlist('images')

        # Validate required fields
        required_fields = {
            'failure_id': failure_id,
            'title': title,
            'location': location,
            'start_date': start_date,
            'start_time': start_time,
            'technician': technician,
            'status': status,
            'description': description
        }
        missing_fields = [key for key, value in required_fields.items() if not value]
        if missing_fields:
            return JsonResponse({
                'status': 'error',
                'message': f'لطفاً فیلدهای زیر را پر کنید: {", ".join(missing_fields)}'
            }, status=400)

        # Validate failure_id
        failure = get_object_or_404(Failure, id=failure_id)

        # Convert Jalali dates to Gregorian
        try:
            start_date=str(start_date).replace('/','-')
            end_date=str(end_date).replace('/','-')
            start_date_gregorian = jdatetime.datetime.strptime(start_date, '%Y-%m-%d').togregorian().date()
            end_date_gregorian = None
            if end_date:
                end_date_gregorian = jdatetime.datetime.strptime(end_date, '%Y-%m-%d').togregorian().date()
        except ValueError:
            return JsonResponse({
                'status': 'error',
                'message': 'فرمت تاریخ نامعتبر است.'
            }, status=400)

        # Validate status
        valid_statuses = [choice[0] for choice in Repair.REPAIR_STATUS]
        if status not in valid_statuses:
            return JsonResponse({
                'status': 'error',
                'message': 'وضعیت تعمیر نامعتبر است.'
            }, status=400)

        # Create Repair instance
        repair = Repair(
            failure=failure,
            title=title,
            start_date=start_date_gregorian,
            start_time=start_time,
            end_date=end_date_gregorian,
            end_time=end_time if end_time else None,
            location=location,
            technician=technician,
            status=status,
            description=description
        )
        repair.save()

        #End repair row
        if status=='COMPLETED':
            failure.inRepair=False
            failure.save()


        # Save images if provided
        for image in images:
            RepairImage.objects.create(repair=repair, image=image)

        return JsonResponse({
            'status': 'success',
            'message': 'تعمیر با موفقیت ثبت شد.'
        })

    except ValidationError as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'خطا در ثبت تعمیر: ' + str(e)
        }, status=500)


@login_required
def mainRegisterService(request):

    context = {'segment': 'service'}
    return render(request, 'maintenance/home/mainRegisterService.html', context)


@login_required
def mainRegisterCrash(request):

    context = {'segment': 'crash'}
    return render(request, 'maintenance/home/mainRegisterCrash.html', context)




