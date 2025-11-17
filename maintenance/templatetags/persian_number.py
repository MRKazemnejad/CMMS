# contract/templatetags/persian_number.py

from django import template
import re
from datetime import datetime, date
from persiantools.jdatetime import JalaliDate, JalaliDateTime

register = template.Library()

@register.filter(name='persian_int')
def persian_int(value, default='—'):
    """
    تبدیل هر نوع داده عددی (str, int, float, Decimal) به فرمت فارسی با جداکننده هزارگان
    مثال‌ها:
        "1234567" → "۱٬۲۳۴٬۵۶۷"
        "1,234,567" → "۱٬۲۳۴٬۵۶۷"
        1234567 → "۱٬۲۳۴٬۵۶۷"
        "1,234.56" → "۱٬۲۳۴" (فقط بخش صحیح)
        None → "—"
    """
    if value is None or value == '':
        return default

    # تبدیل به رشته
    value_str = str(value).strip()

    # حذف همه چیز جز اعداد، نقطه و کاما
    cleaned = re.sub(r'[^\d.,]', '', value_str)

    if not cleaned:
        return default

    # حذف کاماهای داخل عدد (مثل 1,234,567)
    cleaned = cleaned.replace(',', '')

    # اگر نقطه داشت، فقط بخش صحیح رو نگه دار
    if '.' in cleaned:
        cleaned = cleaned.split('.')[0]

    try:
        num = int(cleaned)
        # قالب‌بندی با کاما
        formatted = f"{num:,}"
        # تبدیل کاما به ویرگول فارسی
        formatted = formatted.replace(',', '،')
        # تبدیل اعداد به فارسی
        persian_digits = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
        return formatted.translate(persian_digits)
    except (ValueError, OverflowError):
        return default


@register.filter(name='persian_float')
def persian_float(value, decimal_places=2, default='—'):
    if value is None or value == '':
        return default

    value_str = str(value).strip()
    cleaned = re.sub(r'[^\d.,]', '', value_str)
    if not cleaned:
        return default

    cleaned = cleaned.replace(',', '')

    try:
        num = float(cleaned)
        formatted = f"{num:,.{decimal_places}f}"
        formatted = formatted.replace(',', '،')
        persian_digits = str.maketrans('0123456789.', '۰۱۲۳۴۵۶۷۸۹٫')
        return formatted.translate(persian_digits)
    except (ValueError, OverflowError):
        return default

@register.filter(name='dateToJalali')
def dateToJalali1(edate):
    """
    Input: datetime.datetime(2023, 8, 1, 0, 0)
    Output: '۱۴۰۲/۰۵/۱۰'
    """
    if not edate or edate == datetime.min:
        return '-'

    try:
        # Accept both datetime and date
        if isinstance(edate, date) and not isinstance(edate, datetime):
            edate = datetime(edate.year, edate.month, edate.day)

        # تبدیل به جلالی
        jalali = JalaliDate.to_jalali(edate.year, edate.month, edate.day)
        jalali_str = f"{jalali.year}/{jalali.month:02d}/{jalali.day:02d}"

        # تبدیل اعداد انگلیسی به فارسی
        persian_digits = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
        return jalali_str.translate(persian_digits)

    except Exception as e:
        print(f"[dateToJalali] Error: {e}, Input: {edate}")
        return '-'