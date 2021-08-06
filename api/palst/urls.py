from django.urls import path, include
from . import views, viewsets
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('company', viewsets.CompanyViewSet)

app_name = 'palst'
urlpatterns = [
    path('', include(router.urls)),
]
