from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from capstoneapi.models import Message

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    """ JSON serializer for match

    Arguments:
        serializers.HyperlinkedModelSerializer
    """ 
    class Meta:
        model = Message
        url = serializers.HyperlinkedIdentityField(
            view_name='message',
            lookup_field='id',
        )
        fields = ('id', 'message_body', 'time_sent', 'logged_in_user_id', 'match_id', 'match')
        depth = 2

class Messages(ViewSet):
    def retrieve(self, request, pk=None):
        """
        Handles single GET request for Message
        
        Returns:
            Response -- JSON serialized Message Instance
        """

        try:
            message = Message.objects.get(pk=pk)
            serializer = MessageSerializer(message, context={'request': request})
            return Response(serializer.data)
        
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        Handles GET request for Message list

        Returns:
            Response -- JSON serialized Message list
        """

        match = self.request.query_params.get('match_id', None)
        
        message = Message.objects.all()

        if match is not None:
            message = message.filter(match__id=match)


        serializer = MessageSerializer(message, many=True, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        Handles DELETE request to individual Message resource

        Returns:
            Response -- JSON serialized detail of deleted Message
        """
        
        try:
            message = Message.objects.get(pk=pk)
            message.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Message.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

    def update(self, request, pk=None):
        """
        Handles PUT requests for individual Message item

        Returns:
            Response -- Empty body with 204 status code
        """

        message = Message.objects.get(pk=pk)

        message.message_body = request.data["message_body"]
        message.logged_in_user_id = request.data["logged_in_user_id"]
        message.match_id = request.data["match_id"]

        message.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        """
        Handles POST request for Message

        Returns:
            Response JSON serialized Message instance
        """

        current_user = request.auth.user.dater.id

        message = Message()

        message.message_body = request.data["message_body"]
        message.logged_in_user_id = current_user
        message.match_id = request.data["match_id"]

        message.save()
        serializer=MessageSerializer(message, context={'request': request})

        return Response(serializer.data)