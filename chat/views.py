from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
User = get_user_model()

# Create your views here.
def home(request):
    return render(request, 'chat/index.html')

@login_required
def create_room(request):
    users = User.objects.all()
    context = {
        'users': [i.username for i in users]
    }
    return render(request, 'chat/create-room.html',context)