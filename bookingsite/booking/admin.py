from django.contrib import admin
from .models import *

class OfferAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Offer, OfferAdmin)
admin.site.register(Booking)
