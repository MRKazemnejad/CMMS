from django.db import models

class Maintenance(models.Model):
    diesel_name = models.CharField(max_length=100,null=True,verbose_name="اسم دیزل")
    failure_title = models.CharField(max_length=200,null=True, verbose_name="عنوان خرابی")
    failure_description = models.TextField(null=True,verbose_name="شرح خرابی")
    start_date = models.CharField(max_length=10,null=True, verbose_name="تاریخ شروع خرابی")  # به‌صورت کاراکتر
    end_date = models.CharField(max_length=10,null=True, verbose_name="تاریخ پایان خرابی")    # به‌صورت کاراکتر
    location = models.CharField(max_length=200,null=True, verbose_name="مکان خرابی")
    repair_description = models.TextField(null=True, verbose_name="رفع خرابی")
    officer = models.CharField(null=True,max_length=100, verbose_name="مامور خرابی")
    in_repair=models.BooleanField(default=False)

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



class ChangeParts(models.Model):
    part=models.CharField(max_length=200,null=True)
    serial=models.CharField(max_length=200,null=True)
    change_date=models.CharField(max_length=200,null=True)
    part_number=models.IntegerField(default=0,null=True)
    product_id=models.IntegerField(null=True)
    diesel=models.CharField(null=True,max_length=100)
