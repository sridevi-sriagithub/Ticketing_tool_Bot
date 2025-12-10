from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('personal_id', 'user', 'first_name', 'last_name', 'email', 'is_active')
    search_fields = ('user__username', 'first_name', 'last_name', 'email')
