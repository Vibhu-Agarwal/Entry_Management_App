from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from users.models import User, OfficeBranch


class CustomUserAdmin(UserAdmin):
    ordering = ('id',)
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone_number',
                    'user_type', 'office_branch', 'is_active', 'is_staff')
    list_display_links = ('id', 'first_name', 'last_name', 'email')
    list_filter = ('user_type', 'is_staff')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('avatar', 'first_name', 'last_name', 'phone_number', 'office_branch')}),
        ('User Details', {'fields': ('user_type', 'is_active', 'is_staff')}),
        # ('Permissions', {
        #     'fields': ('is_superuser', 'groups', 'user_permissions'),
        # }),
        # ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number',
                       'office_branch', 'password1', 'password2', 'user_type'),
        }),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(OfficeBranch)
