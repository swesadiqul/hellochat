from django.contrib import admin
from chat.models import Chat, Group

# Register your models here.
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'timestamp', 'group')
    list_display_links = ('id', 'content')
    search_fields = ('content',)
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)
    list_per_page = 10
    list_filter = ('group',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)
    list_per_page = 10
    list_filter = ()
