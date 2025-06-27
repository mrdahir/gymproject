from django import forms
from .models import Member
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        exclude = ['registered_by']
        fields = ['first_name','middle_name','last_name','gender','registration_date','membership_duration','age','emergency_phone','address','method_of_payment','currency','amount_paid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ in ['CheckboxInput', 'CheckboxSelectMultiple']:
                field.widget.attrs['class'] = 'form-check-input'
            elif field.widget.__class__.__name__ in ['Select', 'SelectMultiple']:
                field.widget.attrs['class'] = 'form-select'
            elif field.widget.__class__.__name__ == 'RadioSelect':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

class StaffUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'is_staff', 'is_superuser'] 