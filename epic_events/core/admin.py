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
                           "groups", "is_staff", "user_permissions", "email", "phone",
                           "password1", "password2"),
            },
        ),
    )
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", 'last_name', 'email')
    search_fields = ("username", "first_name", "groups", "last_name")


admin.site.site_title = "Epic Events"
admin.site.site_header = "Epic Events Administration"
admin.site.index_title = "Home"
