from django.contrib import admin
from .models import *


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['first_Name', 'last_Name', 'gender', 'national_ID']
    search_fields = ['national_ID', 'personnel_code']
    readonly_fields = ['created_at', 'updated_at']
    list_filter = ['blood_Type']

    filter_horizontal = ()
    fieldsets = ()
    ordering = ()


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_Name', 'last_Name', 'gender', 'national_ID']
    search_fields = ['national_ID', 'student_ID']
    readonly_fields = ['created_at', 'updated_at']
    list_filter = ['degree']

    filter_horizontal = ()
    fieldsets = ()
    ordering = ()


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ['number']
    search_fields = ['number']
    readonly_fields = ['created_at', 'updated_at']
    list_filter = ['phone_type']

    filter_horizontal = ()
    fieldsets = ()
    ordering = ()


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['province', 'city', 'district', 'street']
    search_fields = ['post_ID']
    readonly_fields = ['created_at', 'updated_at']
    list_filter = ['province']

    filter_horizontal = ()
    fieldsets = ()
    ordering = ()

@admin.register(EmailAddress)
class EmailAddressAdmin(admin.ModelAdmin):
    list_display = ['email', 'email_type']
    search_fields = ['email']
    readonly_fields = ['created_at', 'updated_at']
    list_filter = ['email_type']

    filter_horizontal = ()
    fieldsets = ()
    ordering = ()

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'units', 'department']
    search_fields = ['code']
    readonly_fields = ['created_at', 'updated_at']
    list_filter = ['units']

    filter_horizontal = ()
    fieldsets = ()
    ordering = ()

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'establishment_Date', 'website']
    search_fields = ['code']
    readonly_fields = ['created_at', 'updated_at']

    list_filter = ()
    filter_horizontal = ()
    fieldsets = ()
    ordering = ()


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'faculty', 'established_Date']
    search_fields = ['code']
    readonly_fields = ['created_at', 'updated_at']
    list_filter = ['faculty']

    filter_horizontal = ()
    fieldsets = ()
    ordering = ()
