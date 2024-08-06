from django.contrib import admin
from .models import Vendor, Transporter, Order

# Register your models here.
admin.site.register(Vendor)
admin.site.register(Transporter)
admin.site.register(Order)


