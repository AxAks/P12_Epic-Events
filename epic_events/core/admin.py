from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import Employee
from django.utils.translation import gettext_lazy as _


@admin.register(Employee)
class CustomEmployeeAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions"
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
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


admin.site.site_title = "Epic Events"
admin.site.site_header = "Epic Events Administration"
admin.site.index_title = "Home"

