from django.contrib import admin
from .models import YourTask
from .helpers import ExportCsvMixin

is_superuser=True
@admin.register(YourTask)
class YourTaskAdmin(admin.ModelAdmin, ExportCsvMixin):
    actions = ["export_as_csv","all_complete","all_not_complete"]
    list_display=('title','created','completed')
    list_per_page = 80

