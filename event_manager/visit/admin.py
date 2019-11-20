from django.contrib import admin
from visit.models import Visit


class VisitAdmin(admin.ModelAdmin):
    list_display = ['id', 'visitor', 'host', 'in_time', 'out_time']
    list_per_page = 100
    list_filter = ['host']
    list_display_links = ['id', 'visitor', 'host']


admin.site.register(Visit, VisitAdmin)
