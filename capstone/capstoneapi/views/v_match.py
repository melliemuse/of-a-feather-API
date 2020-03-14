from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from capstoneapi.models import Match

class MatchSerializer(serializers.HyperlinkedModelSerializer):
    """ JSON serializer for match

    Arguments:
        serializers.HyperlinkedModelSerializer
    """ 
    class Meta:
        model = Match
        url = serializers.HyperlinkedIdentityField(
            view_name='match',
            lookup_field='id',
        )
        fields = ('id', 'dater', 'matched_with', 'match_status', 'date_matched')

class Matches(ViewSet):
    def retrieve(self, request, pk=None):
        """
        Handles single GET request for Match
        
        Returns:
            Response -- JSON serialized Match Instance
        """

        try:
            match = Match.objects.get(pk=pk)
            serializer = MatchSerializer(match, context={'request': request})
            return Response(serializer.data)
        
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        Handles GET request for Match list

        Returns:
            Response -- JSON serialized Match list
        """

        match = Match.objects.all()
        serializer = MatchSerializer(match, many=True, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        Handles DELETE request to individual Match resource

        Returns:
            Response -- JSON serialized detail of deleted Match
        """

        try:
            Match.objects.get(pk=pk)
            Match.objects.delete()
            return Response({}, serializer.data)


    def update(self, request, pk=None):
        """
        Handles PUT requests for individual Match item

        Returns:
            Response -- Empty body with 204 status code
        """

    def create(self, request):
        """
        Handles POST request for Match

        Returns:
            Response JSON serialized Match instance
        """