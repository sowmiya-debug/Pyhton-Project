from django import forms
from .models import Employee
from django.core.validators import RegexValidator


phone_validator = RegexValidator(r'^\+?\d{10,15}$', 'Enter a valid contact number.')

from django import forms
from .models import Employee

class EmployeeRegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = [
            'name', 'age', 'gender', 'contact_number',
            'address', 'emergency_contact',
            'department', 'designation', 'salary_basic_pay', 'salary_allowance'
        ]



    def clean_contact_number(self):
        contact = self.cleaned_data.get('contact_number')
        if not contact.isdigit():
            raise forms.ValidationError("Contact number must contain only digits.")
        return contact

    def clean_emergency_contact(self):
        contact = self.cleaned_data.get('emergency_contact')
        if not contact.isdigit():
            raise forms.ValidationError("Emergency contact must contain only digits.")
        return contact
from django import forms
from .models import EmployeeUpdateRequest

class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = EmployeeUpdateRequest
        fields = []