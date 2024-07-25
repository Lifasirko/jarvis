from django.contrib import admin

from .models import CustomUser, File, News


# from contacts.models import Contact


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'storage_limit', 'get_used_storage')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(File)
# admin.site.register(Contact)
# admin.site.register(Note)
admin.site.register(News)
