from django.db import models
from account.models import User
from datetime import datetime

# Create your models here.
class TimestampedModel(models.Model):
    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class GroupAccount(TimestampedModel):
    # Each `Group Admin` must be able to create a co-operative account 


    group_admin = models.ForeignKey(User,on_delete=models.CASCADE)

    name = models.CharField(unique=True,max_length=250)

    amount = models.IntegerField(default=0)

    description = models.TextField()

    maximum_amount = models.IntegerField(default=0)

    start_date = models.DateTimeField(default=datetime.now())

    end_date = models.DateTimeField(default=datetime.now())

    is_searchable = models.BooleanField(default=False)

    def __str__(self):
        return  f"{self.name}"






class MemberAccount(TimestampedModel):
    # Each `User` must be able to join a co-operative account 
    member = models.ForeignKey(User,on_delete=models.CASCADE,related_name='member')

    group = models.ForeignKey(GroupAccount,on_delete=models.CASCADE,related_name='group_member')
    
    member_name = models.CharField(max_length=250,default='')

    amount = models.IntegerField(default=0)

    started_date = models.DateTimeField(default=datetime.now())

    end_date = models.DateTimeField(default=datetime.now())


    def __str__(self):
        return  f"{self.member} joined {self.group} group"

