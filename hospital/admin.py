from django.contrib import admin
from .models import Order, Shopkeeper,Doctor,Patient,Appointment,PatientDischargeDetails
# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Doctor, DoctorAdmin)

class ShopkeeperAdmin(admin.ModelAdmin):
    pass
admin.site.register(Shopkeeper, ShopkeeperAdmin)

class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class OrderAdmin(admin.ModelAdmin):
    pass
admin.site.register(Order, OrderAdmin)

class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)
