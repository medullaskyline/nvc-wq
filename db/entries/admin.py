from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import Feeling, Need, FeelingsNeedsEntry, Entry, NeedCategory, NeedLeaf, FeelingMainCategory, \
    FeelingSubCategory, FeelingLeaf


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


class EntryInline(admin.TabularInline):
    model = Entry
    can_delete = False
    readonly_fields = ('created_at',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 40})},
    }
    fieldsets = (
        (None, {'fields': ('created_at', 'feeling_main_category', 'feeling_sub_category', 'feeling', 'need_category', 'need', 'notes', 'public'),
                'classes': ('collapse', 'extrapretty',)}  # collapse doesn't work for inlines
         ),
    )
    extra = 0

"""
classes and functions for Feelings
"""


class FeelingLeafInline(admin.TabularInline):
    model = FeelingLeaf
    can_delete = False
    readonly_fields = ('feeling_main_category', 'feeling_sub_category', 'feeling_leaf')
    fieldsets = (
        (None, {'fields': ('feeling_main_category', 'feeling_sub_category', 'feeling_leaf')}),
    )
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class FeelingSubCategoryInline(admin.TabularInline):
    model = FeelingSubCategory
    can_delete = False
    readonly_fields = ('feeling_main_category', 'feeling_sub_category')
    fieldsets = (
        (None, {'fields': ('feeling_main_category',  'feeling_sub_category')}),
    )
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(FeelingMainCategory)
class FeelingMainCategoryAdmin(admin.ModelAdmin):
    list_display = ('feeling_main_categories', 'feeling_sub_categories', 'feeling_leaves',)  # 'main_feeling')
    list_display_links = ('feeling_main_categories',)
    inlines = [FeelingSubCategoryInline, FeelingLeafInline]
    readonly_fields = ['feeling_main_category']
    can_delete = False

    def feeling_main_categories(self, obj):
        return obj.name

    def feeling_sub_categories(self, obj):
        return ', '.join([sc.name for sc in obj.feelingsubcategory_set.all()])

    def feeling_leaves(self, obj):
        return ', '.join([feel.name for feel in obj.feelingleaf_set.all()])

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


'''
#classes and functions for Needs
'''


class NeedLeafInline(admin.TabularInline):
    model = NeedLeaf
    can_delete = False
    readonly_fields = ('need_category', 'need_leaf')
    fieldsets = (
        (None, {'fields': ('need_category', 'need_leaf')}),
    )
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(NeedCategory)
class NeedCategoryAdmin(admin.ModelAdmin):
    list_display = ('need_categories', 'need_leaves',)  # 'main_feeling')
    list_display_links = ('need_categories',)
    inlines = [NeedLeafInline]
    readonly_fields = ['need_category']
    can_delete = False

    def need_categories(self, obj):
        return obj.name

    def need_leaves(self, obj):
        return ', '.join([need.name for need in obj.needleaf_set.all()])

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Person', {'fields': ('user', 'created_at')}),
        ('Entry', {'fields': (
            'feeling_main_category', 'feeling_sub_category', 'feeling', 'need_category', 'need', 'notes', 'public')})
    )
    list_display = [
        'user',
        'created_at',
        'feeling_main_category',
        'feeling_sub_category',
        'feeling',
        'need_category',
        'need',
        'public',
    ]
    readonly_fields = [
        'created_at']
    ordering = ('user', 'created_at',)
    actions = [make_entry_public, make_entry_private]



'''
Modified User admin
'''


class ExtendedUserAdmin(UserAdmin):
    inlines = [EntryInline]
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
