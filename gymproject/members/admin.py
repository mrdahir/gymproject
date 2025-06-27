from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'gender', 'registration_date', 'membership_duration', 'expiry_date')
    readonly_fields = ('expiry_date',)
