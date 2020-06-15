from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

admin.site.site_url = "/tickets/home"


@admin.register(User)
@admin.register(Event)
@admin.register(MainEvent)
@admin.register(Seat)
@admin.register(EachEvent)
class Admin(ImportExportModelAdmin):
    pass
