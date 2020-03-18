from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from capstoneapi.models import MatchStatus

class MatchStatusSerializer(serializers.HyperlinkedModelSerializer):
    """ JSON serializer for matchstatus

    Arguments:
        serializers.HyperlinkedModelSerializer
    """ 
    class Meta:
        model = MatchStatus
        url = serializers.HyperlinkedIdentityField(
            view_name='matchstatus',
            lookup_field='id',
        )
        fields = ('id', 'status_type')

class MatchStatuses(ViewSet):
    def retrieve(self, request, pk=None):
        """
        Handles single GET request for MatchStatus
        
        Returns:
            Response -- JSON serialized Matchstatus Instance
        """

        try:
            match_status = MatchStatus.objects.get(pk=pk)
            serializer = MatchStatusSerializer(match_status, context={'request': request})
            return Response(serializer.data)
        
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        Handles GET request for Status list

        Returns:
            Response -- JSON serialized Status list
        """

        match_status = MatchStatus.objects.all()
        serializer = MatchStatusSerializer(match_status, many=True, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        Handles DELETE request to individual Status resource

        Returns:
            Response -- JSON serialized detail of deleted Status
        """

        try:
            MatchStatus.objects.get(pk=pk)
            MatchStatus.objects.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except MatchStatus.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


    def update(self, request, pk=None):
        """
        Handles PUT requests for individual Match item

        Returns:
            Response -- Empty body with 204 status code
        """

        match_status = MatchStatus.objects.get(pk=pk)
        match_status.status_type = request.data["status_type"]

        match_status.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def create(self, request):
        """
        Handles POST request for Status

        Returns:
            Response JSON serialized Status instance
        """

        match_status = MatchStatus()

        match_status.status_type = request.data["status_type"]
        match_status.save()

        serializer=MatchStatusSerializer(match_status, context={'request', request})

        return Response(serializer.data)