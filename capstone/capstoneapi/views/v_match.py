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
        fields = ('id', 'dater_id', 'dater', 'matched_with_id', 'matched_with', 'match_status_id', 'date_matched')
        depth = 2

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
        matched_with = self.request.query_params.get('matched_with_id', None)
        dater = self.request.query_params.get('dater_id', None)
        match_status = self.request.query_params.get('match_status_id', None)


        # SELECT * FROM capstoneapi_match m 
        # JOIN capstoneapi_dater d
        # on d.id = m.matched_with_id or d.id = m.dater_id 
        # WHERE m.match_status_id == 2 
        # AND m.dater_id == 26 
        # OR m.matched_with_id == 26
        # GROUP BY m.id

        # http://localhost:8000/matches?match_status_id=2&dater_id=26
        if match_status is not None and dater is not None:
            match = Match.objects.filter(match_status_id=match_status, dater__id=dater) | Match.objects.filter(match_status_id=match_status, matched_with__id=dater)
        else: 
            match = Match.objects.all().exclude(match_status_id=3)

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
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Match.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


    def update(self, request, pk=None):
        """
        Handles PUT requests for individual Match item

        Returns:
            Response -- Empty body with 204 status code
        """

        match = Match.objects.get(pk=pk)
        
        match.dater_id = request.data["dater_id"]
        match.matched_with_id = request.data["matched_with_id"]
        match.match_status_id = request.data["match_status_id"]

        match.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        """
        Handles POST request for Match

        Returns:
            Response JSON serialized Match instance
        """

        match = Match()

        match.dater_id = request.data["dater_id"]
        match.matched_with_id = request.data["matched_with_id"]
        match.match_status_id = request.data["match_status_id"]

        match.save()

        serializer=MatchSerializer(match, context={'request': request})

        return Response(serializer.data)