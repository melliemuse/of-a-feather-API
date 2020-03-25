from django.http import HttpResponseServerError
# from django.db import connection
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from capstoneapi.models import Dater, Match
from capstoneapi.views.v_match import MatchSerializer
from django.contrib.auth.models import User



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
                  'age_range', 'tagline', 'been_reported', 'matching_daters', 'matched_with_daters', 'url')

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
        gender_preference = self.request.query_params.get('gender_preference', None)
        age_range = self.request.query_params.get('age_range', None)
        current_dater_only = request.query_params.get('self', False)
        # open_order = request.query_params.get('open', False)

        # if open_order == 'true':
        #   orders = orders.filter(payment_type__id=None)
        
        # dater.match_set (if no related-name)

        dater = Dater.objects.all()


        if attachment_style is not None:
            age_range_1 = age_range.split('-')[0]
            age_range_2 = age_range.split('-')[1]
            print(age_range_1)
            print(gender_preference)
            dater_id = request.auth.user.dater.id
            
            if attachment_style == '1' and gender_preference != 'all':
                dater = Dater.objects.raw(
                    '''
                    SELECT * FROM
                    capstoneapi_dater d
                    LEFT OUTER JOIN capstoneapi_match m
                    on d.id = m.matched_with_id or d.id = m.dater_id
                    WHERE d.id NOT IN (SELECT m.matched_with_id FROM capstoneapi_match m LEFT OUTER JOIN capstoneapi_dater d
                    on d.id = m.matched_with_id or d.id = m.dater_id WHERE m.dater_id == %s) 
                    AND d.id NOT IN (SELECT m.matched_with_id FROM capstoneapi_match m LEFT OUTER JOIN capstoneapi_dater d
                    on d.id = m.matched_with_id or d.id = m.dater_id WHERE m.match_status_id == 1 AND m.dater_id == %s)
                    AND d.id NOT IN (SELECT m.dater_id FROM capstoneapi_match m LEFT OUTER JOIN capstoneapi_dater d
                    on d.id = m.matched_with_id or d.id = m.dater_id WHERE m.match_status_id == 3 AND m.matched_with_id == %s)
                    AND d.id != %s AND d.age BETWEEN %s and %s AND d.gender == %s
                    GROUP BY d.id 
                    ''', [dater_id, dater_id, dater_id, dater_id, age_range_1, age_range_2, gender_preference]
                    )
            elif attachment_style == '1' and gender_preference == 'all':
                dater = Dater.objects.raw(
                    '''
                    SELECT * FROM 
                    capstoneapi_dater d
                    LEFT OUTER JOIN capstoneapi_match m
                    on d.id = m.matched_with_id or d.id = m.dater_id
                    WHERE d.id NOT IN (SELECT m.matched_with_id FROM capstoneapi_match m LEFT OUTER JOIN capstoneapi_dater d
                    on d.id = m.matched_with_id or d.id = m.dater_id WHERE m.dater_id == %s) 
                    AND d.id NOT IN (SELECT m.matched_with_id FROM capstoneapi_match m LEFT OUTER JOIN capstoneapi_dater d
                    on d.id = m.matched_with_id or d.id = m.dater_id WHERE m.match_status_id == 1 AND m.dater_id == %s)
                    AND d.id NOT IN (SELECT m.dater_id FROM capstoneapi_match m LEFT OUTER JOIN capstoneapi_dater d
                    on d.id = m.matched_with_id or d.id = m.dater_id WHERE m.match_status_id == 3 AND m.matched_with_id == %s)
                    AND d.id != %s AND d.age BETWEEN %s and %s 
                    GROUP BY d.id 
                    ''', [dater_id, dater_id, dater_id, dater_id, age_range_1, age_range_2]
                    )

                    
            elif attachment_style != '1' and gender_preference == 'all':
                dater = Dater.objects.raw(
                    '''
                    SELECT * FROM 
                    capstoneapi_dater d
                    LEFT OUTER JOIN capstoneapi_match m
                    on d.id = m.matched_with_id or d.id = m.dater_id
                    WHERE d.id NOT IN (SELECT m.matched_with_id FROM capstoneapi_match m LEFT OUTER JOIN capstoneapi_dater d
                    on d.id = m.matched_with_id or d.id = m.dater_id WHERE m.dater_id == %s) 
                    AND d.id NOT IN (SELECT m.matched_with_id FROM capstoneapi_match m LEFT OUTER JOIN capstoneapi_dater d
                    on d.id = m.matched_with_id or d.id = m.dater_id WHERE m.match_status_id == 1 AND m.dater_id == %s)
                    AND d.id NOT IN (SELECT m.dater_id FROM capstoneapi_match m LEFT OUTER JOIN capstoneapi_dater d
                    on d.id = m.matched_with_id or d.id = m.dater_id WHERE m.match_status_id == 3 AND m.matched_with_id == %s)
                    AND d.id != %s AND d.attachment_style_id = %s AND d.age BETWEEN %s and %s
                    GROUP BY d.id
                    ''', [dater_id, dater_id, dater_id, dater_id, 1, age_range_1, age_range_2]
                )

            elif attachment_style != '1' and gender_preference != 'all':
                dater = Dater.objects.raw(
                    '''
                    SELECT * FROM 
                    capstoneapi_dater d
                    LEFT OUTER JOIN capstoneapi_match m
                    on d.id = m.matched_with_id or d.id = m.dater_id
                    WHERE d.id NOT IN (SELECT m.matched_with_id FROM capstoneapi_match m LEFT OUTER JOIN capstoneapi_dater d
                    on d.id = m.matched_with_id or d.id = m.dater_id WHERE m.dater_id == %s) 
                    AND d.id NOT IN (SELECT m.matched_with_id FROM capstoneapi_match m LEFT OUTER JOIN capstoneapi_dater d
                    on d.id = m.matched_with_id or d.id = m.dater_id WHERE m.match_status_id == 1 AND m.dater_id == %s)
                    AND d.id NOT IN (SELECT m.dater_id FROM capstoneapi_match m LEFT OUTER JOIN capstoneapi_dater d
                    on d.id = m.matched_with_id or d.id = m.dater_id WHERE m.match_status_id == 3 AND m.matched_with_id == %s)
                    AND d.id != %s AND d.attachment_style_id = %s AND d.age BETWEEN %s and %s  AND d.gender == %s
                    GROUP BY d.id
                    ''', [dater_id, dater_id, dater_id, dater_id, 1, age_range_1, age_range_2, gender_preference]
                )

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

        user = User.objects.get(pk=dater.user.id)
        user.username = request.data["username"]
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.email = request.data["email"]
        user.password = request.data["password"]

        user.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

