from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from chat.models import Rooms
User = get_user_model()

# Create your views here.
def home(request):
    return render(request, 'chat/index.html')

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