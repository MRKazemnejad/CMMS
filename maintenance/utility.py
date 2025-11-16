from persiantools.jdatetime import JalaliDate, JalaliDateTime
from django.utils import timezone
from jdatetime import datetime as jdatetime
from datetime import datetime, date


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


def jalali_to_gregorian(jalali_str):
    if not jalali_str:
        return None
    try:
        jdate = jdatetime.strptime(jalali_str, '%Y/%m/%d')
        return jdate.togregorian()
    except:
        return None


# def dateToJalali1(edate):
#     """
#     Input: datetime.datetime(2023, 8, 1, 0, 0)
#     Output: '۱۴۰۲/۰۵/۱۰'
#     """
#     if not edate or edate == datetime.min:
#         return '-'
#
#     try:
#         # Accept both datetime and date
#         if isinstance(edate, date) and not isinstance(edate, datetime):
#             edate = datetime(edate.year, edate.month, edate.day)
#
#         # تبدیل به جلالی
#         jalali = JalaliDate.to_jalali(edate.year, edate.month, edate.day)
#         jalali_str = f"{jalali.year}/{jalali.month:02d}/{jalali.day:02d}"
#
#         # تبدیل اعداد انگلیسی به فارسی
#         persian_digits = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
#         return jalali_str.translate(persian_digits)
#
#     except Exception as e:
#         print(f"[dateToJalali] Error: {e}, Input: {edate}")
#         return '-'


# ----------------------------------------------------------------------
# Fixed: Convert Gregorian datetime → Jalali string
# ----------------------------------------------------------------------
def dateToJalali1(edate):
    """
    Input: datetime.datetime(2023, 8, 1, 0, 0)
    Output: '1402/05/10'
    """
    if not edate or edate == datetime.min:
        return '-'

    try:
        # Accept both datetime and date
        if isinstance(edate, date) and not isinstance(edate, datetime):
            edate = datetime(edate.year, edate.month, edate.day)

        jalali_str = str(JalaliDate.to_jalali(edate.year, edate.month, edate.day))
        return jalali_str.replace('-', '/')
    except Exception as e:
        print(f"[dateToJalali] Error: {e}, Input: {edate}")
        return '-'