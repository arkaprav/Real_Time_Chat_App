from django.contrib import admin
from .models import Rooms, Message
# Register your models here.
class RoomsAdmin(admin.ModelAdmin):
    list_display = ('Room_name', 'get_members', 'slug')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('author','content','get_room', 'timestamp')

admin.site.register(Message, MessageAdmin)
admin.site.register(Rooms, RoomsAdmin)