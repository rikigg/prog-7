from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SurveyViewSet

router = DefaultRouter()
router.register(r'surveys', SurveyViewSet, basename='survey')

app_name = 'poll_analytics'

urlpatterns = [
    path('api/', include(router.urls)),
] 