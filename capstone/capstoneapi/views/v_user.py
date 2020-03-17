from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for dater

    Arguments: 
        serializers.HyperlinkedModelSerializer
    """

class Meta:
    model = User
    url = serializers.HyperlinkedIdentityField(
        view_name='user',
        lookup_field='id'
    )
    
    fields = ('id', 'username','first_name', 'last_name', 'email')

class Users(ViewSet):
    def retrieve(self, request, pk=None):
            """Handle GET requests for single customer
            Returns:
                Response -- JSON serialized customer instance
            """

            try:
                user = User.objects.get(pk=pk)
                serializer = UserSerializer(user,
                context = {'request': request})
                return Response(serializer.data)
            except Exception as ex:
                return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to customers resource
        Returns:
            Response -- JSON serialized list of customers
        """       

        users = User.objects.all()

        # customer = self.request.query_params.get('customer', None)

        # if customer is not None:
        #     payment_types = payment_types.filter(customer__id=customer)

        serializer = UserSerializer(users, many = True, context={'request': request})

        return Response(serializer.data)