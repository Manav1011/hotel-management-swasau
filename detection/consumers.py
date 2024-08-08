import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Utensil,Tag
from django.db.models import Count, Case, When, IntegerField

class DetectionConsumer(AsyncWebsocketConsumer):
    entities = {'producers':None,'consumers':[]}
    async def connect(self):
        self.client = self.scope["url_route"]["kwargs"]["client"]
        if self.client == 'consumer':
            print("Consumer added")
            self.entities['consumers'].append(self)
            await self.channel_layer.group_add('consumers', self.channel_name)
        await self.accept()        

    async def disconnect(self,close_code): 
        await self.channel_layer.group_discard('consumers', self.channel_name)
        if self in self.entities['consumers']:
            self.entities['consumers'].remove(self)
        self.send(json.dumps(close_code))
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json['client'] == 'producer' and text_data_json.get('action'):
            if text_data_json['action'] == 'connection':
                self.entities['producers'] = self
                print(self.entities)
            if text_data_json['action'] == 'stream' and text_data_json.get('frame'):                
                if len(self.entities['consumers']) > 0:
                    frame_to_be_sent = await self.act_upon_the_stream(text_data_json['frame'])
                    await self.channel_layer.group_send(
                        "consumers", {"type": "send.frame", "frame_obj": {'action':'stream','frame':frame_to_be_sent}}
                    )


        if text_data_json['client'] == 'consumer' and text_data_json.get('action'):
            if text_data_json['action'] == 'connection':
                self.entities['producers'] = self
                initial_obj = await self.get_initial_obj()
                await self.channel_layer.group_send(
                        "consumers", {"type": "send.frame", "frame_obj": {'action':'initial_obj','obj':initial_obj}}
                    )

    # Receive message from room group
    async def send_frame(self, event):
        frame = event["frame_obj"]        
        await self.send(text_data=json.dumps(frame))
    
    @database_sync_to_async
    def get_initial_obj(self):
        initial_dict = {'countings':{'total_tags_inside':0,'total_tags_outside':0},'items':[]}
        utensils = Utensil.objects.all()
        for utensil in utensils:
            tags = utensil.tag_set.all()
            utensil_count = utensil.tag_set.all().aggregate(
                        true_count=Count(Case(When(status=True, then=1), output_field=IntegerField())),
                        false_count=Count(Case(When(status=False, then=1), output_field=IntegerField())),                
            )
            initial_dict['items'].append({"type":utensil.type,"count":utensil_count})
            for tag in tags:
                if tag.status == True:
                    initial_dict['countings']['total_tags_inside'] += 1
                else:
                    initial_dict['countings']['total_tags_outside'] += 1
        return initial_dict

    def get_current_obj(self):
        initial_dict = {'countings':{'total_tags_inside':0,'total_tags_outside':0},'items':[]}
        utensils = Utensil.objects.all()
        for utensil in utensils:
            tags = utensil.tag_set.all()
            utensil_count = utensil.tag_set.all().aggregate(
                        true_count=Count(Case(When(status=True, then=1), output_field=IntegerField())),
                        false_count=Count(Case(When(status=False, then=1), output_field=IntegerField())),                
            )
            initial_dict['items'].append({"type":utensil.type,"count":utensil_count})
            for tag in tags:
                if tag.status == True:
                    initial_dict['countings']['total_tags_inside'] += 1
                else:
                    initial_dict['countings']['total_tags_outside'] += 1

    @database_sync_to_async
    def act_upon_the_stream(self,frame):        
        tag = Tag.objects.select_related('utensil').filter(tag_id=frame['EPC']).first()         
        if tag:
            tag.status = frame['status']
            tag.save()            
            initial_dict = {'countings':{'total_tags_inside':0,'total_tags_outside':0},'items':[]}
            utensils = Utensil.objects.all()
            for utensil in utensils:
                tags = utensil.tag_set.all()
                utensil_count = utensil.tag_set.all().aggregate(
                            true_count=Count(Case(When(status=True, then=1), output_field=IntegerField())),
                            false_count=Count(Case(When(status=False, then=1), output_field=IntegerField())),                
                )
                initial_dict['items'].append({"type":utensil.type,"count":utensil_count})
                for tag_obj in tags:
                    if tag_obj.status == True:
                        initial_dict['countings']['total_tags_inside'] += 1
                    else:
                        initial_dict['countings']['total_tags_outside'] += 1            
            frame_to_be_sent = {'event':{'type':tag.utensil.type,'log':frame},'countings':initial_dict}
            print(frame_to_be_sent['event'])
            return frame_to_be_sent
        else:
            # Handle the case where the tag does not exist if necessary
            print("Tag does not exist")