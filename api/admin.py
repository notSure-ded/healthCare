from django.contrib import admin
from .models import User, Patient, Doctor, PatientDoctorMapping

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_staff', 'date_joined')
    search_fields = ('email', 'name')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'created_by__email')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'created_at')
    search_fields = ('name', 'specialization')

@admin.register(PatientDoctorMapping)
class PatientDoctorMappingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'assigned_at')
    autocomplete_fields = ['patient', 'doctor'] # Makes selection easier
