import json
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from capstoneapi.models import Dater


@csrf_exempt
def login_user(request):
    '''Handles the authentication of a user

    Method arguments:
      request -- The full HTTP request object
    '''

    req_body = json.loads(request.body.decode())

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Use the built-in authenticate method to verify
        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, respond with their token
        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps({"valid": True, "token": token.key})
            return HttpResponse(data, content_type='application/json')

        else:
            # Bad login details were provided. So we can't log the user in.
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')


@csrf_exempt
def register_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Load the JSON string of the request body into a dict
    req_body = json.loads(request.body.decode())

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    new_user = User.objects.create_user(
        username=req_body['username'],
        email=req_body['email'],
        password=req_body['password'],
        first_name=req_body['first_name'],
        last_name=req_body['last_name']
    )
    
    dater = Dater.objects.create(
        attachment_style_id=req_body['attachment_style_id'],
        location=req_body['location'], 
        bio=req_body['bio'],
        gender=req_body['gender'],
        gender_preference=req_body['gender_preference'],
        kids=req_body['kids'],
        smoker=req_body['smoker'],
        looking_for=req_body['looking_for'],
        interests=req_body['interests'],
        profile_pic=req_body['profile_pic'],
        age=req_body['age'],
        age_range=req_body['age_range'],
        tagline=req_body['tagline'],
        been_reported=req_body['been_reported'],
        user=new_user
    )
   

    # Commit the user to the database by saving it
    dater.save()

    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=new_user)

    # Return the token to the client
    data = json.dumps({"token": token.key})
    return HttpResponse(data, content_type='application/json')
