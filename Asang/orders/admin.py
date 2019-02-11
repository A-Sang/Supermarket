from django.contrib import admin

# Register your models here.
from orders.models import TranSport, Payment

admin.site.register(TranSport)
admin.site.register(Payment)