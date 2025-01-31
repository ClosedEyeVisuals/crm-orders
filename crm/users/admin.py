from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'is_staff'
    )
    list_editable = (
        'is_staff',
    )
    search_fields = (
        'username',
        'email'
    )


admin.site.unregister(Group)
