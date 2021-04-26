"""URL routes for account app"""
from django.conf.urls import path, include
from rest_framework import routers
from account.views import Account

def urls():
    """Make urls of routers"""
    router = routers.DefaultRouter()
    router.register(r'', Account)
    return router.urls

urlpatterns = [
    path('', include(urls())),
]
