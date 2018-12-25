from django.contrib import admin
from .models import product_card, journal_request, journal_supplier, income

admin.site.register(product_card)
admin.site.register(journal_request)
admin.site.register(journal_supplier)
admin.site.register(income)
# Register your models here.
