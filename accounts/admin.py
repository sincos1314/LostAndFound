from django.contrib import admin
from accounts.models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'college', 'class_name', 'gender', 'phone')
    search_fields = ('user__username', 'student_id', 'phone', 'user__email', 'college', 'class_name')