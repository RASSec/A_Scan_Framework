from django.contrib import admin

# Register your models here.
from .models import buglist


class bugadmin(admin.ModelAdmin):
    list_display = ('bugname','pub_time','update_time',)

admin.site.register(buglist,bugadmin)