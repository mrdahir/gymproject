from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.db.models import Sum

class Member(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('zaad', 'Zaad'),
        
        ('edahab', 'Edahab'),
     
        ('bank', 'Bank'),
        
        ('cash', 'Cash'),
       
    ]

    CURRENCY_CHOICES = [
        ('usd', 'Dollar'),
        ('sls', 'Somaliland Shilling'),
    ]

    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    registration_date = models.DateField(default=timezone.now)
    membership_duration = models.PositiveSmallIntegerField(
        help_text="Duration in months (1-12)",
        choices=[(i, f"{i} month{'s' if i>1 else ''}") for i in range(1,13)]
    )
    age = models.PositiveSmallIntegerField()
    emergency_phone = models.CharField(max_length=15)
    address = models.TextField()
    registered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='registered_members')
    method_of_payment = models.CharField(
        max_length=1000,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash'
    )
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='usd')

    @property
    def expiry_date(self):
        # Compute the expiry date
        return self.registration_date + timedelta(days=30*self.membership_duration)

    def days_until_expiry(self):
        return (self.expiry_date - timezone.now().date()).days

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

def report(request):
    members = Member.objects.all()
    total_usd = members.filter(currency='usd').aggregate(total=Sum('amount_paid'))['total'] or 0
    total_sls = members.filter(currency='sls').aggregate(total=Sum('amount_paid'))['total'] or 0
    return render(request, 'members/report.html', {
        'members': members,
        'total_usd': total_usd,
        'total_sls': total_sls,
    })
