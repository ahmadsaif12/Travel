from django.contrib import admin
from .models import Guide

class GuideAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'gender', 'language', 'location', 'experience', 'created_at')
    search_fields = ('name', 'email', 'location')
    list_filter = ('gender', 'language', 'location')

admin.site.register(Guide, GuideAdmin)
