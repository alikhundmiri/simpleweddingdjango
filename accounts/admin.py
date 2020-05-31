from django.contrib import admin
from .models import accountCode,Profile

# Register your models here.
class profile_Admin(admin.ModelAdmin):
	list_display = ['user', 'phone_number', 'bio', 'chat_id', 'timestamp', 'updated']
	list_filter = ['user', 'phone_number', 'bio', 'chat_id', 'timestamp', 'updated']
	search_fields = ['user', 'phone_number', 'bio', 'chat_id', 'timestamp', 'updated']

class account_code_Admin(admin.ModelAdmin):
	list_display = ['chat_id', 'verify_code', 'timestamp', 'updated']
	list_filter = ['chat_id', 'verify_code', 'timestamp', 'updated']
	search_fields = ['chat_id', 'verify_code', 'timestamp', 'updated']


admin.site.register(Profile, profile_Admin)
admin.site.register(accountCode, account_code_Admin)

