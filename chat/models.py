from django.db import models
from django.contrib.auth import get_user_model
from autoslug import AutoSlugField
User = get_user_model()
# Create your models here.
class Rooms(models.Model):
    Room_name = models.CharField(max_length=22)
    members = models.ManyToManyField(User,related_name='books_authored', blank=True)
    slug = AutoSlugField(populate_from='Room_name')
    
    def __str__(self):
        return self.Room_name
    
    def get_members(self):
        return ', '.join([str(p.username) for p in self.members.all()])

class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_message', on_delete=models.CASCADE)
    content = models.TextField()
    room = models.ForeignKey(Rooms,related_name = 'related_room', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.author.username
    
    def last_10_messages(slug):
        room = Rooms.objects.get(slug = slug)
        message = Message.objects.filter(room = room).order_by('timestamp').all()
        if len(message) > 15:
            return message[len(message)-15:]
        else:
            return message

    def get_room(self):
        return self.room.Room_name