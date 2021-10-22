from django.contrib import admin
from .models import User, OTP
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','firstname', 'lastname', 'email', 'is_active', 'date_joined' ]
    
    
admin.site.register(OTP)