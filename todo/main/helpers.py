import csv
from django.http import HttpResponse
class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response
    export_as_csv.short_description = "Export to csv"

    def all_complete(self,request,queryset):
        self.model.objects.all().update(completed=True)
        self.message_user(request, "All task are set as completed now")

    def all_not_complete(self,request,queryset):
        self.model.objects.all().update(completed=False)
        self.message_user(request, "All task are set as uncompleted now")