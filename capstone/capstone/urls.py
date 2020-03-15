from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth.models import User
from django.contrib import admin
from capstoneapi.views import AttachmentStyles, Daters, Matches, MatchStatuses, Messages, register_user, login_user

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'attachmentstyles', AttachmentStyles, 'attachmentstyle')
router.register(r'daters', Daters, 'dater')
router.register(r'matches', Matches, 'match')
router.register(r'messages', Messages, 'message')
router.register(r'matchstatuses', MatchStatuses, 'matchstatus')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('api-token-auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]