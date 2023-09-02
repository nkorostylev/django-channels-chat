
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from core.models import MessageModel, CustomUser
from rest_framework.serializers import ModelSerializer, CharField
from core.consumers import active_users

class MessageModelSerializer(ModelSerializer):

    user = CharField(source='user.username', read_only=True)
    recipient = CharField(source='recipient.username')

    def create(self, validated_data):
        user = self.context['request'].user
        recipient = get_object_or_404(
            CustomUser, username=validated_data['recipient']['username'])
        msg = MessageModel(recipient=recipient,
                           body=validated_data['body'],
                           user=user)
        msg.save()
        return msg

    class Meta:
        model = MessageModel
        fields = ('id', 'user', 'recipient', 'timestamp', 'body')

class UserModelSerializer(ModelSerializer):

    status = serializers.SerializerMethodField('get_status')

    def get_status(self, foo):
        return 'online' if active_users.get("{}".format(foo.id), 0) > 0 else ''

    class Meta:
        model = CustomUser
        status = serializers.SerializerMethodField('get_status')
        fields = ('id', 'username','status')