from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)

class ElectricityIssue(models.Model):
    ISSUE_TYPES = [
        ('Pole', 'Fallen/Damaged Pole'),
        ('Wire', 'Broken/Exposed Wire'),
        ('Streetlight', 'Non-Functioning Streetlight'),
        ('Transformer', 'Transformer Issue'),
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue_type = models.CharField(max_length=20, choices=ISSUE_TYPES)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='issue_images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.issue_type} - {self.status}"


class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Links feedback to user
    complaint = models.ForeignKey('ElectricityIssue', on_delete=models.CASCADE)  # Links to complaint
    message = models.TextField()  # Feedback message
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return f"Feedback from {self.user.username} on {self.complaint.title}"
