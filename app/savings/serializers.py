from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import GroupAccount,MemberAccount



class GetGroupSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of Group objects."""
    group_admin = serializers.ReadOnlyField(source='group_admin.full_name')
    class Meta:
        model = GroupAccount
        fields = ('group_admin','name','description', 'amount','maximum_amount',)


class GroupSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of Group objects."""

    class Meta:
        model = GroupAccount
        fields = ('id','name','description', 'amount','maximum_amount')

    def update(self, instance, validated_data):
        """Performs an update on a User."""
        for (key, value) in validated_data.items():

            setattr(instance, key, value)

            instance.save()


        return instance




class MemberSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of Group objects."""

    class Meta:
        model = MemberAccount
        fields = ('id','amount')
    






    
