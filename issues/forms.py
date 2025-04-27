from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ElectricityIssue, Feedback, CustomUser

# User Registration Form
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

# Form for Issue Reporting
class ElectricityIssueForm(forms.ModelForm):
    class Meta:
        model = ElectricityIssue
        fields = ['issue_type', 'description', 'location', 'image']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your feedback...'})
        }