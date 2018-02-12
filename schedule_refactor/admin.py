from django.contrib import admin
from schedule_refactor.forms import RuleForm

from schedule_refactor.models import Room, Reservation, RoomRelation, Rule

class RoomAdminOptions(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']

class RuleAdmin(admin.ModelAdmin):
    form = RuleForm

admin.site.register(Room, RoomAdminOptions)
admin.site.register(Rule, RuleAdmin)
admin.site.register([Reservation, RoomRelation])
