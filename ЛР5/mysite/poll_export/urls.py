from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExportViewSet

router = DefaultRouter()
router.register(r'surveys', ExportViewSet)

app_name = 'poll_export'

urlpatterns = [
    path('', include(router.urls)),
] 