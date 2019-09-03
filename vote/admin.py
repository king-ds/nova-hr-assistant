from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Votes

@admin.register(Votes)
class VotesAdmin(ImportExportModelAdmin):
    pass