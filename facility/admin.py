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
    list_display = ('patient', 'doctor', 'room', 'bed', 'admit_date', 'status', 'length_of_stay_display')
    list_filter = ('status', 'admit_date', 'room__dept')
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 'room__room_number')
    readonly_fields = ('length_of_stay_display', 'admit_date')
    
    def length_of_stay_display(self, obj):
        return f"{obj.length_of_stay} Days"
    length_of_stay_display.short_description = 'Current Stay'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "bed":
            # Only show available beds in the dropdown when creating a new admission
            # But allow the current bed to be shown when editing
            kwargs["queryset"] = Bed.objects.filter(status=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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
    list_display = ('get_full_name', 'salary')

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Name'

    

@admin.register(StaffAssignment)
class StaffAssignmentAdmin(admin.ModelAdmin):
    list_display = ('staff', 'patient', 'assigned_date')
