from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.contrib.auth.models import User, Permission
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.models import ContentType


from .models import Feeling, Need, FeelingsNeedsEntry


@admin.register(Feeling)
class FeelingAdmin(admin.ModelAdmin):
    can_delete = False
    readonly_fields = ('name',)


@admin.register(Need)
class NeedAdmin(admin.ModelAdmin):
    can_delete = False


'''
classes and functions for FeelingsNeedsEntry
'''


class FeelingsNeedsEntryInline(admin.TabularInline):
    model = FeelingsNeedsEntry
    can_delete = False
    show_change_link = True
    readonly_fields = ('created_at',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 40})},
    }
    fieldsets = (
        (None, {'fields': ('created_at', 'feeling', 'need', 'notes', 'public'),
                'classes': ('collapse', 'extrapretty',)}  # collapse doesn't work for inlines
         ),
    )
    extra = 0


def make_entry_public(modeladmin, request, queryset):
    queryset.update(public=True)


make_entry_public.short_description = 'Make selected entries public'


def make_entry_private(modeladmin, request, queryset):
    queryset.update(public=False)


make_entry_private.short_description = 'Make selected entries private'


@admin.register(FeelingsNeedsEntry)
class FeelingsNeedsEntryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Person', {'fields': ('user', 'created_at')}),
        ('Entry', {'fields': ('feeling', 'need', 'notes', 'public')})
    )
    list_display = [
        'user',
        'created_at',
        'feeling',
        'need',
        'public'
    ]
    readonly_fields = [
        # 'user',
        'created_at']
    ordering = ('user', 'created_at',)
    actions = [make_entry_public, make_entry_private]

'''
Modified User admin
'''


class ExtendedUserAdmin(UserAdmin):
    inlines = [FeelingsNeedsEntryInline]
    readonly_fields = ('last_login', 'date_joined',)
    fieldsets = (
        (None, {'fields': (('username', 'date_joined', 'last_login',), 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email'),
                           'classes': ('collapse',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
                         'classes': ('collapse',)}),
        # (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)
admin.site.register(Permission)
admin.site.register(ContentType)