from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from core.models import Employee, Department


@admin.register(Employee)
class CustomEmployeeAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("first_name", "last_name", "username",
                           "groups", "email", "phone",
                           "password1", "password2"),
            },
        ),
    )


@admin.register(Department)
class DepartmentAdmin(GroupAdmin):
    search_fields = ("name",)
    field_name = "department"


admin.site.site_title = "Epic Events"
admin.site.site_header = "Epic Events Administration"
admin.site.index_title = "Home"

admin.site.unregister(Group)
