from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ['user', 'email']  # 'email' is read-only as it is derived from 'user'
    
    list_display = ['user', 'first_name', 'last_name', 'email']
    search_fields = ['user__username', 'first_name', 'last_name']

admin.site.register(Profile, ProfileAdmin)
