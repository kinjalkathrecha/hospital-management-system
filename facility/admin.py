from django.contrib import admin
from .models import Room, Bed, Admission, Bill, Payment, Staff, StaffAssignment

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'dept', 'type', 'room_charge','total_days')
    list_filter = ('type', 'dept')

@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ('bed_number', 'room', 'status')
    list_filter = ('status', 'room')

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'room', 'bed', 'admit_date', 'discharge_date')

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('patient', 'total_amount', 'status', 'created_at')
    list_filter = ('status',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('bill', 'total_amount', 'payment_date', 'payment_status')
    list_filter = ('payment_status',)

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_phone', 'salary')

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Name'

    def get_phone(self, obj):
        return obj.user.phone
    get_phone.short_description = 'Phone'

@admin.register(StaffAssignment)
class StaffAssignmentAdmin(admin.ModelAdmin):
    list_display = ('staff', 'patient', 'assigned_date')
