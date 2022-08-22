from django.contrib import admin

from .models import Follow, User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'password',
    )
    search_fields = (
        'username',
        'email',
    )
    list_filter = (
        'email',
        'username'
    )
    list_per_page = 10


admin.site.register(Follow)
