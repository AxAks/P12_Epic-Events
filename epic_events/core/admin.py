from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import Employee, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'employee'


class CustomEmployeeAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomEmployeeAdmin, self).get_inline_instances(request, obj)


admin.site.register(Employee, CustomEmployeeAdmin)
