from django.contrib import admin
from .models import HeadPhoto, Notice, NoticeStudent, NoticeImage

class NoticeStudentManger(admin.ModelAdmin):
    search_fields = ['student__name']

class NoticeManger(admin.ModelAdmin):
    list_display = ['title', 'time', 'radio']
    list_editable = ['time']


admin.site.register(HeadPhoto)
admin.site.register(Notice, NoticeManger)
admin.site.register(NoticeStudent, NoticeStudentManger)
admin.site.register(NoticeImage)
