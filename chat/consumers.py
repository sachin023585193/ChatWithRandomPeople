import json
from .models import *
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class SocketConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.username = self.scope['url_route']['kwargs']['username']
        self.send(json.dumps({'data-type':'waitingForUser'}))
        # checking whether a user is already waiting in a room or not
        gName , created = groupName.objects.get_or_create(used=False)
        # if no user is in the waiting room new room will be created
        # else used in the group name will be set to true
        if not created:
            self.room_group_name = gName.groupname
            gName.used = True
            gName.username2=self.username
            gName.save()
            async_to_sync(self.channel_layer.group_add)(
                    self.room_group_name,
                    self.channel_name
            ) 
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                'type':'broadcast.message',
                'data-type':'connectedToUser',
                'data':'',
                'username':self.username,
                }
            )
            # sends the other user's name connected to same channel to display in spinners place
            self.send(json.dumps({
                'data-type':'connectedToUser',
                'data':'',
                'sender':gName.username1,
                }))
        else:
            self.room_group_name = self.channel_name[-12:]
            gName.groupname=self.room_group_name
            gName.username1=self.username
            gName.save()
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )    

    def receive(self, text_data):
        data = json.loads(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'broadcast.message',
                'data-type':'broadcasted_message',
                'data':data,
                'username':self.username,
            }
        )
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_send)(self.room_group_name,{'type':'broadcast.message','data-type':'userDisconnected','data':'Unfortunately user got disconnected.','username':self.username,})
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
        userDisconnectedChat = groupName.objects.filter(groupname=self.room_group_name).exists()
        if userDisconnectedChat:
            groupName.objects.get(groupname=self.room_group_name).delete()


    def broadcast_message(self,event):
        self.send(json.dumps({
            'data-type':event['data-type'],
            'data':event['data'],
            'sender':event['username']
        }))


class privateSocketConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.username = self.scope['url_route']['kwargs']['username']
        self.room_group_name = self.scope['url_route']['kwargs']['roomname']
        self.room_group_name = self.scope['url_route']['kwargs']['roomname']
        self.is_host = self.scope['url_route']['kwargs']['is_host']
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'private.message.broadcast',
                'data-type':'userJoined',
                'data':self.username+' joined group',
                'noOfUsers':privateChat.objects.get(groupname=self.room_group_name).noOfUsers
            }
        )
    def disconnect(self, code):
        usersprivateChat = privateChat.objects.get(groupname=self.room_group_name)
        usersprivateChat.noOfUsers = usersprivateChat.noOfUsers - 1
        usersprivateChat.save()
        if usersprivateChat.noOfUsers == 0:
            async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
            zombieGroup = privateChat.objects.get(groupname=self.room_group_name)
            zombieGroup.delete()
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {'type':'private.message.broadcast','data-type':'userDisconnected','noOfUsers':usersprivateChat.noOfUsers}
        )
    
    def receive(self,text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'private.message.broadcast',
                'sender':self.username,
                'data-type':'broadcasted_message',
                'data':text_data,
            }
        )
    

    def private_message_broadcast(self,event):
        self.send(json.dumps({
            'data':event
        }))