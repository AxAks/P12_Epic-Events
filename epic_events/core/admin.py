from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from core.models import Employee, Department, Affiliation


class AffiliationInline(admin.StackedInline):
    model = Affiliation
    can_delete = False
    verbose_name_plural = 'Affiliations'
    fk_name = 'employee'


class CustomEmployeeAdmin(UserAdmin):
    inlines = (AffiliationInline, )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("first_name", "last_name", "username", "email", "phone", "department", "password1", "password2"),
            },
        ),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomEmployeeAdmin, self).get_inline_instances(request, obj)


class DepartmentAdmin(GroupAdmin):
    search_fields = ("name",)



admin.site.register(Employee, CustomEmployeeAdmin)
admin.site.unregister(Group)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Affiliation)
