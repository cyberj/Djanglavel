from django.contrib import admin

from .models import Contact, Email


class EmailInline(admin.TabularInline):
    model = Email
    extra = 3


class ContactAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['first_name', 'last_name']}),
        ('Date information', {'fields': ['birthday'], 'classes': ['collapse']}),
    ]
    inlines = [EmailInline]
    list_display = ('first_name', 'last_name')
    search_fields = ['first_name', 'last_name']

admin.site.register(Contact, ContactAdmin)
