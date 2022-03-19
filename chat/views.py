from django.shortcuts import redirect, render
from .models import privateChat
# from .models import privateRoomUsers
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,'index.html')

def room(request):
    if request.method == 'POST':
        username = request.POST['username']
        context = {'username':username}
        return render(request,'chat/room.html',context)
    return redirect('index')

def privateRoom(request):
    if request.method == 'POST':
        username = request.POST['username']
        roomname = request.POST['roomname']
        password = request.POST['password']
        createOrJoin = request.POST['createOrJoin']
        if createOrJoin == 'create':
            if privateChat.objects.filter(groupname=roomname).exists():
                messages.error(request, 'RoomName already exists')
                return redirect('privateroom')
            else:
                newPrivateChatRoom = privateChat.objects.create(groupname=roomname,password=password)
                newPrivateChatRoom.save()  
                
        elif createOrJoin == 'join':
            privateChatRoom = privateChat.objects.filter(groupname=roomname,password=password)
            print(privateChatRoom)
            if not privateChatRoom.exists():
                messages.info(request, 'Invalid Credentials')
                return redirect('privateroom')
            else:
                print(privateChatRoom[0].noOfUsers )
                chatRoom = privateChatRoom[0]
                chatRoom.noOfUsers = chatRoom.noOfUsers + 1
                chatRoom.save()
                
        context ={'username':username,'roomname':roomname,'createOrJoin':createOrJoin}
        return render(request,'chat/privatechatroom.html',context)           
    return render(request,'chat/privateroom.html')