from django.contrib import admin
from .models import Info, Student, ReportInfo, Image

class InfoInline(admin.StackedInline):
    model = Info

class RepostInfoInline(admin.StackedInline):
    model = ReportInfo

class StudentManager(admin.ModelAdmin):
    list_display = ['uuid', 'have_info', 'check_in', 'info', 'openid']
    list_filter = ['have_info', 'check_in', 'openid']
    list_editable = ['have_info']
    search_fields = ['uuid', 'name', 'id_card']
    inlines = [InfoInline, RepostInfoInline]


admin.site.register(Info)
admin.site.register(Student, StudentManager)
admin.site.register(ReportInfo)
admin.site.register(Image)
