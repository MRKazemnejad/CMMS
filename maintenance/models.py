from django.db import models

class Maintenance(models.Model):
    diesel_name = models.CharField(max_length=100, verbose_name="اسم دیزل")
    failure_title = models.CharField(max_length=200, verbose_name="عنوان خرابی")
    failure_description = models.TextField(verbose_name="شرح خرابی")
    start_date = models.CharField(max_length=10, verbose_name="تاریخ شروع خرابی")  # به‌صورت کاراکتر
    end_date = models.CharField(max_length=10, verbose_name="تاریخ پایان خرابی")    # به‌صورت کاراکتر
    location = models.CharField(max_length=200, verbose_name="مکان خرابی")
    symptoms = models.TextField(verbose_name="علائم خرابی")
    officer = models.CharField(max_length=100, verbose_name="مامور خرابی")

    def __str__(self):
        return f"{self.diesel_name} - {self.failure_title}"

    class Meta:
        verbose_name = "تعمیرات"
        verbose_name_plural = "تعمیرات‌ها"

class MaintenanceImage(models.Model):
    IMAGE_TYPE_CHOICES = [
        ('before', 'قبل از تعمیر'),
        ('after', 'بعد از تعمیر'),
    ]
    maintenance = models.ForeignKey(Maintenance, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='maintenance/', verbose_name="تصویر")
    image_type = models.CharField(max_length=10, choices=IMAGE_TYPE_CHOICES, verbose_name="نوع تصویر")

    class Meta:
        verbose_name = "تصویر تعمیرات"
        verbose_name_plural = "تصاویر تعمیرات"