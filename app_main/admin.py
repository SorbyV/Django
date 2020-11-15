from django.contrib import admin
from .models import SummaryStorage, ListStorage
# Register your models here.
admin.site.register(SummaryStorage)
admin.site.register(ListStorage)