from django.contrib import admin
from gmail_authentication.models import User, Department
from import_export.admin import ImportExportModelAdmin
from import_export import resources

@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    pass

@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    pass