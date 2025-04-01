from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from base.models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'profile_image_preview')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'profile_image',
                'profile_image_preview',
                'address',
                'phone_number'
            )
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    readonly_fields = ('profile_image_preview',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    def profile_image_preview(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="100" style="border-radius: 5px;" />', obj.profile_image.url)
        return "No image"

    profile_image_preview.short_description = 'Profile Image'


admin.site.register(User, CustomUserAdmin)