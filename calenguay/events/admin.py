from django.contrib import admin

from .models import Category, Event, EventRule, EventType, UserCategory


class UserCategoryInline(admin.TabularInline):
    model = UserCategory
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [UserCategoryInline]


class EventRuleInline(admin.TabularInline):
    model = EventRule
    extra = 0


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    inlines = [EventRuleInline]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user")
