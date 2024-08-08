from django.db import models
import uuid
import time

# Create your models here.

def generate_unique_hash():    
    random_hash = str(uuid.uuid4().int)[:6]    
    timestamp = str(int(time.time()))    
    unique_hash = f"{random_hash}_{timestamp}"
    return unique_hash

class Utensil(models.Model):
    type=models.CharField(max_length=255)
    count=models.IntegerField()
    slug = models.SlugField(unique=True,null=True,blank=True)

    def __str__(self):
        return self.type    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
        super(Utensil, self).save(*args, **kwargs)                    
            

class Tag(models.Model):
    tag_id=models.CharField(max_length=255)
    utensil=models.ForeignKey(Utensil,on_delete=models.DO_NOTHING)
    status=models.BooleanField(default=True)

    def __str__(self):
        return self.tag_id