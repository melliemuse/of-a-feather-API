from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from capstoneapi.models import AttachmentStyle

class AttachmentStyleSerializer(serializers.HyperlinkedModelSerializer):
    """ JSON serializer for attachment style

    Arguments:
        serializers.HyperlinkedModelSerializer
    """ 
    class Meta:
        model = AttachmentStyle
        url = serializers.HyperlinkedIdentityField(
            view_name='attachmentstyle',
            lookup_field='id',
        )
        fields = ('id', 'name', 'description')

class AttachmentStyles(ViewSet):
    def retrieve(self, request, pk=None):
        """
        Handles single GET request for Attachment Style
        
        Returns:
            Response -- JSON serialized Attachment Style Instance
        """

        try:
            attachment_style = AttachmentStyle.objects.get(pk=pk)
            serializer = AttachmentStyleSerializer(
                attachment_style, context={'request', request})
            return Response(serializer.data)
        
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        Handles GET request for Attachment Style list
        
        Returns:
            Response -- JSON list of serialized Attachment Style list
        """
        attachment_style = AttachmentStyle.objects.all()
        
        serializer = AttachmentStyleSerializer(attachment_style, many=True, context={'request', request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        Handles DELETE request to Attachment Style resource

        Returns:
            Response -- JSON serialized detail of deleted Attachment Style
        """

        try: 
            attachment_style = AttachmentStyle.objects.get(pk=pk)
            attachment_style.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except AttachmentStyle.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def update(self, request, pk=None):
        """
        Handles PUT request for individual Attachment Style item
        
        Returns:
            Response -- Empty body with 204 status code
        """
        
        attachment_style = AttachmentStyle.objects.get(pk=pk)
        attachment_style.name = request.data["name"]
        attachment_style.description = request.data["description"]

        attachment_style.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        """
        Handles POST request for Attachment Style

        Returns:
            Response JSON serialized Attachment Style instance
        """

        new_attachment_style = AttachmentStyle()
        new_attachment_style.name = request.data["name"]
        new_attachment_style.description = request.data["description"]

        new_attachment_style.save()

        serializer=AttachmentStyleSerializer(new_attachment_style, context={'request', request})

        return Response(serializer.data)