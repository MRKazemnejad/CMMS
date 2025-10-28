import jdatetime
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import json
from maintenance.models import Locomotive, Failure, FailureImage, Repair, RepairImage,Service,Incident
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.db.models import Count
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from django.forms.models import model_to_dict
from maintenance.utility import dateToGrgorian,jalali_to_gregorian
from django.db.models import Q




# Dictionary for damage type translations
DAMAGE_TYPE_LABELS = {
    'MECHANICAL': 'مکانیکی',
    'ELECTRICAL': 'الکتریکی',
    'BOGIE_CHASSIS': 'بوژی و شاسی',
    'BRAKE': 'ترمز',
    'CABIN_AMENITIES': 'کابین'
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


    # total_locomotives = Locomotive.objects.count()
    # total_failures = Failure.objects.count()
    # recent_failures = Failure.objects.select_related('locomotive').prefetch_related('images').order_by('-reported_date',
    #                                                                                                    '-reported_time')[
    #                   :10]
    #
    # for failure in recent_failures:
    #     failure.image_urls = json.dumps([image.image.url for image in failure.images.all()])
    #     # تبدیل reported_date به شمسی
    #     if failure.reported_date:
    #         reported_date_shamsi = jdatetime.datetime.fromgregorian(date=failure.reported_date).strftime('%Y/%m/%d')
    #         failure.reported_date_shamsi = reported_date_shamsi
    #     else:
    #         failure.reported_date_shamsi = 'N/A'
    #
    # locomotives = Locomotive.objects.order_by('created_at')[:25]
    # matrix_data = []
    # for loco in locomotives:
    #     latest_failure = Failure.objects.filter(locomotive=loco).order_by('-reported_date', '-reported_time').first()
    #     status = 'COLD' if latest_failure and latest_failure.inRepair else 'HOT'
    #     matrix_data.append({
    #         'locomotive_id': loco.locomotive_id,
    #         'status': status
    #     })
    #
    # today = timezone.now()
    # today_shamsi = jdatetime.datetime.fromgregorian(datetime=today).strftime(
    #     '%Y/%m/%d')
    # failure_types = Failure.objects.values('damage_type').annotate(count=Count('id')).order_by('-count')
    # failure_type_labels = [item['damage_type'] for item in failure_types]
    # failure_type_counts = [item['count'] for item in failure_types]
    #
    # failures_by_loco = Failure.objects.values('locomotive__locomotive_id').annotate(count=Count('id')).order_by(
    #     '-count')
    # locomotive_ids = [item['locomotive__locomotive_id'] for item in failures_by_loco]
    # locomotive_counts = [item['count'] for item in failures_by_loco]
    #
    # stoppage_locomotive_ids = []
    # stoppage_durations = []
    # repairs = Repair.objects.select_related('failure__locomotive').filter(status='COMPLETED')
    # for repair in repairs:
    #     if repair.start_date and repair.start_time and repair.end_date and repair.end_time:
    #         start = datetime.combine(repair.start_date, repair.start_time)
    #         end = datetime.combine(repair.end_date, repair.end_time)
    #         duration = (end - start).total_seconds() / 3600
    #         stoppage_locomotive_ids.append(repair.failure.locomotive.locomotive_id)
    #         stoppage_durations.append(round(duration, 2))
    #
    # top_locations = Failure.objects.values('location').annotate(count=Count('id')).order_by('-count')[:20]
    # location_labels = [item['location'] for item in top_locations]
    # location_counts = [item['count'] for item in top_locations]
    #
    # context = {
    #     'total_locomotives': total_locomotives,
    #     'total_failures': total_failures,
    #     'recent_failures': recent_failures,
    #     'matrix_data': matrix_data[:5] if len(matrix_data) > 5 else matrix_data,
    #     'failure_type_labels': json.dumps(failure_type_labels, ensure_ascii=False),
    #     'failure_type_counts': json.dumps(failure_type_counts),
    #     'locomotive_ids': json.dumps(locomotive_ids, ensure_ascii=False),
    #     'locomotive_counts': json.dumps(locomotive_counts),
    #     'stoppage_locomotive_ids': json.dumps(stoppage_locomotive_ids, ensure_ascii=False),
    #     'stoppage_durations': json.dumps(stoppage_durations),
    #     'location_labels': json.dumps(location_labels, ensure_ascii=False),
    #     'location_counts': json.dumps(location_counts),
    #     'today_shamsi': today_shamsi,
    # }
    # return render(request, 'maintenance/home/dashboard.html', context)
    total_locomotives = Locomotive.objects.count()
    total_failures = Failure.objects.count()
    recent_failures = Failure.objects.select_related('locomotive').prefetch_related('images').order_by('-reported_date',
                                                                                                       '-reported_time')[
                      :10]

    # مپینگ نوع خرابی به متن فارسی (اختیاری، می‌تونی تو جاوااسکریپت هم بسازی)
    damage_type_map = {
        "MECHANICAL": "مکانیکی",
        "CABIN_AMENITIES": "امکانات کابین",
        "BOGIE_CHASSIS": "شاسی بوژی"
    }

    for failure in recent_failures:
        failure.image_urls = json.dumps([image.image.url for image in failure.images.all()])
        # تبدیل reported_date به شمسی
        if failure.reported_date:
            reported_date_shamsi = jdatetime.datetime.fromgregorian(date=failure.reported_date).strftime('%Y/%m/%d')
            failure.reported_date_shamsi = reported_date_shamsi
        else:
            failure.reported_date_shamsi = 'N/A'
        # تبدیل reported_time به فرمت 24 ساعته (HH:MM:SS)
        if failure.reported_time:
            failure.reported_time_24h = failure.reported_time.strftime('%H:%M:%S')
        else:
            failure.reported_time_24h = 'N/A'
        # اعمال مپینگ damage_type (اختیاری)
        failure.damage_type_display = damage_type_map.get(failure.damage_type, failure.damage_type)

    locomotives = Locomotive.objects.order_by('created_at')[:25]
    matrix_data = []
    for loco in locomotives:
        latest_failure = Failure.objects.filter(locomotive=loco).order_by('-reported_date', '-reported_time').first()
        status = 'COLD' if latest_failure and latest_failure.inRepair else 'HOT'
        matrix_data.append({
            'locomotive_id': loco.locomotive_id,
            'status': status
        })

    today = timezone.now()
    today_shamsi = jdatetime.datetime.fromgregorian(datetime=today).strftime(
        '%Y/%m/%d')
    failure_types = Failure.objects.values('damage_type').annotate(count=Count('id')).order_by('-count')
    failure_type_labels = [item['damage_type'] for item in failure_types]
    failure_type_counts = [item['count'] for item in failure_types]

    failures_by_loco = Failure.objects.values('locomotive__locomotive_id').annotate(count=Count('id')).order_by(
        '-count')
    locomotive_ids = [item['locomotive__locomotive_id'] for item in failures_by_loco]
    locomotive_counts = [item['count'] for item in failures_by_loco]

    stoppage_locomotive_ids = []
    stoppage_durations = []
    repairs = Repair.objects.select_related('failure__locomotive').filter(status='COMPLETED')
    for repair in repairs:
        if repair.start_date and repair.start_time and repair.end_date and repair.end_time:
            start = datetime.combine(repair.start_date, repair.start_time)
            end = datetime.combine(repair.end_date, repair.end_time)
            duration = (end - start).total_seconds() / 3600
            stoppage_locomotive_ids.append(repair.failure.locomotive.locomotive_id)
            stoppage_durations.append(round(duration, 2))

    top_locations = Failure.objects.values('location').annotate(count=Count('id')).order_by('-count')[:20]
    location_labels = [item['location'] for item in top_locations]
    location_counts = [item['count'] for item in top_locations]

    context = {
        'total_locomotives': total_locomotives,
        'total_failures': total_failures,
        'recent_failures': recent_failures,
        'matrix_data': matrix_data[:5] if len(matrix_data) > 5 else matrix_data,
        'failure_type_labels': json.dumps(failure_type_labels, ensure_ascii=False),
        'failure_type_counts': json.dumps(failure_type_counts),
        'locomotive_ids': json.dumps(locomotive_ids, ensure_ascii=False),
        'locomotive_counts': json.dumps(locomotive_counts),
        'stoppage_locomotive_ids': json.dumps(stoppage_locomotive_ids, ensure_ascii=False),
        'stoppage_durations': json.dumps(stoppage_durations),
        'location_labels': json.dumps(location_labels, ensure_ascii=False),
        'location_counts': json.dumps(location_counts),
        'today_shamsi': today_shamsi,
    }
    return render(request, 'maintenance/home/dashboard.html', context)





def mainDashboardFilter(request):

    # start_date1 = request.GET.get('start_date')
    # end_date1 = request.GET.get('end_date')
    #
    # start_date = dateToGrgorian(start_date1) if start_date1 else None
    # end_date = dateToGrgorian(end_date1) if end_date1 else None
    #
    # failures = Failure.objects.all()
    # if start_date and end_date:
    #     start = start_date
    #     end = end_date
    #     failures = failures.filter(reported_date__range=[start, end])
    # elif start_date:
    #     start = start_date
    #     failures = failures.filter(reported_date__gte=start)
    # elif end_date:
    #     end = end_date
    #     failures = failures.filter(reported_date__lte=end)
    #
    # recent_failures = failures.select_related('locomotive').prefetch_related('images').order_by('-reported_date',
    #                                                                                             '-reported_time')[:10]
    # for failure in recent_failures:
    #     failure.image_urls = json.dumps([image.image.url for image in failure.images.all()])
    #     # تبدیل reported_date به شمسی
    #     if failure.reported_date:
    #         reported_date_shamsi = jdatetime.datetime.fromgregorian(date=failure.reported_date).strftime('%Y/%m/%d')
    #         failure.reported_date_shamsi = reported_date_shamsi
    #     else:
    #         failure.reported_date_shamsi = 'N/A'
    #
    # # آماده‌سازی داده‌ها برای نمودارها
    # failure_types = failures.values('damage_type').annotate(count=Count('id')).order_by('-count')
    # failure_type_labels = [item['damage_type'] for item in failure_types]
    # failure_type_counts = [item['count'] for item in failure_types]
    #
    # failures_by_loco = failures.values('locomotive__locomotive_id').annotate(count=Count('id')).order_by('-count')
    # locomotive_ids = [item['locomotive__locomotive_id'] for item in failures_by_loco]
    # locomotive_counts = [item['count'] for item in failures_by_loco]
    #
    # stoppage_locomotive_ids = []
    # stoppage_durations = []
    # repairs = Repair.objects.select_related('failure__locomotive').filter(status='COMPLETED', failure__in=failures)
    # for repair in repairs:
    #     if repair.start_date and repair.start_time and repair.end_date and repair.end_time:
    #         start = datetime.combine(repair.start_date, repair.start_time)
    #         end = datetime.combine(repair.end_date, repair.end_time)
    #         duration = (end - start).total_seconds() / 3600
    #         stoppage_locomotive_ids.append(repair.failure.locomotive.locomotive_id)
    #         stoppage_durations.append(round(duration, 2))
    #
    # top_locations = failures.values('location').annotate(count=Count('id')).order_by('-count')[:20]
    # location_labels = [item['location'] for item in top_locations]
    # location_counts = [item['count'] for item in top_locations]
    #
    # # تبدیل recent_failures به دیکشنری با اضافه کردن reported_date_shamsi
    # recent_failures_dicts = []
    # for failure in recent_failures:
    #     failure_dict = model_to_dict(failure)
    #     failure_dict['image_urls'] = failure.image_urls  # اضافه کردن image_urls
    #     failure_dict['reported_date_shamsi'] = failure.reported_date_shamsi  # اضافه کردن تاریخ شمسی
    #     recent_failures_dicts.append(failure_dict)
    #
    # data = {
    #     'recent_failures': recent_failures_dicts,
    #     'failure_type_labels': failure_type_labels,
    #     'failure_type_counts': failure_type_counts,
    #     'locomotive_ids': locomotive_ids,
    #     'locomotive_counts': locomotive_counts,
    #     'stoppage_locomotive_ids': stoppage_locomotive_ids,
    #     'stoppage_durations': stoppage_durations,
    #     'location_labels': location_labels,
    #     'location_counts': location_counts,
    # }
    # return JsonResponse(data)

    start_date1 = request.GET.get('start_date')
    end_date1 = request.GET.get('end_date')

    start_date = dateToGrgorian(start_date1) if start_date1 else None
    end_date = dateToGrgorian(end_date1) if end_date1 else None

    failures = Failure.objects.all()
    if start_date and end_date:
        start = start_date
        end = end_date
        failures = failures.filter(reported_date__range=[start, end])
    elif start_date:
        start = start_date
        failures = failures.filter(reported_date__gte=start)
    elif end_date:
        end = end_date
        failures = failures.filter(reported_date__lte=end)

    recent_failures = failures.select_related('locomotive').prefetch_related('images').order_by('-reported_date',
                                                                                                '-reported_time')[:10]
    for failure in recent_failures:
        failure.image_urls = json.dumps([image.image.url for image in failure.images.all()])
        # تبدیل reported_date به شمسی
        if failure.reported_date:
            reported_date_shamsi = jdatetime.datetime.fromgregorian(date=failure.reported_date).strftime('%Y/%m/%d')
            failure.reported_date_shamsi = reported_date_shamsi
        else:
            failure.reported_date_shamsi = 'N/A'

    # آماده‌سازی داده‌ها برای نمودارها
    failure_types = failures.values('damage_type').annotate(count=Count('id')).order_by('-count')
    failure_type_labels = [item['damage_type'] for item in failure_types]
    failure_type_counts = [item['count'] for item in failure_types]

    failures_by_loco = failures.values('locomotive__locomotive_id').annotate(count=Count('id')).order_by('-count')
    locomotive_ids = [item['locomotive__locomotive_id'] for item in failures_by_loco]
    locomotive_counts = [item['count'] for item in failures_by_loco]

    stoppage_locomotive_ids = []
    stoppage_durations = []
    repairs = Repair.objects.select_related('failure__locomotive').filter(status='COMPLETED', failure__in=failures)
    for repair in repairs:
        if repair.start_date and repair.start_time and repair.end_date and repair.end_time:
            start = datetime.combine(repair.start_date, repair.start_time)
            end = datetime.combine(repair.end_date, repair.end_time)
            duration = (end - start).total_seconds() / 3600
            stoppage_locomotive_ids.append(repair.failure.locomotive.locomotive_id)
            stoppage_durations.append(round(duration, 2))

    top_locations = failures.values('location').annotate(count=Count('id')).order_by('-count')[:20]
    location_labels = [item['location'] for item in top_locations]
    location_counts = [item['count'] for item in top_locations]

    # تبدیل recent_failures به دیکشنری با اضافه کردن locomotive_id
    recent_failures_dicts = []
    for failure in recent_failures:
        failure_dict = model_to_dict(failure)
        failure_dict['image_urls'] = failure.image_urls  # اضافه کردن image_urls
        failure_dict['reported_date_shamsi'] = failure.reported_date_shamsi  # اضافه کردن تاریخ شمسی
        failure_dict['locomotive_id'] = failure.locomotive.locomotive_id  # اضافه کردن locomotive_id
        recent_failures_dicts.append(failure_dict)

    data = {
        'recent_failures': recent_failures_dicts,
        'failure_type_labels': failure_type_labels,
        'failure_type_counts': failure_type_counts,
        'locomotive_ids': locomotive_ids,
        'locomotive_counts': locomotive_counts,
        'stoppage_locomotive_ids': stoppage_locomotive_ids,
        'stoppage_durations': stoppage_durations,
        'location_labels': location_labels,
        'location_counts': location_counts,
    }
    return JsonResponse(data)
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
            move_status = request.POST.get('moveStatus')
            dispatch_from = request.POST.get('dispatchFrom')  # New field
            reported_date = request.POST.get('reportedDate')  # Expected format: YYYY/MM/DD (Jalali)
            reported_time = request.POST.get('reportedTime')  # Expected format: HH:MM
            print(f'{locomotive_id}-{damage_type}-{description}-{location}-{move_status}-{dispatch_from}-{reported_date}-{reported_time}')
            # Validate required fields
            if not all([locomotive_id, damage_type, description, location, move_status, reported_date, reported_time]):
                return JsonResponse({'status': 'error', 'message': 'همه فیلدهای الزامی هستند'}, status=400)

            # Get locomotive instance
            try:
                locomotive = Locomotive.objects.get(locomotive_id=locomotive_id)
            except Locomotive.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'شناسه لکوموتیو نامعتبر است'}, status=400)

            # Validate damage type
            if damage_type not in dict(Failure.DAMAGE_TYPES).keys():
                return JsonResponse({'status': 'error', 'message': 'نوع خرابی نامعتبر است'}, status=400)

            # Validate move status
            if move_status not in dict(Failure.MOVE_STATUS).keys():
                return JsonResponse({'status': 'error', 'message': 'وضعیت حرکت نامعتبر است'}, status=400)

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


            if move_status == 'ACTIVE':
                inRepair=False
            else:
                inRepair = True


            # Create Failure instance
            failure = Failure.objects.create(
                locomotive=locomotive,
                damage_type=damage_type,
                description=description,
                location=location,
                reported_date=gregorian_date,  # Store Gregorian date
                reported_time=gregorian_time,  # Store Gregorian time
                inRepair=inRepair,
                dispatch_from=dispatch_from or None,  # Handle empty dispatch_from
                move_status=move_status
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


    # Get recent failures (last 5) and convert dates to Jalali
    recent_failures = Failure.objects.filter(inRepair=True).order_by('-reported_date', '-reported_time')
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
        'recent_failures': recent_failures_data,
        'segment': 'repair',
    }

    return render(request, 'maintenance/home/mainRegisterFailureRepair.html', context)


@login_required
def mainRegisterFailureRepair_submit(request):

    if request.method == 'POST':
        try:
            # Extract form data
            failure_id = request.POST.get('failure_id')
            action_type = request.POST.get('action_type')
            title = request.POST.get('title')
            location = request.POST.get('location')
            start_date = request.POST.get('start_date')
            start_time = request.POST.get('start_time')
            end_date = request.POST.get('end_date')
            end_time = request.POST.get('end_time')
            technician = request.POST.get('technician')
            status = "COMPLETED"
            description = request.POST.get('description')
            images = request.FILES.getlist('images')

            # Log received data for debugging
            print(f"Received: failure_id={failure_id}, action_type={action_type}, title={title}, "
                  f"location={location}, start_date={start_date}, start_time={start_time}, "
                  f"end_date={end_date}, end_time={end_time}, technician={technician}, "
                  f"status={status}, description={description}")

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

            # Validate action_type
            if action_type not in ['REGISTER_REPAIR', 'COMPLETE_REPAIR']:
                return JsonResponse({
                    'status': 'error',
                    'message': 'نوع اقدام نامعتبر است.'
                }, status=400)

            # Validate failure_id
            failure = get_object_or_404(Failure, id=failure_id)

            # Convert Jalali dates to Gregorian
            try:
                start_date = str(start_date).replace('/', '-')
                end_date = str(end_date).replace('/', '-') if end_date else None
                start_date_gregorian = jdatetime.datetime.strptime(start_date, '%Y-%m-%d').togregorian().date()
                end_date_gregorian = None
                if end_date:
                    end_date_gregorian = jdatetime.datetime.strptime(end_date, '%Y-%m-%d').togregorian().date()
            except ValueError:
                return JsonResponse({
                    'status': 'error',
                    'message': 'فرمت تاریخ نامعتبر است.'
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
                description=description,

            )
            repair.save()

            # Update failure.inRepair based on action_type
            if action_type == 'REGISTER_REPAIR':
                failure.inRepair = True
            elif action_type == 'COMPLETE_REPAIR':
                failure.inRepair = False
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
            print(f"Server error: {str(e)}")  # Log server error
            return JsonResponse({
                'status': 'error',
                'message': 'خطا در ثبت تعمیر: ' + str(e)
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'متد درخواست نامعتبر است.'
    }, status=405)


@login_required
def mainRegisterService(request):

    context = {'segment': 'service'}
    return render(request, 'maintenance/home/mainRegisterService.html', context)


@login_required
def mainRegisterCrash(request):

    context = {'segment': 'crash'}
    return render(request, 'maintenance/home/mainRegisterCrash.html', context)

@login_required
def mainAllHistory(request):

    # Get all locomotives
    locomotives = Locomotive.objects.all()

    # Prepare locomotive data with failure status
    locomotives_data = []
    for locomotive in locomotives:
        has_active_failure = Failure.objects.filter(locomotive=locomotive, inRepair=True).exists()
        locomotives_data.append({
            'id': locomotive.id,
            'locomotive_id': locomotive.locomotive_id,
            'has_active_failure': has_active_failure
        })

    return render(request, 'maintenance/home/mainAllHistory.html', {
        'locomotives': locomotives_data,
        'segment':'history'
    })

@login_required
def mainLocomotiveFailure(request, locomotive_id):
    # try:
    #     # Get the specific locomotive
    #     locomotive = get_object_or_404(Locomotive, id=locomotive_id)
    #     # Get failures with related repairs and images
    #     failures = Failure.objects.filter(locomotive=locomotive).prefetch_related('images', 'repairs__images').order_by(
    #         '-reported_date')
    #
    #     # Convert data to a list of dictionaries for the template
    #     failures_data = []
    #     for failure in failures:
    #         jalali_reported_date = jdatetime.date.fromgregorian(date=failure.reported_date).strftime('%Y/%m/%d')
    #         jalali_created_at = jdatetime.datetime.fromgregorian(datetime=failure.created_at).strftime(
    #             '%Y/%m/%d %H:%M:%S')
    #         # Get image URLs for failure
    #         image_urls = [image.image.url for image in failure.images.all()]
    #         # Get repairs for this failure, ordered by start_date and start_time descending
    #         repairs = failure.repairs.all().order_by('-start_date', '-start_time')
    #         repairs_data = []
    #         for repair in repairs:
    #             repairs_data.append({
    #                 'id': repair.id,
    #                 'title': repair.title,
    #                 'location': repair.location,
    #                 'technician': repair.technician,
    #                 'start_date': jdatetime.date.fromgregorian(date=repair.start_date).strftime(
    #                     '%Y/%m/%d') if repair.start_date else '',
    #                 'start_time': repair.start_time.strftime('%H:%M:%S') if repair.start_time else '',
    #                 'end_date': jdatetime.date.fromgregorian(date=repair.end_date).strftime(
    #                     '%Y/%m/%d') if repair.end_date else '',
    #                 'end_time': repair.end_time.strftime('%H:%M:%S') if repair.end_time else '',
    #                 'status': repair.get_status_display() if hasattr(repair, 'get_status_display') else repair.status,
    #                 'description': repair.description,
    #                 'images': [image.image.url for image in repair.images.all()]
    #             })
    #         # Debug: Print repairs for this failure
    #         print(f"Failure {failure.id} Repairs:", repairs_data)
    #         failures_data.append({
    #             'id': failure.id,
    #             'locomotive': failure.locomotive,
    #             'damage_type': DAMAGE_TYPE_LABELS.get(failure.damage_type,
    #                                                   failure.get_damage_type_display() if hasattr(failure,
    #                                                                                                'get_damage_type_display') else failure.damage_type),
    #             'description': failure.description,
    #             'location': failure.location,
    #             'reported_date': jalali_reported_date,
    #             'reported_time': failure.reported_time.strftime('%H:%M:%S') if failure.reported_time else '',
    #             'created_at': jalali_created_at,
    #             'inRepair': failure.inRepair,
    #             'move_status': failure.get_move_status_display() if hasattr(failure,
    #                                                                         'get_move_status_display') else failure.move_status,
    #             'dispatch_from': failure.dispatch_from or '',
    #             'images': image_urls,
    #             'repairs': json.dumps(repairs_data, cls=DjangoJSONEncoder, ensure_ascii=False)  # Serialize to JSON
    #         })
    #
    #     # Debug: Print failures_data to check content
    #     print("Failures Data:", failures_data)
    #
    #     return render(request, 'maintenance/home/mainLocomotiveFailure.html', {
    #         'locomotive': locomotive,
    #         'failures': failures_data,
    #         'template_name': 'locomotive_failures',
    #         'segment': 'history'
    #     })
    # except Locomotive.DoesNotExist:
    #     return render(request, 'maintenance/home/mainAllHistory.html', status=404)

    try:
        # Get the specific locomotive
        locomotive = get_object_or_404(Locomotive, id=locomotive_id)

        # --- اگر پارامترهای GET وجود داشت → فیلتر فعال → برو به ویو مرکزی ---
        if request.GET:
            return smart_filter_view(request)

        # --- اگر GET خالی بود → همون کد اصلی تو (بدون تغییر) ---
        # Get failures with related repairs and images
        failures = Failure.objects.filter(locomotive=locomotive).prefetch_related('images', 'repairs__images').order_by(
            '-reported_date')

        # Convert data to a list of dictionaries for the template
        failures_data = []
        for failure in failures:
            jalali_reported_date = jdatetime.date.fromgregorian(date=failure.reported_date).strftime('%Y/%m/%d')
            jalali_created_at = jdatetime.datetime.fromgregorian(datetime=failure.created_at).strftime(
                '%Y/%m/%d %H:%M:%S')
            # Get image URLs for failure
            image_urls = [image.image.url for image in failure.images.all()]
            # Get repairs for this failure, ordered by start_date and start_time descending
            repairs = failure.repairs.all().order_by('-start_date', '-start_time')
            repairs_data = []
            for repair in repairs:
                repairs_data.append({
                    'id': repair.id,
                    'title': repair.title,
                    'location': repair.location,
                    'technician': repair.technician,
                    'start_date': jdatetime.date.fromgregorian(date=repair.start_date).strftime(
                        '%Y/%m/%d') if repair.start_date else '',
                    'start_time': repair.start_time.strftime('%H:%M:%S') if repair.start_time else '',
                    'end_date': jdatetime.date.fromgregorian(date=repair.end_date).strftime(
                        '%Y/%m/%d') if repair.end_date else '',
                    'end_time': repair.end_time.strftime('%H:%M:%S') if repair.end_time else '',
                    'status': repair.get_status_display() if hasattr(repair, 'get_status_display') else repair.status,
                    'description': repair.description,
                    'images': [image.image.url for image in repair.images.all()]
                })
            # Debug: Print repairs for this failure
            print(f"Failure {failure.id} Repairs:", repairs_data)
            failures_data.append({
                'id': failure.id,
                'locomotive': failure.locomotive,
                'damage_type': DAMAGE_TYPE_LABELS.get(failure.damage_type,
                                                      failure.get_damage_type_display() if hasattr(failure,
                                                                                                   'get_damage_type_display') else failure.damage_type),
                'description': failure.description,
                'location': failure.location,
                'reported_date': jalali_reported_date,
                'reported_time': failure.reported_time.strftime('%H:%M:%S') if failure.reported_time else '',
                'created_at': jalali_created_at,
                'inRepair': failure.inRepair,
                'move_status': failure.get_move_status_display() if hasattr(failure,
                                                                            'get_move_status_display') else failure.move_status,
                'dispatch_from': failure.dispatch_from or '',
                'images': image_urls,
                'repairs': json.dumps(repairs_data, cls=DjangoJSONEncoder, ensure_ascii=False)  # Serialize to JSON
            })

        # Debug: Print failures_data to check content
        print("Failures Data:", failures_data)

        return render(request, 'maintenance/home/mainLocomotiveFailure.html', {
            'locomotive': locomotive,
            'failures': failures_data,
            'template_name': 'locomotive_failures',
            'segment': 'history'
        })
    except Locomotive.DoesNotExist:
        return render(request, 'maintenance/home/mainAllHistory.html', status=404)


@login_required
def mainGetLocomotives(request):
    locomotives = Locomotive.objects.all().values('locomotive_id')
    locomotive_list = [{'id': loco['locomotive_id'], 'name': loco['locomotive_id']} for loco in locomotives]
    return JsonResponse({'locomotives': locomotive_list})

MODEL_MAP = {
    'failure': Failure,
    'repair': Repair,
    'service': Service,
    'incident': Incident,
    'locomotive': Locomotive,
}

SEARCH_FIELDS = {
    'failure': ['description', 'location', 'locomotive__locomotive_id','damage_type'],
    'repair': ['title', 'description', 'failure__locomotive__locomotive_id'],
    'service': ['checklist', 'locomotive__locomotive_id'],
    'incident': ['description', 'locomotive__locomotive_id'],
    'locomotive': ['locomotive_id', 'model', 'depot'],

}




def smart_filter_view(request):
    """
    Central filter view.
    - No external jdatetime import required
    - All date conversions happen inside
    """
    # --- Lazy import jdatetime inside function ---
    try:
        import jdatetime
    except ImportError:
        return render(request, 'error.html', {'msg': 'ماژول jdatetime نصب نیست.'})

    model_name = request.GET.get('model', '').strip()
    if not model_name:
        return render(request, 'error.html', {'msg': 'مدل مشخص نشده'})

    template_name = request.GET.get('template', 'base_list.html')
    view_name = request.GET.get('view', 'dashboard')
    locomotive_id = request.GET.get('locomotive_id')

    model_key = model_name.lower()
    model = MODEL_MAP.get(model_key)
    if not model:
        return render(request, 'error.html', {'msg': f'مدل {model_name} معتبر نیست'})

    # --- Initial queryset ---
    queryset = model.objects.all()

    # --- Filter by locomotive ---
    if locomotive_id and model == Failure:
        try:
            loco = Locomotive.objects.get(id=locomotive_id)
            queryset = queryset.filter(locomotive=loco)
        except (Locomotive.DoesNotExist, ValueError):
            return render(request, 'error.html', {'msg': 'لکوموتیو یافت نشد'})

    # --- Prefetch ---
    if model == Failure:
        queryset = queryset.prefetch_related('images', 'repairs__images')
    elif model == Repair:
        queryset = queryset.select_related('failure__locomotive')

    # --- Text search ---
    part = request.GET.get('part', '').strip()
    if part:
        q_objects = Q()
        for field in SEARCH_FIELDS.get(model_key, []):
            q_objects |= Q(**{f"{field}__icontains": part})
        queryset = queryset.filter(q_objects)

    # --- Date field ---
    date_field = {
        'failure': 'reported_date',
        'repair': 'start_date',
    }.get(model_key, 'created_at')

    # --- Date range filter ---
    from_date = request.GET.get('from_date', '').strip()
    if from_date:
        gd = jalali_to_gregorian(from_date)
        if gd:
            queryset = queryset.filter(**{f"{date_field}__gte": gd.date()})

    to_date = request.GET.get('to_date', '').strip()
    if to_date:
        gd = jalali_to_gregorian(to_date)
        if gd:
            queryset = queryset.filter(**{f"{date_field}__lte": gd.date()})

    # --- Order ---
    queryset = queryset.order_by(f'-{date_field}')

    # --- Prepare Failure data ---
    if model == Failure and locomotive_id:
        failures_data = []
        for failure in queryset:
            # --- Convert dates to Jalali (inside function) ---
            jalali_reported_date = jdatetime.date.fromgregorian(date=failure.reported_date).strftime('%Y/%m/%d')
            jalali_created_at = jdatetime.datetime.fromgregorian(datetime=failure.created_at).strftime('%Y/%m/%d %H:%M:%S')

            # --- Images ---
            image_urls = [img.image.url for img in failure.images.all()]

            # --- Repairs ---
            repairs_data = []
            for repair in failure.repairs.all().order_by('-start_date', '-start_time'):
                repairs_data.append({
                    'id': repair.id,
                    'title': repair.title,
                    'location': repair.location,
                    'technician': repair.technician,
                    'start_date': jdatetime.date.fromgregorian(date=repair.start_date).strftime('%Y/%m/%d') if repair.start_date else '',
                    'start_time': repair.start_time.strftime('%H:%M:%S') if repair.start_time else '',
                    'end_date': jdatetime.date.fromgregorian(date=repair.end_date).strftime('%Y/%m/%d') if repair.end_date else '',
                    'end_time': repair.end_time.strftime('%H:%M:%S') if repair.end_time else '',
                    'status': repair.get_status_display() if hasattr(repair, 'get_status_display') else repair.status,
                    'description': repair.description,
                    'images': [img.image.url for img in repair.images.all()]
                })

            # --- Persian damage type ---
            damage_type_display = DAMAGE_TYPE_LABELS.get(failure.damage_type, failure.damage_type)

            failures_data.append({
                'id': failure.id,
                'locomotive': failure.locomotive,
                'damage_type': damage_type_display,
                'description': failure.description,
                'location': failure.location,
                'reported_date': jalali_reported_date,
                'reported_time': failure.reported_time.strftime('%H:%M:%S') if failure.reported_time else '',
                'created_at': jalali_created_at,
                'inRepair': failure.inRepair,
                'move_status': failure.get_move_status_display() if hasattr(failure, 'get_move_status_display') else failure.move_status,
                'dispatch_from': failure.dispatch_from or '',
                'images': image_urls,
                'repairs': json.dumps(repairs_data, ensure_ascii=False, cls=DjangoJSONEncoder)
            })

        context = {
            'locomotive': loco,
            'failures': failures_data,
            'view_name': view_name,
            'model_name': model_name,
            'template_name': template_name,
            'segment': 'history'
        }
    else:
        context = {
            'objects': queryset,
            'view_name': view_name,
            'model_name': model_name,
            'template_name': template_name,
        }

    return render(request, template_name, context)