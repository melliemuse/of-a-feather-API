from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth.models import User
from django.contrib import admin
from capstoneapi.views import AttachmentStyles, Daters, register_user

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'attachmentstyles', AttachmentStyles, 'attachmentstyle')
router.register(r'daters', Daters, 'dater')

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token),
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token),
    path('register', register_user),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]