from django.contrib import admin
from .models import Task,Category
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
      list_display=('task','is_completed','updated_at')
      search_fields=('task',)
admin.site.register(Task,TaskAdmin)
admin.site.register(Category)