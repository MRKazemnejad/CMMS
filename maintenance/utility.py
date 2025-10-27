from persiantools.jdatetime import JalaliDate, JalaliDateTime
from django.utils import timezone
from jdatetime import datetime as jdatetime


def dateToGrgorian(pdate):

    date_change_slash = pdate.replace('/', '-')
    year = int(date_change_slash[:4])
    month = int(date_change_slash[5:7])
    day = int(date_change_slash[8:10])
    date1 = JalaliDate(year, month, day).to_gregorian()
    return date1


def dateToJalali(edate):
    per_start_date = str(JalaliDate.to_jalali(edate)).replace('-', '/')
    return per_start_date
def dateTimeToJalali(edate):

    if not edate:
        return 'N/A'
    dt = timezone.localtime(edate, timezone.get_fixed_timezone(210))  # IRST: UTC+3:30
    jalali_dt = jdatetime.fromgregorian(datetime=dt)
    return jalali_dt.strftime('%Y/%m/%d %H:%M')