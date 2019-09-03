from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Reaction

@admin.register(Reaction)
class ReactionAdmin(ImportExportModelAdmin):
    pass