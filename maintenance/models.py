from django.db import models
from django.utils import timezone


# Locomotive model to store locomotive details
class Locomotive(models.Model):
    locomotive_id = models.CharField(max_length=50, unique=True, verbose_name="Locomotive ID")
    model = models.CharField(max_length=100, verbose_name="Locomotive Model")
    depot = models.CharField(max_length=100, verbose_name="Depot Location")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return f"{self.locomotive_id} - {self.model}"

    class Meta:
        verbose_name = "Locomotive"
        verbose_name_plural = "Locomotives"

# Base model for images to support multiple image uploads
class Image(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name="Image")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Uploaded At")

    class Meta:
        abstract = True

# Failure model to store locomotive failure details
class Failure(models.Model):
    DAMAGE_TYPES = (
        ('MECHANICAL', 'Mechanical'),
        ('ELECTRICAL', 'Electrical'),
        ('BOGIE_CHASSIS', 'Bogie and Chassis'),
        ('BRAKE', 'Brake'),
        ('CABIN_AMENITIES', 'Cabin and Amenities'),
    )

    MOVE_STATUS = (
        ('ACTIVE', 'گرم / ادامه سیر'),
        ('DEACTIVE', 'سرد'),
        ('REPAIR', 'متوقف / اعزام به تعمیرات'),
    )

    locomotive = models.ForeignKey(Locomotive, on_delete=models.CASCADE, related_name='failures', verbose_name="Locomotive")
    damage_type = models.CharField(max_length=50, choices=DAMAGE_TYPES, verbose_name="Damage Type")
    description = models.TextField(verbose_name="Failure Description")
    location = models.CharField(max_length=100, verbose_name="Failure Location")
    reported_date = models.DateField(default=timezone.now, verbose_name="Reported Date")
    reported_time = models.TimeField(default=timezone.now, verbose_name="Reported Time")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    inRepair = models.BooleanField(default=False, null=True)
    dispatch_from = models.CharField(max_length=100, blank=True, null=True, verbose_name="اعزام نیرو از")
    move_status = models.CharField(max_length=20, choices=MOVE_STATUS, default='ACTIVE', verbose_name="وضعیت حرکت")

    def __str__(self):
        return f"Failure {self.id} - {self.locomotive.locomotive_id} ({self.damage_type})"

    class Meta:
        verbose_name = "Failure"
        verbose_name_plural = "Failures"

# FailureImage model to store multiple images for a failure
class FailureImage(Image):
    failure = models.ForeignKey(Failure, on_delete=models.CASCADE, related_name='images', verbose_name="Failure")

    def __str__(self):
        return f"Image for Failure {self.failure.id}"

    class Meta:
        verbose_name = "Failure Image"
        verbose_name_plural = "Failure Images"

# Repair model to store repair details with updated fields
class Repair(models.Model):
    REPAIR_STATUS = (
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    )



    failure = models.ForeignKey(Failure, on_delete=models.CASCADE, related_name='repairs', verbose_name="Related Failure")
    title = models.CharField(max_length=200, verbose_name="Repair Title")
    start_date = models.DateField(default=timezone.now, verbose_name="Start Date")
    start_time = models.TimeField(default=timezone.now, verbose_name="Start Time")
    end_date = models.DateField(null=True, blank=True, verbose_name="End Date")
    end_time = models.TimeField(null=True, blank=True, verbose_name="End Time")
    location = models.CharField(max_length=100, verbose_name="Repair Location")
    technician = models.CharField(max_length=100, verbose_name="Technician")
    status = models.CharField(max_length=20, choices=REPAIR_STATUS, default='IN_PROGRESS', verbose_name="Repair Status")
    description = models.TextField(verbose_name="Repair Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return f"Repair {self.title} for Failure {self.failure.id}"

    class Meta:
        verbose_name = "Repair"
        verbose_name_plural = "Repairs"

# RepairImage model to store multiple images for a repair
class RepairImage(Image):
    repair = models.ForeignKey(Repair, on_delete=models.CASCADE, related_name='images', verbose_name="Repair")

    def __str__(self):
        return f"Image for Repair {self.repair.id}"

    class Meta:
        verbose_name = "Repair Image"
        verbose_name_plural = "Repair Images"

# Service model to store regular service details
class Service(models.Model):
    locomotive = models.ForeignKey(Locomotive, on_delete=models.CASCADE, related_name='services', verbose_name="Locomotive")
    checklist = models.TextField(verbose_name="Checklist Details")
    hasOil=models.BooleanField(default=False,null=True)
    serviced_date = models.DateField(default=timezone.now, verbose_name="Serviced Date")
    serviced_time = models.TimeField(default=timezone.now, verbose_name="Serviced Time")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return f"Service {self.id} - {self.locomotive.locomotive_id}"

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

# ServiceImage model to store multiple images for a service
class ServiceImage(Image):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='images', verbose_name="Service")

    def __str__(self):
        return f"Image for Service {self.service.id}"

    class Meta:
        verbose_name = "Service Image"
        verbose_name_plural = "Service Images"

# Incident model to store incident details
class Incident(models.Model):
    locomotive = models.ForeignKey(Locomotive, on_delete=models.CASCADE, related_name='incidents', verbose_name="Locomotive")
    description = models.TextField(verbose_name="Incident Description")
    incident_date = models.DateField(default=timezone.now, verbose_name="Incident Date")
    incident_time = models.TimeField(default=timezone.now, verbose_name="Incident Time")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return f"Incident {self.id} - {self.locomotive.locomotive_id}"

    class Meta:
        verbose_name = "Incident"
        verbose_name_plural = "Incidents"

# IncidentImage model to store multiple images for an incident
class IncidentImage(Image):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='images', verbose_name="Incident")

    def __str__(self):
        return f"Image for Incident {self.incident.id}"

    class Meta:
        verbose_name = "Incident Image"
        verbose_name_plural = "Incident Images"


