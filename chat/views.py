from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from chat.models import Rooms
User = get_user_model()

# Create your views here.
def home(request):
    context = {}
    if request.user.is_authenticated:
        rooms = Rooms.objects.filter(members = request.user)
        context['rooms'] = rooms
    return render(request, 'chat/index.html', context)

def handle_create_room(request):
    name = request.POST.get('name', None)
    room = Rooms.objects.create(Room_name = name)
    members = request.POST.getlist('members[]')
    for i in members:
        user = User.objects.get(username = i)
        room.members.add(user)
    return JsonResponse("added", safe=False, status = 200)

@login_required
def create_room(request):
    if request.method == 'POST':
        handle_create_room(request)
    users = User.objects.all()
    context = {
        'users': [i.username for i in users]
    }
    return render(request, 'chat/create-room.html',context)
@login_required
def chatPage(request, room_slug):
    room = Rooms.objects.get(slug = room_slug)
    members = room.members.all()
    if request.user in members:
        context = {
            'room':room,
        }
        return render(request, 'chat/chatPage.html', context)
    return HttpResponse("not authorized")