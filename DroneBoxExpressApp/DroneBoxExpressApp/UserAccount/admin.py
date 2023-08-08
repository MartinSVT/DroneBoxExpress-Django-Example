from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from DroneBoxExpressApp.UserAccount.models import DroneBoxProfile, DroneBoxUser
from django.utils.translation import gettext_lazy as _


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
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
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )
    list_display = ("username", "email", "is_staff", "is_superuser", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email")


class DBPAdmin(admin.ModelAdmin):
    list_display = ["get_custom_name", "profile_type", "user", "date_of_birth", "total_revenue"]
    search_fields = ("first_name", "last_name")
    exclude = ["user"]
    list_filter = ("profile_type",)

    def has_add_permission(self, request):
        return False


admin.site.register(DroneBoxProfile, DBPAdmin)
admin.site.register(DroneBoxUser, CustomUserAdmin)
