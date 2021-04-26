"""URL routes for Transfer app"""
from django.conf.urls import url, include
from rest_framework import routers
from Transfer.views import Transfer

def urls():
    """Make urls of routers"""
    router = routers.DefaultRouter()
    router.register(r'', Transfer)
    return router.urls

urlpatterns = [
    url(r'^', include(urls())),
]
