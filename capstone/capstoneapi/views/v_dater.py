from django.http import HttpResponseServerError
# from django.db import connection
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from capstoneapi.models import Dater, Match
from capstoneapi.views.v_match import MatchSerializer


class DaterSerializer(serializers.HyperlinkedModelSerializer):
    """ JSON serializer for dater

    Arguments:
        serializers.HyperlinkedModelSerializer
    """

    class Meta:
        model = Dater
        url = serializers.HyperlinkedIdentityField(
            view_name='dater',
            lookup_field='id',
        )
        fields = ('id', 'user', 'attachment_style', 'attachment_style_id', 'location', 'bio',
                  'gender', 'gender_preference', 'kids', 'smoker',
                  'looking_for', 'interests', 'profile_pic', 'age',
                  'age_range', 'tagline', 'been_reported', 'matching_daters', 'matched_with_daters')

        depth = 3

class Daters(ViewSet):
    
    def retrieve(self, request, pk=None):
        """
        Handles single GET request for Dater

        Returns:
            Response -- JSON serialized Dater Instance
        """

        try:
            dater = Dater.objects.get(pk=pk)
            serializer = DaterSerializer(
            dater, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        Handles GET request for Dater list

        Returns:
            Response -- JSON list of serialized Dater list
        """
        
        attachment_style = self.request.query_params.get('attachment_style_id', None)
        # match_status = self.request.query_params.get('match_status_id', None)
        

        dater = Dater.objects.all()
        # match = Match.objects.all().exclude(match_status_id=3)

        # dater.match_set (if no related-name)

        dater_id = request.auth.user.dater.id

        if attachment_style is not None:
            dater = Dater.objects.raw (
                (
                '''
                SELECT * FROM capstoneapi_dater d
                LEFT OUTER JOIN capstoneapi_match m 
                ON d.id = m.dater_id 
                AND m.match_status_id != 3 
                AND m.match_status_id != 2 
                AND m.dater_id != 26
                WHERE d.attachment_style_id == 1'''
                ))
            
            

        else:
            dater = Dater.objects.filter(id=request.auth.user.dater.id)
                
               
            
            # dater = dater.filter(attachment_style__id=attachment_style).exclude(id=request.auth.user.dater.id)
            # dater = dater.match_set.exclude(matched_with_daters__match_status=3)
            # dater = dater.exclude(matching_daters__dater_id=request.auth.user.dater.id)
            # matches = dater.exclude(match_status_daters=3)

            # matches = dater.matching_daters.exclude(dater_id=request.auth.user.dater.id)
        

        serializer = DaterSerializer(
        dater, many=True, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        Handles DELETE request to Dater resource

        Returns:
            Response -- JSON serialized detail of deleted Dater
        """

        try:
            dater = Dater.objects.get(pk=pk)
            dater.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Dater.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """
        Handles PUT request for individual Dater item

        Returns:
            Response -- Empty body with 204 status code
        """

        dater = Dater.objects.get(pk=pk)
        
        dater.location = request.data["location"]
        dater.bio = request.data["bio"]
        dater.attachment_style_id = request.data["attachment_style_id"]
        dater.gender = request.data["gender"]
        dater.gender_preference = request.data["gender_preference"]
        dater.looking_for = request.data["looking_for"]
        dater.interests = request.data["interests"]
        dater.kids = request.data["kids"]
        dater.smoker = request.data["smoker"]
        dater.profile_pic = request.data["profile_pic"]
        dater.age = request.data["age"]
        dater.age_range = request.data["age_range"]
        dater.tagline = request.data["tagline"]
        dater.been_reported = request.data["been_reported"]

        dater.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

