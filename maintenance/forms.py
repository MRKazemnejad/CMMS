from django import forms
from maintenance.models import Maintenance

# ویجت سفارشی برای پشتیبانی از چندین فایل
class CustomMultiFileInput(forms.FileInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({'multiple': 'multiple'})

    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}
        attrs.update({'multiple': 'multiple'})
        return super().render(name, value, attrs, renderer)

class MaintenanceForm(forms.ModelForm):
    images = forms.FileField(
        widget=CustomMultiFileInput(attrs={'accept': 'image/*'}),
        required=False,
        label="تصاویر (قبل و بعد از تعمیر)"
    )
    image_types = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        label="نوع تصاویر"
    )

    class Meta:
        model = Maintenance
        fields = ['diesel_name', 'failure_title', 'failure_description', 'start_date', 'end_date', 'location', 'symptoms', 'officer', 'images', 'image_types']
        widgets = {
            'failure_description': forms.Textarea(attrs={'rows': 4}),
            'start_date': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}),
            'end_date': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}),
        }